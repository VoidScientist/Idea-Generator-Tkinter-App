import random as rd
from collections.abc import Iterable


# Class to generate and store characters.
class Character:

    # Class constructor
    def __init__(self, data: dict, name="Character"):

        self.name = name
        self.attributes: dict = {}
        # TODO support multiple trait for each key if user desires it
        # TODO add custom commands like --> [RANDOM&1-100]
        # assign attributes randomly to the character
        for key in data:
            value = data[key]
            if type(value) is list and len(value) > 0:
                self.attributes[key] = rd.choice(value)
            if type(value) is str:
                self.attributes[key] = value

    # return the description
    def toStr(self):
        # string description that the user can interpret in the console
        description = ""
        for key in self.attributes:
            print(key, self.attributes)
            renderedKey = list(key)
            renderedKey[0] = key[0].upper()
            renderedKey = "".join(renderedKey)
            description += f"\n-{renderedKey}: {self.attributes[key]}"
        return f"{self.name} a pour caractéristiques :\n {description}"
