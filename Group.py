import json

class Group:
    def __init__(self, num):
        self.num = num

        with open("groups.json") as f:
            groups = json.load(f)
        group = groups[num]

        self.name = group["name"]
        self.members = group["members"]