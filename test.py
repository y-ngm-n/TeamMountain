from models.Meetings import Meeting

meeting_list = Meeting("team1")
print(meeting_list.getAllMeetings())
meeting_list.setMeetingAttendant("20221127", "송영민")
meeting_list.setMeetingAttendant("20221127", "송영민")
meeting_list.addMeeting("20221130")
meeting_list.setMeetingName("20221127", "아차차")
meeting_list.setMeetingMemo("20221127", "어라라라라라")
print(meeting_list.getTeamMeeting("20221127"))