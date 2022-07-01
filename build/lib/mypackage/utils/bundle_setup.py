import os
import json
import time

from mypackage.utils.bundle_paths import DockerPaths, SWBundlePaths, BundleType

BUNDLE_ENV_PATH = f"{DockerPaths.WORKDIR.value}/env.json"
SW_BUNDLE_ENV_PATH = "env.json"


def get_bundle_env(bundle_type=None, env_path=BUNDLE_ENV_PATH):
    # file saved before activating devops env in order to use it later
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            my_env = json.load(f)
    elif bundle_type is not None and bundle_type == BundleType.RELEASE:
        my_env = os.environ.copy()
        my_env["PATH"] = ':'.join([DockerPaths.RELEASE_ENV_PATH.value, my_env["PATH"]])
    elif bundle_type is not None and bundle_type == BundleType.VALIDATION:
        my_env = os.environ.copy()
        my_env["PATH"] = ':'.join([SWBundlePaths.VALIDATION_ENV_PATH.value, my_env["PATH"]])
    elif bundle_type is not None and bundle_type == BundleType.SW_RELEASE:
        my_env = os.environ.copy()
        my_env["PATH"] = ':'.join([SWBundlePaths.RELEASE_ENV_PATH.value, my_env["PATH"]])
    return my_env


class BundleSetup:

    def setup(self):
        cur_dir = os.getcwd()
        self._change_dir()
        self._install_pcie()
        self._change_dir(cur_dir)

    def _run_command(self, cmd, ignore_errors=False, show_output=True, **kwargs):
        shell_runner = ShellRunner(self.working_dir)
        result = shell_runner.run(cmd, run_without_venv=True, ignore_errors=ignore_errors, **kwargs)
        return result

    def _reset_driver(self):
        cmd = "sudo modprobe -r hailo_pci && sudo modprobe hailo_pci && hailortcli fw-control reset --reset-type soft"
        self._run_command(cmd, ignore_errors=True)

    def _change_dir(self, path=None):
        path = path if path is not None else self.working_dir
        os.chdir(path)


class BundlePackageSetup(BundleSetup):
    DOCKER_RUN_SH = "hailo_sw_suite_docker_run.sh"

    def __init__(self, remote_dir_path, archive_name, archive_extension, logger):
        self.working_dir = os.getcwd()
        self.logger = logger
        self.remote_dir_path = f"{remote_dir_path}"
        self.archive_extension = archive_extension
        self.tarfile = f"{archive_name}.tar"
        self.archive_name = f"{archive_name}.{archive_extension}"
        self.image_name = archive_name
        self.package_path = os.path.join(self.remote_dir_path, self.archive_name)
        self._current_thread = None

    def setup(self):
        self.logger.info(f"Downloading file {FREENAS_IP}:{self.package_path}")
        SCPUtil.download(FREENAS_IP, self.package_path, os.getcwd())
        self.logger.info(f"Extracting files from {self.archive_name}")
        if self.archive_extension == "zip":
            self._run_command(f"unzip {self.archive_name}")
            self.logger.info(f"Extracting files from {self.tarfile}")
        else:
            self._run_command(f"gzip -d -f {self.archive_name}")
        self._run_command(f"tar -xvf {self.tarfile}")
        self.logger.info("Set env variable DISPLAY=:4.0")
        self._run_command("export DISPLAY=:4.0")
        self.logger.info(f"set {self.DOCKER_RUN_SH} file permissions")
        self._run_command(f"sudo chmod +x {self.DOCKER_RUN_SH}")
        self.logger.info(f"Change script {self.DOCKER_RUN_SH} content from interactive run to detached run")
        self._run_command(f'''sed -i 's/-ti $1"/-t -d $1"/g' {self.DOCKER_RUN_SH}''')
        self._run_command(f"sed -i 's/docker exec -it/docker exec -t -d/g' {self.DOCKER_RUN_SH}")
        self.override_container()

    def override_container(self):
        cmd = f"{self.working_dir}/{self.DOCKER_RUN_SH} --override"
        self.logger.info(f"Execute --override option: {cmd}")
        self._run_command(cmd)
        time.sleep(20)

    def resume_container(self):
        cmd = f"{self.working_dir}/{self.DOCKER_RUN_SH} --resume"
        self.logger.info(f"Execute --resume option: {cmd}")
        self._run_command(cmd)

    def skip_pcie_install_container(self):
        cmd = f"{self.working_dir}/{self.DOCKER_RUN_SH} --skip-pcie-install"
        self.logger.info(f"Execute --skip-pcie-install option: {cmd}")
        self._run_command(cmd)
        time.sleep(20)

    def show_help_container(self):
        cmd = f"{self.working_dir}/{self.DOCKER_RUN_SH} --help"
        self.logger.info(f"Execute --help option: {cmd}")
        self._run_command(cmd)

    @property
    def _container_hash(self):
        container_hash = ''
        out, *_ = self._run_command("docker ps")
        if out and isinstance(out, bytes):
            out = out.decode()
            for line in out.splitlines():
                if self.image_name in line:
                    container_hash = line.split()[0]
                    break
        return container_hash


class BundleReleaseSetup(BundleSetup):

    def __init__(self):
        self.working_dir = BundlePaths.PLATFORM.value

    def _install_pcie(self):
        self._run_command("yes | ./install.sh --pcie-driver-only")
        self._reset_driver()
        self._run_command("yes | ./install.sh --pcie-driver-only")


class BundleValidationSetup(BundleSetup):

    def __init__(self):
        self.working_dir = BundlePaths.PLATFORM_VALIDATION.value

    def _install_pcie(self):
        self._run_command("./install.py comp build_pcie")
        self._reset_driver()
        self._run_command("./install.py comp build_fw && ./install.py comp build_pcie")
