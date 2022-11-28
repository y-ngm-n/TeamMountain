import json


class Meeting:
    def __init__(self, teamName):
        self.team = teamName
        with open(f"./databases/meetings.json", encoding='UTF-8') as f:
            self.meetings = json.load(f)
            self.meeting = self.meetings[teamName]


    def getAllMeetings(self):
        return self.meetings

    def getTeamMeetings(self):
        return self.meeting

    def getTeamMeeting(self, date):
        return self.meeting[date]


    def addMeeting(self, date):
        self.meeting[date] = { "attendant": [], "memo": "" }
        with open(f"./databases/meetings.json", "w", encoding='UTF-8') as f:
            json.dump(self.meetings, f, indent=4, ensure_ascii=False)


    def setMeetingAttendant(self, date, member):
        attendant = self.meeting[date]["attendant"]
        if member not in attendant:
            self.meeting[date]["attendant"].append(member)
        with open(f"./databases/meetings.json", "w", encoding='UTF-8') as f:
            json.dump(self.meetings, f, indent=4, ensure_ascii=False)

    def setMeetingAllAttendant(self, date, attendant):
        self.meeting[date]["attendant"] = attendant
        with open(f"./databases/meetings.json", "w", encoding='UTF-8') as f:
            json.dump(self.meetings, f, indent=4, ensure_ascii=False)

    # def setMeetingName(self, date, name):
    #     self.meeting[date]["name"] = name
    #     with open(f"./databases/meetings.json", "w", encoding='UTF-8') as f:
    #         json.dump(self.meetings, f, indent=4, ensure_ascii=False)

    def setMeetingMemo(self, date, memo):
        self.meeting[date]["memo"] = memo
        with open(f"./databases/meetings.json", "w", encoding='UTF-8') as f:
            json.dump(self.meetings, f, indent=4, ensure_ascii=False)

        