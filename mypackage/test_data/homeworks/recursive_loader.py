import os
import json


class GeneratedAttribute:
    """Class to represent attributes from JSON structure"""

    def __init__(self, name: str, _hidden=None):
        self.name = name  # Store attribute name as a string
        self._hidden = _hidden  # Store JSON structure as is. The same as Loader instance.__dict

    def __repr__(self):
        """Loader attribute representation as an instance of the current class"""
        return self.name


class Loader:
    """   Class to load JSON file values and structure them as nested attributes according to loaded JSON structure"""

    def __init__(self, json_path: str):
        if os.path.exists(json_path):
            with open(json_path) as json_file:
                self.__dict = json.load(json_file)
                self.recursive_set(self.__dict, self.__dict__)

    def recursive_set(self, input_dict: dict, output_dict: dict):
        """Method to update class instance attributes structure according to input_dict structure.
        output_dict will store generated attributes.
            Usage example:
                self.layers.conv1.quantization_params.bias_mode;
                """
        for key, value in input_dict.items():
            # Check value type is a dictionary and need to be represented with GeneratedAttribute instance
            if isinstance(value, dict):
                # Create new instance of the GeneratedAttribute class
                output_dict[key] = GeneratedAttribute(key, value)
                # Update __dict__ attribute of the just created instance recursively
                self.recursive_set(value, output_dict[key].__dict__)
            else:
                # Create new attribute of the current instance or recursively created GeneratedAttribute instance
                output_dict[key] = value

    def searcher(self, input_dict, item, result=None):
        """Method to get the first match of the item from the JSON structure"""
        for key, value in input_dict.items():
            if item == key:
                return value
            elif isinstance(value, dict):
                result = self.searcher(input_dict[key], item, result)  # search recursively in case of dictionary
        return result

    def __getattr__(self, item):
        """Overloaded to get much more easy access for attributes from loaded JSON structure.
        Will return first best item match in the current realization!
        Usage example: self.conv1, self.bias_mode, self.original_names
        Return: JSON structure value as is"""
        item_value = self.searcher(self.__dict__, item)
        return item_value


data_loader = Loader('resnet.json')  # Provide json file to load into created object

# How to get attribute. Option 1.  Get attribute created after recursive_set call
print(data_loader.name)
print(data_loader.layers)
print(data_loader.net_params.version)
print(data_loader.layers.conv1.quantization_params.bias_mode)

# How to get attribute. Option 2. Get attribute obtained with overloaded __getattr__ magic method
print(data_loader.conv1)
print(data_loader.input_shapes)
