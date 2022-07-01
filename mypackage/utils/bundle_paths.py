from enum import Enum

WORKDIR_PATH = '/local/workspace'

class DockerPaths(Enum):
    EXECUTABLE = "docker_run.sh"
    IMAGE_NAME = "sw_suite"
    WORKDIR = WORKDIR_PATH


class SWBundlePaths(Enum):
    NETWORK_PATH = "releases/bundle_releases/"
    WORKDIR = "sw_suite"


class BundleType(Enum):
    RELEASE = "release"
    VALIDATION = "validation"
    SW_RELEASE = 'sw_release'
