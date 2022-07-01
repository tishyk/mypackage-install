import os
import re
import logging
import shlex
import time
import subprocess
import threading

from mypackage.utils.bundle_paths import DockerPaths

class Executable:
    "Class to handle docker bundle executable file and run it"

    def __init__(self, executable_file):
        self.executable = executable_file
        self.detached_executable = f"detached_{executable_file}"

    def detached_run(self, *args):
        "Run bundle executable file in detached state with provided options"
        self.create_detached_executable()
        out = subprocess.run(
            shlex.split(f"./{self.detached_executable} {' '.join(args)}"), 
                                                check=True, stdout=subprocess.PIPE).stdout.decode()

    def create_detached_executable(self):
        # Create a new file with changed docker run "-it" to "-d" 
        mode = f" -v {os.path.abspath('.')}:{DockerPaths.WORKDIR.value}/system-tests -d "
        if not os.path.exists(self.detached_executable):
            with open(self.executable) as src:
                with open(self.detached_executable, 'w') as dest:
                    
                    for line in src.readlines():
                        if "docker exec -it" in line:
                            line = line.replace(" -it ", mode)
                        elif "docker run ${DOCKER_ARGS} -ti $1" in line:
                            line = line.replace(" -ti ", mode)
                        dest.write(line)
            subprocess.run(shlex.split(f"chmod +x {self.detached_executable}"), check=True)

    def cleanup(self):
        if os.path.exists(self.detached_executable):
            os.remove(self.detached_executable)


class DockerImage:
    KEEP_ALIVE = False

    def __init__(self, image_name):
        self.image_name = image_name
        self.containers = []

    @property
    def image_ids(self):
        image_ids_cmd = f'docker images {self.image_name} -q'
        out = subprocess.run(shlex.split(image_ids_cmd), check=True, stdout=subprocess.PIPE).stdout.decode()
        return [image_id.strip() for image_id in out.splitlines()]

    @property
    def exists(self):
        return any(self.image_ids)

    def get_containers(self):
        for items in DockerContainer.docker_ps("-a"):
            container_id, image = items
            if self.image_name in image:
                self.containers.append(DockerContainer(container_id))
        return self.containers

    def wait_container_state(self, state, timeout=30):
        time_start = time.time()
        container = None
        found = False
        while time.time()-time_start <= timeout and not found:
            time.sleep(2)
            for container in self.get_containers():
                if container.status[0] == state:
                    found = True
                    break
        return container

    def remove(self, image_id):
        remove_cmd = f'docker rmi {image_id} -f'
        subprocess.run(shlex.split(remove_cmd), check=True, stdout=subprocess.PIPE)
    
    def remove_all(self):
        for image_id in self.image_ids:
            self.remove(image_id)

    def remove_containers(self, timeout=10):
        if not self.__class__.KEEP_ALIVE:
            for container in self.get_containers():
                if container.status[0]:
                    if container.status[0] != 'Exited':
                        container.runner.kill_container()
                    container.runner.rm_container()


class DockerContainer:
    def __init__(self, container_hash):
        self.container_hash = container_hash
        self.runner = ContainerRunner(container_hash)
        self.image = ''
        self.command = ''

    @property
    def status(self):
        """ Return container hash state and number. Number is a return code for exited container or junk for other """
        state, number = '',''
        cmd = 'docker ps -a  -f="id={0}" --format "{1}"'.format(self.container_hash, "{{.Status}}")
        out = subprocess.run(shlex.split(cmd), check=True, stdout=subprocess.PIPE).stdout.decode()
        found = re.search('(\w+).+?(\d+)', out)
        if found:
            state, number = found.groups()
        return state, number
        
    @staticmethod
    def docker_ps(*args):
        """ Return list with a tuples('container hash', 'image')"""
        args = " ".join(args)
        docker_ps_cmd = f"docker ps {args}"
        out = subprocess.run(shlex.split(docker_ps_cmd), check=True, stdout=subprocess.PIPE).stdout.decode()
        ps_output = re.findall("^(\w+)\s+(\w.+?:\w+)\s", out, re.M)
        return ps_output

        
class ContainerRunner:
    def __init__(self, container_hash=None):
        self._container_hash = container_hash
        self.running = False
        self.interactive = None

    def build_container(self, project_dir, image_name):
        build_cmd = f'docker build . --no-cache -t {image_name}'
        subprocess.run(shlex.split(build_cmd), cwd=project_dir, check=True, stdout=subprocess.PIPE)

    def run_container(self, image_name, options=('-d --network host')):
        self._container_hash = subprocess.run(
            shlex.split(f'docker run {image_name} {options}'), check=True, stdout=subprocess.PIPE
        ).stdout.decode()
        self.running = True


    def run_detached_container(self, image_name, options):
        self.interactive = threading.Thread(target=self.run_container, args=(image_name, options), daemon=True)
        self.interactive.start()
        print(f"Detached container thread started")


    def exec_container(self, cmd, workdir='"/local/workspace"'):
        exec_cmd = f'docker exec -e DISPLAY=:4.0 --workdir {workdir} {self._container_hash} {cmd}'
        try:
            out = 0, subprocess.run(shlex.split(exec_cmd), check=True, 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
        except subprocess.CalledProcessError as msg:
            out = 1, msg
        return out

    def kill_container(self):
        subprocess.run(shlex.split(f'docker kill {self._container_hash}'), check=True, stdout=subprocess.PIPE)

    def rm_container(self):
        subprocess.run(shlex.split(f'docker rm {self._container_hash}'), check=True, stdout=subprocess.PIPE)
    

class ComposeRunner:
    def __init__(self, docker_compose_file, services=None, logger_name=None):
        self._docker_compose_file = docker_compose_file
        self._services = services or ''
        self._logger = logging.getLogger(logger_name)

    @property
    def _prefix(self):
        return f'docker-compose -f {self._docker_compose_file}'

    def _run_cmd(self, cmd):
        self._logger.info(f'running {cmd}')
        subprocess.run(shlex.split(cmd), check=True)

    def build(self):
        build_cmd = f'{self._prefix} build --force-rm --no-cache {self._services}'
        self._run_cmd(build_cmd)

    def run(self, build=False):
        opts = '-d --renew-anon-volumes'
        if build:
            opts += ' --build --force-recreate'
        up_cmd = f'{self._prefix} up {opts} {self._services}'
        self._run_cmd(up_cmd)

    def kill(self):
        down_cmd = f'{self._prefix} down --remove-orphans'
        self._run_cmd(down_cmd)