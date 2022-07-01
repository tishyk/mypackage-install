import json

class BuiltInAttr:
    def __init__(self, dict):
        self.__dict__.update(dict)

class Loader:
    def __init__(self, path):
        with open(path) as f:
            self.__dict__.update(json.load(f))

    def searcher(self, input_dict, item, result=None):
        for key, value in input_dict.items():
            if item == key:
                return value
            elif type(value) is dict:
                result = self.searcher(input_dict[key], item)  # search recursively
        return result

    def __getattr__(self, item):
        item_value = self.searcher(self.__dict__, item)
        return item_value



data_loader = Loader('resnet.json')
data_loader.layers = BuiltInAttr(data_loader.layers)
print(data_loader.conv1)
data_loader

# def factorial(n):
#     if n > 0:
#         return n * factorial(n-1)
#     else:
#         return 1
#
# print(factorial(6))
