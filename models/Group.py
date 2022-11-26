import numpy as np
import pandas as pd
import json

from models.User import Student

class Team:

    def __init__(self, teamNum):
        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        self.teamNum = teamNum
        self.name = groups[teamNum]["name"]
        self.membersName = groups[teamNum]["members"]
        self.membersClass = []
        self.score = groups[teamNum]["score"]
        self.timeTable = self.createEmptyDF()

    def createEmptyDF(self):
        myArr = np.zeros((15, 7))
        time = pd.Series(['09:00 ~ 10:00', '10:00 ~ 11:00', '11:00 ~ 12:00', '12:00 ~ 13:00', '13:00 ~ 14:00', '14:00 ~ 15:00', '15:00 ~ 16:00',
                          '16:00 ~ 17:00', '17:00 ~ 18:00', '18:00 ~ 19:00', '19:00 ~ 20:00', '20:00 ~ 21:00', '21:00 ~ 22:00', '22:00 ~ 23:00', '23:00 ~ 24:00'])
        timeTable = pd.DataFrame(myArr, columns=['월', '화', '수', '목', '금', '토', '일'])
        timeTable = timeTable.set_index(time)
        return timeTable

    def addMemberClass(self):
        for name in self.membersName:
            self.membersClass.append(Student(name, self))

    def matchTime(self):
        self.timeTable = self.createEmptyDF()
        for member in self.membersClass:
            self.timeTable += member.timeTable