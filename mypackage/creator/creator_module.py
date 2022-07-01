import time


class Creator:
    def __init__(self, name):
        self.name = name

    def create_package(self, path):
        print(f"Package creation for path: {path}")
        time.sleep(2)
        print("Package created.")
