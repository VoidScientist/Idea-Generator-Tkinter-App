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
            self._data = {key: [] for key in self.allowedKeys}
        elif isinstance(keys, str):
            self.allowedKeys = keys
            # generate data from allowed key
            self._data = {keys: []}
        elif keys is None:
            self.allowedKeys = PropertyStorage.allowedKeys
            self._data = {key: [] for key in self.allowedKeys}

        self.load()

    def load(self):
        # loading the class
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'rb') as f:
                try:
                    tempData = pickle.load(f)
                    self.allowedKeys = [key for key in tempData[0]]
                    self._data = {key: [] for key in self.allowedKeys}
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

    def updateAllowedKeys(self, keys, action):
        if action == "remove" and keys in self.allowedKeys:
            self.allowedKeys.remove(keys)
        if action == "add" and keys not in self.allowedKeys:
            self.allowedKeys.append(keys)

    # add or remove allowed keys from the class
    def setAllowedKeys(self, keys, action="add"):
        if keys is str:
            self.updateAllowedKeys(keys, action)
        elif keys is list:
            for key in keys:
                self.updateAllowedKeys(keys, action)

        self.save()
        self.load()

    def getKeys(self):
        res = "Keys :\n\n"
        for keys in self.allowedKeys:
            res += f"-{keys}\n"
        return res

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
            self._data = {key: [] for key in PropertyStorage.allowedKeys}
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
        # function should return messages according to either value already exists or doesn't or invalid action
        if action == "remove" and value in self.data[key]:
            self._data[key].remove(value)
            self.save()
        elif action == "add" and value not in self.data[key]:
            self._data[key].append(value)
            self.save()

    # used to limit case sensitivity
    def lowercase(self, value):
        # make the function not case sensitive
        if value is str:
            return value.lower()
        elif value is list:
            return list(map(lambda x: x.lower(), value))
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
