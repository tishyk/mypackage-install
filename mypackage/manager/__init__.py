from .manager_module import Manager
from ..creator.creator_module import Creator

# Creator.manager = Manager.DEFAULT_MANAGER
# Creator = Creator('Jessie') # --> Jordan
Manager.Creator = Creator('Jessie')


class Creator(Creator):
    manager = Manager.DEFAULT_MANAGER

    def __init__(self):
        super('Jessie').__init__()
