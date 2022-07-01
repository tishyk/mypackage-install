import json
import re
import requests

class GeneratedAttribute:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Loader:
    def __init__(self, _dict):
        self.set_attrs(_dict, self.__dict__)

    def set_attrs(self, input_dict, output_dict):
        for key, value in input_dict.items():
            if isinstance(value, dict):
                output_dict[key] = GeneratedAttribute(key)
                self.set_attrs(value, output_dict[key].__dict__)
            else:
                output_dict[key] = value


    #
    # def searcher(self, input_dict, item, result=None):
    #     for key, value in input_dict.items():
    #         if item == key:
    #             return value
    #         elif isinstance(value, dict):
    #             result = self.searcher(input_dict[key], item, result)  # search recursively
    #     return result
    #
    #
    #
    #
    # def __getattr__(self, item):
    #     # print(data_loader.conv1)
    #     item_value = self.searcher(self.__dict__, item)
    #     return item_value
    #
    # def __getattribute__(self, item): # 'name'
    #     value = super().__getattribute__(item)
    #     if isinstance(value, dict) and item != '__dict__':
    #         value = BuiltInAttr(value)
    #     return value


#1 Load json data
with open('resnet.json') as f:
    data = json.load(f)

data # dict
d = {}
d.update(data)

data_loader = Loader(data)
#print(data_loader.conv1)    #{'type': 'conv', 'input': ['input_layer1'], 'output': ['maxpool1'], 'input_shapes': [[-1, 224, 224, 3]], 'output_shapes': [[-1, 112, 112, 64]], 'original_names': ['resnet_v1_18/conv1/Pad', 'resnet_v1_18/conv1/Conv2D', 'resnet_v1_18/conv1/BatchNorm/cond/FusedBatchNorm_1/Switch', 'resnet_v1_18/conv1/Relu'], 'quantization_params': {'bias_mode': 'double_scale_initialization'}, 'params': {'kernel_shape': [7, 7, 3, 64], 'strides': [1, 2, 2, 1], 'dilations': [1, 1, 1, 1], 'padding': 'SAME', 'groups': 1, 'batch_norm': True, 'elementwise_add': False, 'elementwise_bool': None, 'activation': 'relu'}}
#print(data_loader.input_shapes) # {'bias_mode': 'double_scale_initialization'}
print(data_loader.layers.conv1.quantization_params.bias_mode) # {'bias_mode': 'double_scale_initialization'}
# print(data_loader.name)
# print(data_loader.layers)
#
print(data_loader.name)
# data_loader.names


# data_loader = Loader('resnet.json')
# print(data_loader.layers['conv1']['input_shapes'][0][0])
#print(data_loader.layers.conv1.input_shapes[0][0])
# print(data_loader.layers.some_items)
# def factorial(n):
#     if n > 0:
#         return n * factorial(n-1)
#     else:
#         return 1
#
# print(factorial(6))

#
# def recursion(n):
#     print("Cycle", n)
#     if n <= 0:
#         return 0
#     else:
#         recursion(n-1)
#
# #def factorial(n): # n*(n-1)*(n-2)*(n-3) ... *(n-(n-1))
#
# def factorial(n):
#     if n > 0:
#         return n * factorial(n-1)
#     else:
#         return 1
#
# result = factorial(3) # 3 * 2 * 1 = 6
# result = factorial(0) # 3 * 2 * 1 = 6
# result = factorial(-10) # 3 * 2 * 1 = 6
# recursion(10)


#
# respond = requests.get("https://docs.pytest.org/en/latest/reference/reference.html#ini-options-ref")
# text = respond.text
#
# template1 = '\w' # a-z, 0-9, ! .?/
# template2 = '\d\d\d' # 0-9, ! .?/
# template3 = '\d{1, 10}' # 0-9, ! .?/  from 1 to 1000000000
# template4 = '.+' # 0-9, ! .?/  from 1 to 1000000000
#
# template5 = 'meta charset="\w+-\d+"'
# template6 = 'href="#\w*-?\w*"'
# template6c = re.compile('href="#(.*?)".+id="(.+?)"')
#
#
# res = template6c.findall(text, re.M)  # --> []
# res = re.findall(template6, text)  # --> []
# # res = re.search(template5, text)    # --> sre.Match object. group() / groups()
# # res.groups()
# # res = re.match(template5, text)
# # res = re.finditer(template5, text)
# print(res)
# len(res)
# set_res = [y for x, y in res]
#
# print(sorted(set_res))
#assert len(set_res) == len(res)