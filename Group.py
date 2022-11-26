import numpy as np
import pandas as pd



class Team:
    def __init__(self, name, score):
        self.timeTable = self.createEmptyDF()
        self.teamName = name
        self.teamMembers = []
        self.teamScore = score

    def createEmptyDF(self):
        myArr = np.zeros((15, 7))
        time = pd.Series(['09:00 ~ 10:00', '10:00 ~ 11:00', '11:00 ~ 12:00', '12:00 ~ 13:00', '13:00 ~ 14:00', '14:00 ~ 15:00', '15:00 ~ 16:00',
                          '16:00 ~ 17:00', '17:00 ~ 18:00', '18:00 ~ 19:00', '19:00 ~ 20:00', '20:00 ~ 21:00', '21:00 ~ 22:00', '22:00 ~ 23:00', '23:00 ~ 24:00'])
        timeTable = pd.DataFrame(myArr, columns=['월', '화', '수', '목', '금', '토', '일'])
        timeTable = timeTable.set_index(time)
        return timeTable

    def addTeamMember(self, nameList):
        for name in nameList:
            self.teamMembers.append(Student(name))


'''
import json

class Group:
    def __init__(self, num):
        self.num = num

        with open("groups.json") as f:
            groups = json.load(f)
        group = groups[num]

        self.name = group["name"]
        self.members = group["members"]
'''        