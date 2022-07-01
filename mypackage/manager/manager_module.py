#from mypackage.creator.creator_module import Creator
from ..creator.creator_module import Creator

#   File "C:\Projects\Hillel_Automation\Packages\mypackage\manager\manager_module.py", line 2, in <module>
#     from ..creator.creator_module import Creator
# ImportError: attempted relative import with no known parent package

class Manager:
    """Class to represent manager"""
    DEFAULT_MANAGER = 'Jordan'

    def __init__(self, name, request):
        self.name = name
        self.request = request
        self.creators = []

    def add_creator(self, name):
        creator = Creator(name)
        self.creators.append(creator)
        return creator

    def proceed_request(self):
        print(f"Running {self.name} request {self.request}")


if __name__ == "__main__":
    print(Manager("Jordan", "empty"))
