import os.path
import pickle
from collections.abc import Iterable


# class to store all the properties
class PropertyStorage:
    allowedKeys = ['personality', 'country', 'job', 'sex']

    # construct the class
    def __init__(self, keys=None, name="default"):
        # creating a filepath in order to save the class
        self.name = str(name)
        self.filepath = str("saves/" + name + ".pickle")

        # filter what to do with the keys parameter
        if isinstance(keys, Iterable) and not isinstance(keys, str):
            self.allowedKeys = [key for key in keys]
            # generate data from allowed keys
            self.__setattr__("_data", {key: [] for key in self.allowedKeys}, self)
        elif isinstance(keys, str):
            self.allowedKeys = keys
            # generate data from allowed key
            self.__setattr__("_data", {keys: []}, self)
        elif keys is None:
            self.allowedKeys = PropertyStorage.allowedKeys
            self.__setattr__("_data", {key: [] for key in self.allowedKeys}, self)

        self.load()

    def load(self):
        # loading the class
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'rb') as f:
                try:
                    tempData = pickle.load(f)
                    self.allowedKeys = [key for key in tempData[0]]
                    self.__setattr__("_data", {key: [] for key in self.allowedKeys}, self)
                    for key in tempData[1]:
                        for x in tempData[1][key]:
                            self.setData(x, key)
                    print("Loaded !", self.filepath)
                except EOFError:
                    print("Nothing to load, moving on...")
        else:
            open(self.filepath, "x")

        self.save()

    def getName(self):
        return self.name

    # add or remove allowed keys from the class
    def setAllowedKeys(self, keys, action="add"):
        if isinstance(keys, Iterable) and not isinstance(keys, str):
            for key in keys:
                match action:
                    case "remove":
                        if key in self.allowedKeys:
                            self.allowedKeys.remove(key)
                    case "add":
                        if key not in self.allowedKeys:
                            self.allowedKeys.append(key)
        elif isinstance(keys, str):
            match action:
                case "remove":
                    if keys in self.allowedKeys:
                        self.allowedKeys.remove(keys)
                case "add":
                    if keys not in self.allowedKeys:
                        self.allowedKeys.append(keys)
        self.save()
        self.load()

    def getKeys(self):
        res = "Keys :\n\n"
        for keys in self.allowedKeys:
            res += f"-{keys}\n"
        return res

    # act according to the attribute being modified
    def __setattr__(self, key, value, other=None):
        if key == "_data" and other != self:
            print("Access refused, use expected/conventional means like --> PropertyStorage.setData()")
        else:
            super().__setattr__(key, value)

    # interprets user input to then add it to the _data
    def userInterpret(self, input):
        if isinstance(input, str):
            if ":" in input:
                keySepIndex = input.find(":")
                key = input[keySepIndex + 1:]
                value = input[:keySepIndex].split(",")
            else:
                print("Lack of key in the command")
                return
            if "&" in input:
                actionSepIndex = input.find("&")
                key = input[keySepIndex + 1:actionSepIndex]
                value = input[:keySepIndex].split(",")
                action = input[actionSepIndex + 1:]
            else:
                action = "add"

            for i in range(len(value)):
                value[i] = value[i].strip()

            print(f"\n{key}\n{value}\n{action}")
            self.setData(value, key, action)
        else:
            print("Wrong input")

    def userInterpretKey(self, input):
        if isinstance(input, str):
            if "&" in input:
                actionSepIndex = input.find("&")
                keys = input[:actionSepIndex].split(",")
                action = input[actionSepIndex + 1:]

            for i in range(len(keys)):
                keys[i] = keys[i].strip()

            print(f"{keys}\n{action}")

            self.setAllowedKeys(keys, action)

    # print the class
    def toStr(self):
        storage = ""
        for key in self._data:
            storage += f"\n-{key}:" + str(self._data[key])
        return f"\n{self.name} is storing: {storage}"

    # either clear the whole _data or just a specific key
    def clear(self, key=None):
        if key is None:
            self.__setattr__("_data", {key: [] for key in PropertyStorage.allowedKeys}, self)
            self.save()
        else:
            self._data[key] = []
            self.save()

    def displayData(self):
        res: str = ""
        data = self.getData()
        for key in data:
            if res == "":
                res += f"{key}:\n"
            else:
                res += f"\n{key}:\n"
            for values in data[key]:
                res += f"\t-> {values}\n"
        return res

    # get the data
    def getData(self):
        return self._data

    # refactor of a portion of setData(), used to add or remove a value to _data
    def actionCheck(self, value, key, action):
        match action:
            case "remove":
                if value in self.data[key]:
                    self._data[key].remove(value)
                    self.save()
                else:
                    print("Value already not present")
            case "add":
                if value not in self.data[key]:
                    self._data[key].append(value)
                    self.save()
                else:
                    print("Value already registered")
            case _:
                print('Invalid action, try again with either "add" or "remove"')

    # used to limit case sensitivity
    def lowercase(self, value):
        # make the function not case sensitive
        if isinstance(value, Iterable) and not isinstance(value, str):
            for i in range(len(value)):
                value[i] = value[i].lower()
        elif isinstance(value, str):
            return value.lower()
        else:
            print(f"Unexpected value data type detected during while removing case sensibility'", value, type(value))
        return value

    # Setter for the data in the class
    def setData(self, value, key, action="add"):
        value = self.lowercase(value)
        key = self.lowercase(key)

        # check if key is allowed
        if key in self.allowedKeys:
            # is the key in data iterable ?
            if isinstance(self._data[key], Iterable):
                # is the value iterable and not a string ?
                if isinstance(value, Iterable) and not isinstance(value, str):
                    # iterates through the values
                    for item in value:
                        # act according to chosen action
                        self.actionCheck(item, key, action)
                else:
                    # act according to chosen action
                    self.actionCheck(value, key, action)
            else:
                print("Unexpected datatype in _data, report this to the developer")
        else:
            print(
                f"Exception in 'PropertyStorage -> setData', key: '{key}' not allowed. Try one of those : {PropertyStorage.allowedKeys}")

    # Save class in a .pickle file
    def save(self):
        with open(self.filepath, 'wb') as f:
            pickle.dump([self.allowedKeys, self._data], f)

    data = property(getData, setData)


a = PropertyStorage()
a.setAllowedKeys("test1", "remove")
print(a.allowedKeys)
