import json

class User:
    def __init__(self, name):
        self.name = name

        with open("users.json") as f:
            users = json.load(f)
        user = users[name]
        self.type = user["type"]
        self.group = user["group"]



class Student(User):
    def __init__(self, name):
        User.__init__(self, name)
        print(self.name, self.type)


class Professor(User):
    def __init__(self, name):
        User.__init__(self, name)
        print(self.name, self.type)