import numpy as np
import pandas as pd



class Student:
    def __init__(self, name):
        self.timeTable = self.createEmptyDF()
        self.studentName = name

    def addTime(self, impossibleTime):
        if impossibleTime == '0':
            return
        else:
            impossibleTime = impossibleTime.split()
            impossibleTime[1] = impossibleTime[1].split('~')
            impossibleTime[1][0] = impossibleTime[1][0].strip()
            self.timeTable.loc[impossibleTime[1][0]
                :impossibleTime[3], impossibleTime[0]] = 1
            return self.timeTable

    def createEmptyDF(self):
        myArr = np.zeros((15, 7))
        time = pd.Series(['09:00 ~ 10:00', '10:00 ~ 11:00', '11:00 ~ 12:00', '12:00 ~ 13:00', '13:00 ~ 14:00', '14:00 ~ 15:00', '15:00 ~ 16:00',
                          '16:00 ~ 17:00', '17:00 ~ 18:00', '18:00 ~ 19:00', '19:00 ~ 20:00', '20:00 ~ 21:00', '21:00 ~ 22:00', '22:00 ~ 23:00', '23:00 ~ 24:00'])
        timeTable = pd.DataFrame(myArr, columns=['월', '화', '수', '목', '금', '토', '일'])
        timeTable = timeTable.set_index(time)
        return timeTable

    def matchTime(self):
        for team in teamList:
            if self in team.teamMembers:
                team.timeTable = team.createEmptyDF()
                for member in team.teamMembers:
                    team.timeTable = team.timeTable + member.timeTable
                    


# import json

'''
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


class Professor(User):
    def __init__(self, name):
        User.__init__(self, name)
'''