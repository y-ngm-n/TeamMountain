import os
import sys
import json
import random


from PyQt6.QtWidgets import *
from PyQt6 import uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import QDate
from collections import defaultdict
import numpy as np
import pandas as pd

from models.User import Student, Professor
from models.Group import Team
from models.Meetings import Meeting
from views.resources import background_rc

global N, count
global attend
global teamList
global weeks

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('./views/main.ui')
form_class = uic.loadUiType(form)[0]

form_login = resource_path('./views/login.ui')
form_login_window = uic.loadUiType(form_login)[0]

form_student = resource_path('./views/student_main.ui')
form_student_window = uic.loadUiType(form_student)[0]

form_teacher = resource_path('./views/teacher_main.ui')
form_teacher_window = uic.loadUiType(form_teacher)[0]

form_timetable = resource_path('./views/timetable.ui')
form_timetable_window = uic.loadUiType(form_timetable)[0]

form_timetable_list = resource_path('./views/student_timetable_list.ui')
form_timetable_list_window = uic.loadUiType(form_timetable_list)[0]

form_show = resource_path('./views/show_time.ui')
form_show_window = uic.loadUiType(form_show)[0]

form_ranking = resource_path('./views/student_ranking.ui')
form_ranking_window = uic.loadUiType(form_ranking)[0]

form_person_ranking = resource_path('./views/person_ranking.ui')
form_person_ranking_window = uic.loadUiType(form_person_ranking)[0]

form_team_ranking = resource_path('./views/team_ranking.ui')
form_team_ranking_window = uic.loadUiType(form_team_ranking)[0]

form_meeting_main = resource_path('./views/student_attendance.ui')
form_meeting_main_window = uic.loadUiType(form_meeting_main)[0]

form_meeting_list = resource_path('./views/meeting_list.ui')
form_meeting_list_window = uic.loadUiType(form_meeting_list)[0]

form_teacher_meeting = resource_path('./views/teacher_attendance.ui')
form_teacher_meeting_window = uic.loadUiType(form_teacher_meeting)[0]

form_teacher_list = resource_path('./views/teacher_meeting.ui')
form_teacher_list_window = uic.loadUiType(form_teacher_list)[0]

form_leader_contribution = resource_path('./views/leader_list.ui')
form_leader_contribution_window = uic.loadUiType(form_leader_contribution)[0]

form_member_contribution = resource_path('./views/member_list.ui')
form_member_contribution_window = uic.loadUiType(form_member_contribution)[0]

form_todo = resource_path('./views/add_todo.ui')
form_todo_window = uic.loadUiType(form_todo)[0]

form_random = resource_path('./views/student_random.ui')
form_random_window = uic.loadUiType(form_random)[0]

form_teacher_attendance = resource_path('./views/teacher_attendance.ui')
form_teacher_attendance_window = uic.loadUiType(form_teacher_attendance)[0]

form_teacher_ranking = resource_path('./views/teacher_score.ui')
form_teacher_ranking_window = uic.loadUiType(form_teacher_ranking)[0]

form_teacher_score = resource_path('./views/teacher_team_score.ui')
form_teacher_score_window = uic.loadUiType(form_teacher_score)[0]

form_teacher_temp = resource_path('./views/teacher_temp.ui')
form_teacher_temp_window = uic.loadUiType(form_teacher_temp)[0]


# 시작 화면
class StartWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

    def btn_to_student(self):
        self.student = LoginWindow("student")
        self.hide()

    def btn_to_teacher(self):   # 교수자 DB 만들고 수정할 것
        self.teacher = LoginWindow("professor")
        self.hide()


# 로그인 화면
class LoginWindow(QMainWindow, QWidget, form_login_window):
    def __init__(self, login_type):
        super().__init__()
        self.type = login_type
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    # 로그인 함수: 로그인한 사용자 객체를 user로, 사용자가 속한 팀 객체를 team으로 반환 => (user, team) 형태
    def logIn(self, name):
        for team in teamList:
            if name in team.membersName:
                user = None
                team.addMemberClass()
                for mem in team.membersClass:
                    if mem.name == name:
                        user = mem
                return user, team
        return Professor(name), None

    def btn_login_clicked(self):
        global weeks

        with open("./databases/users.json") as f:
            users = json.load(f)

        weeks = self.spinBox.value()
        name = self.input_name.text()
        pw = self.input_pw.text()
        msg = QMessageBox()

        if not name: msg.information(self, "Login failed", "이름을 입력해주세요.")
        elif name in users:
            if pw == users[name]["pw"]:
                if self.type == "student":
                    if users[name]["group"]=="0": msg.information(self, "Access denied", "접근 권한이 없습니다.")
                    else:
                        temp = Student(name, [])
                        if str(type(temp)) == "<class 'models.User.Student'>":
                            msg.information(self, "Login success", f"{temp.name}님, 환영합니다.")
                            self.hide()
                            self.windowclass = StudentWindow(self.logIn(name))
                else:
                    if users[name]["group"]!="0": msg.information(self, "Access denied", "접근 권한이 없습니다.")
                    else:
                        temp = Professor(name)
                        if str(type(temp)) == "<class 'models.User.Professor'>":
                            msg.information(self, "Login success", f"{temp.name}님, 환영합니다.")
                            self.hide()
                            self.windowclass = TeacherWindow(self.logIn(name))

            else: msg.information(self, "Login failed", "비밀번호를 확인해주세요.")
        else: msg.information(self, "Login failed", "존재하지 않는 사용자입니다.")

    def btn_cancel_clicked(self):
        self.close()
        myWindow.show()


# 접속 화면
class WindowClass(QMainWindow, QWidget, form_class):
    def __init__(self, info):
        super().__init__()
        self.info = info
        self.name, self.team = self.info
        self.setupUi(self)
        self.show()

    def btn_to_student(self):
        if str(type(self.name)) == "<class 'models.User.Student'>":
            self.student = StudentWindow(self.info)
            self.hide()
        else:
            msg = QMessageBox()
            msg.information(self, "Access denied", "접근 권한이 없습니다.")

    def btn_to_teacher(self):   # 교수자 DB 만들고 수정할 것
        if str(type(self.name)) == "<class 'models.User.Professor'>":
            self.teacher = TeacherWindow()
            self.hide()
        else:
            msg = QMessageBox()
            msg.information(self, "Access denied", "접근 권한이 없습니다.")


# 학습자: 0. 메인 화면
class StudentWindow(QDialog, QWidget, form_student_window):
    def __init__(self, info):
        super(StudentWindow, self).__init__()
        self.info = info
        self.name, self.team = info
        self.init_ui()
        self.show()

    def init_ui(self):
        global weeks

        self.setupUi(self)
        self.table_info.setItem(-1, 1, QTableWidgetItem(f"{weeks}주차"))
        self.table_info.setItem(0, 1, QTableWidgetItem(f"{self.name.name}"))
        self.table_info.setItem(1, 1, QTableWidgetItem(f"{self.team.name}"))

    def btn_main_to_timetable(self):
        self.timetable = TimetableWindow(self.info)
        self.timetable.exec()
        self.team.matchTime()

    def btn_main_to_show(self):
        self.show_time_table = TimetableListWindow(self.info)
        self.show_time_table.exec()

    def btn_main_to_ranking(self):
        self.ranking = RankingWindow(self.team)
        self.ranking.exec()

    def btn_main_to_attendance(self):
        self.attendance = MeetingMainWindow(self.info)
        self.attendance.exec()

    def btn_main_to_contribution(self):
        with open(f"./databases/users.json") as f:
            users = json.load(f)
        if users[self.name.name]["leader"] == 1:
            self.contribution = LeaderContributionWindow(self.team)
        else:
            self.contribution = MemberContributionWindow(self.team)
        self.contribution.exec()

    def btn_main_to_random(self):
        self.set_random = RandomWindow(self.team)
        self.set_random.exec()

    def add_time(self, time):
        self.name.addTime(time)

    def logout(self):
        self.team.membersClass = []
        self.close()
        myWindow.show()


# 학습자: 1. 시간표 등록 화면
class TimetableWindow(QDialog, QWidget, form_timetable_window):
    def __init__(self, info):
        super(TimetableWindow, self).__init__()
        self.info = info
        self.name, self.team = info
        self.temp = Student("temp", self.team)
        self.init_ui()
        self.show()
        self.timeList = []

    def init_ui(self):
        global weeks

        self.setupUi(self)
        self.label_23.setText(f"{weeks}주차")

    def btn_timetable_to_main(self):
        self.close()

    def btn_timetable_to_timetable(self):
        for time in self.timeList: self.temp.addTime(time)
        self.name.timeTable = self.temp.timeTable
        self.name.setTimeTable(self.timeList)
        self.close()

    def btn_1(self):
        self.pushButton.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 09:00 ~ 10:00")
    def btn_2(self):
        self.pushButton_2.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 10:00 ~ 11:00")
    def btn_3(self):
        self.pushButton_3.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 11:00 ~ 12:00")
    def btn_4(self):
        self.pushButton_4.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 12:00 ~ 13:00")
    def btn_5(self):
        self.pushButton_5.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 13:00 ~ 14:00")
    def btn_6(self):
        self.pushButton_6.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 14:00 ~ 15:00")
    def btn_7(self):
        self.pushButton_7.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 15:00 ~ 16:00")
    def btn_8(self):
        self.pushButton_8.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 16:00 ~ 17:00")
    def btn_9(self):
        self.pushButton_9.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 17:00 ~ 18:00")
    def btn_10(self):
        self.pushButton_10.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 18:00 ~ 19:00")
    def btn_11(self):
        self.pushButton_11.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 19:00 ~ 20:00")
    def btn_12(self):
        self.pushButton_12.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 20:00 ~ 21:00")
    def btn_13(self):
        self.pushButton_13.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 21:00 ~ 22:00")
    def btn_14(self):
        self.pushButton_14.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 22:00 ~ 23:00")
    def btn_15(self):
        self.pushButton_15.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("월 23:00 ~ 24:00")
    def btn_16(self):
        self.pushButton_16.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 09:00 ~ 10:00")
    def btn_17(self):
        self.pushButton_17.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 10:00 ~ 11:00")
    def btn_18(self):
        self.pushButton_18.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 11:00 ~ 12:00")
    def btn_19(self):
        self.pushButton_19.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 12:00 ~ 13:00")
    def btn_20(self):
        self.pushButton_20.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 13:00 ~ 14:00")
    def btn_21(self):
        self.pushButton_21.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 14:00 ~ 15:00")
    def btn_22(self):
        self.pushButton_22.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 15:00 ~ 16:00")
    def btn_23(self):
        self.pushButton_23.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 16:00 ~ 17:00")
    def btn_24(self):
        self.pushButton_24.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 17:00 ~ 18:00")
    def btn_25(self):
        self.pushButton_25.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 18:00 ~ 19:00")
    def btn_26(self):
        self.pushButton_26.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 19:00 ~ 20:00")
    def btn_27(self):
        self.pushButton_27.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 20:00 ~ 21:00")
    def btn_28(self):
        self.pushButton_28.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 21:00 ~ 22:00")
    def btn_29(self):
        self.pushButton_29.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 22:00 ~ 23:00")
    def btn_30(self):
        self.pushButton_30.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("화 23:00 ~ 24:00")
    def btn_31(self):
        self.pushButton_31.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 09:00 ~ 10:00")
    def btn_32(self):
        self.pushButton_32.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 10:00 ~ 11:00")
    def btn_33(self):
        self.pushButton_33.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 11:00 ~ 12:00")
    def btn_34(self):
        self.pushButton_34.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 12:00 ~ 13:00")
    def btn_35(self):
        self.pushButton_35.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 13:00 ~ 14:00")
    def btn_36(self):
        self.pushButton_36.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 14:00 ~ 15:00")
    def btn_37(self):
        self.pushButton_37.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 15:00 ~ 16:00")
    def btn_38(self):
        self.pushButton_38.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 16:00 ~ 17:00")
    def btn_39(self):
        self.pushButton_39.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 17:00 ~ 18:00")
    def btn_40(self):
        self.pushButton_40.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 18:00 ~ 19:00")
    def btn_41(self):
        self.pushButton_41.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 19:00 ~ 20:00")
    def btn_42(self):
        self.pushButton_42.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 20:00 ~ 21:00")
    def btn_43(self):
        self.pushButton_43.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 21:00 ~ 22:00")
    def btn_44(self):
        self.pushButton_44.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 22:00 ~ 23:00")
    def btn_45(self):
        self.pushButton_45.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("수 23:00 ~ 24:00")
    def btn_46(self):
        self.pushButton_46.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 09:00 ~ 10:00")
    def btn_47(self):
        self.pushButton_47.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 10:00 ~ 11:00")
    def btn_48(self):
        self.pushButton_48.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 11:00 ~ 12:00")
    def btn_49(self):
        self.pushButton_49.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 12:00 ~ 13:00")
    def btn_50(self):
        self.pushButton_50.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 13:00 ~ 14:00")
    def btn_51(self):
        self.pushButton_51.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 14:00 ~ 15:00")
    def btn_52(self):
        self.pushButton_52.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 15:00 ~ 16:00")
    def btn_53(self):
        self.pushButton_53.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 16:00 ~ 17:00")
    def btn_54(self):
        self.pushButton_54.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 17:00 ~ 18:00")
    def btn_55(self):
        self.pushButton_55.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 18:00 ~ 19:00")
    def btn_56(self):
        self.pushButton_56.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 19:00 ~ 20:00")
    def btn_57(self):
        self.pushButton_57.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 20:00 ~ 21:00")
    def btn_58(self):
        self.pushButton_58.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 21:00 ~ 22:00")
    def btn_59(self):
        self.pushButton_59.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 22:00 ~ 23:00")
    def btn_60(self):
        self.pushButton_60.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("목 23:00 ~ 24:00")
    def btn_61(self):
        self.pushButton_61.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("금 09:00 ~ 10:00")
    def btn_62(self):
        self.pushButton_62.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("금 10:00 ~ 11:00")
    def btn_63(self):
        self.pushButton_63.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("금 11:00 ~ 12:00")
    def btn_64(self):
        self.pushButton_64.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.timeList.append("금 12:00 ~ 13:00")
    def btn_65(self):
        self.pushButton_65.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 13:00 ~ 14:00")
    def btn_66(self):
        self.pushButton_66.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 14:00 ~ 15:00")
    def btn_67(self):
        self.pushButton_67.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 15:00 ~ 16:00")
    def btn_68(self):
        self.pushButton_68.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 16:00 ~ 17:00")
    def btn_69(self):
        self.pushButton_69.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 17:00 ~ 18:00")
    def btn_70(self):
        self.pushButton_70.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 18:00 ~ 19:00")
    def btn_71(self):
        self.pushButton_71.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 19:00 ~ 20:00")
    def btn_72(self):
        self.pushButton_72.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 20:00 ~ 21:00")
    def btn_73(self):
        self.pushButton_73.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 21:00 ~ 22:00")
    def btn_74(self):
        self.pushButton_74.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 22:00 ~ 23:00")
    def btn_75(self):
        self.pushButton_75.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("금 23:00 ~ 24:00")
    def btn_76(self):
        self.pushButton_76.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 09:00 ~ 10:00")
    def btn_77(self):
        self.pushButton_77.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 10:00 ~ 11:00")
    def btn_78(self):
        self.pushButton_78.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 11:00 ~ 12:00")
    def btn_79(self):
        self.pushButton_79.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 12:00 ~ 13:00")
    def btn_80(self):
        self.pushButton_80.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 13:00 ~ 14:00")
    def btn_81(self):
        self.pushButton_81.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 14:00 ~ 15:00")
    def btn_82(self):
        self.pushButton_82.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 15:00 ~ 16:00")
    def btn_83(self):
        self.pushButton_83.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 16:00 ~ 17:00")
    def btn_84(self):
        self.pushButton_84.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 17:00 ~ 18:00")
    def btn_85(self):
        self.pushButton_85.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 18:00 ~ 19:00")
    def btn_86(self):
        self.pushButton_86.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 19:00 ~ 20:00")
    def btn_87(self):
        self.pushButton_87.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 20:00 ~ 21:00")
    def btn_88(self):
        self.pushButton_88.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 21:00 ~ 22:00")
    def btn_89(self):
        self.pushButton_89.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 22:00 ~ 23:00")
    def btn_90(self):
        self.pushButton_90.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("토 23:00 ~ 24:00")
    def btn_91(self):
        self.pushButton_91.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 09:00 ~ 10:00")
    def btn_92(self):
        self.pushButton_92.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 10:00 ~ 11:00")
    def btn_93(self):
        self.pushButton_93.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 11:00 ~ 12:00")
    def btn_94(self):
        self.pushButton_94.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 12:00 ~ 13:00")
    def btn_95(self):
        self.pushButton_95.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 13:00 ~ 14:00")
    def btn_96(self):
        self.pushButton_96.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 14:00 ~ 15:00")
    def btn_97(self):
        self.pushButton_97.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 15:00 ~ 16:00")
    def btn_98(self):
        self.pushButton_98.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 16:00 ~ 17:00")
    def btn_99(self):
        self.pushButton_99.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 17:00 ~ 18:00")
    def btn_100(self):
        self.pushButton_100.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 18:00 ~ 19:00")
    def btn_101(self):
        self.pushButton_101.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 19:00 ~ 20:00")
    def btn_102(self):
        self.pushButton_102.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 20:00 ~ 21:00")
    def btn_103(self):
        self.pushButton_103.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 21:00 ~ 22:00")
    def btn_104(self):
        self.pushButton_104.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 22:00 ~ 23:00")
    def btn_105(self):
        self.pushButton_105.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.timeList.append("일 23:00 ~ 24:00")


class TimetableListWindow(QDialog, QWidget, form_timetable_list_window):
    def __init__(self, info):
        super(TimetableListWindow, self).__init__()
        self.info = info
        self.user, self.team = info
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        mems = self.team.membersName
        self.table_timetables.setRowCount(len(mems))
        for i in range(len(mems)):
            btn = QPushButton(mems[i])
            btn.clicked.connect(lambda _, x=i: self.btn_timetable_clicked(self.team.membersClass[x]))
            self.table_timetables.setCellWidget(i, 0, btn)
            
    def btn_timetable_clicked(self, member):
        self.show_time_table = ShowWindow(member)
        self.show_time_table.exec()

    def btn_team_timetable_clicked(self):
        self.show_time_table = ShowWindow(self.team)
        self.show_time_table.exec()

    def btn_back_clicked(self):
        self.close()


# 학습자: 2. 시간표 조회 화면
class ShowWindow(QDialog, QWidget, form_show_window):
    def __init__(self, info):
        super(ShowWindow, self).__init__()
        self.info = info
        self.init_ui()
        self.show()

    def init_ui(self):
        global weeks

        self.setupUi(self)
        self.label_2.setText(f"{weeks}주차")
        time = ['09:00 ~ 10:00', '10:00 ~ 11:00', '11:00 ~ 12:00', '12:00 ~ 13:00', '13:00 ~ 14:00', '14:00 ~ 15:00', '15:00 ~ 16:00', '16:00 ~ 17:00', '17:00 ~ 18:00', '18:00 ~ 19:00', '19:00 ~ 20:00', '20:00 ~ 21:00', '21:00 ~ 22:00', '22:00 ~ 23:00', '23:00 ~ 24:00']
        day = ['월', '화', '수', '목', '금', '토', '일']
        if str(type(self.info)) == "<class 'models.User.Student'>":
            self.label.setText(f"{self.info.name}")
        else:
            self.label.setText(f"<<  {self.info.name}  >>")
            self.info.matchTime()
        for i in range(15):
            for j in range(7):
                if self.info.timeTable[day[j]][time[i]] >= 1:
                    self.tableWidget.setItem(i, j, QTableWidgetItem())
                    self.tableWidget.item(i, j).setBackground(QtGui.QColor(230, 0, 0))


# 학습자: 3. 순위 확인 화면
class RankingWindow(QDialog, QWidget, form_ranking_window):
    def __init__(self, team):
        super(RankingWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_ranking_to_main(self):
        self.close()

    def person_ranking(self):
        self.hide()
        self.person_ranking = PersonRankingWindow(self.team)
        self.person_ranking.exec()
        self.close()

    def team_ranking(self):
        self.hide()
        self.team_ranking = TeamRankingWindow(self.team)
        self.team_ranking.exec()
        self.close()


# 학습자: 3-1. 학습자 기여도 화면
class PersonRankingWindow(QDialog, QWidget, form_person_ranking_window):
    def __init__(self, team):
        super(PersonRankingWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

        with open(f"./databases/meetings.json") as f:
            attendance = json.load(f)

        with open(f"./databases/groups.json") as f:
            importance = json.load(f)

        for i in range(len(self.team.membersClass)):
            attend_score = 0
            for j in attendance[self.team.teamNum]:
                if self.team.membersClass[i].name in attendance[self.team.teamNum][j]['attendant']:
                    attend_score += 1

            import_score = 0
            for j in range(len(importance[self.team.teamNum]["todolist"])):
                if importance[self.team.teamNum]["todolist"][j][2] == self.team.membersClass[i].name and \
                        importance[self.team.teamNum]["todolist"][j][3] == "o":
                    import_score += int(importance[self.team.teamNum]["todolist"][j][1])

            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.team.membersClass[i].name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(attend_score)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(import_score)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(attend_score + import_score)))


# 학습자: 3-2. 팀 순위 화면
class TeamRankingWindow(QDialog, QWidget, form_team_ranking_window):
    def __init__(self, team):
        super(TeamRankingWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        global teamList

        self.setupUi(self)

        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        score = list()
        for i in range(9):
            score.append((groups[teamList[i].teamNum]["score"], teamList[i].teamNum))
        score.sort(reverse=True)

        for i in range(9):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(teamList[i].name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(groups[teamList[i].teamNum]["score"])))
            if score.index((groups[teamList[i].teamNum]["score"], teamList[i].teamNum)) <= 4:
                self.tableWidget.setItem(i, 2, QTableWidgetItem("A+"))
            elif score.index((groups[teamList[i].teamNum]["score"], teamList[i].teamNum)) <= 7:
                self.tableWidget.setItem(i, 2, QTableWidgetItem("B+"))
            else:
                self.tableWidget.setItem(i, 2, QTableWidgetItem("C+"))
            self.tableWidget.update()


# 학습자: 4. 회의 목록 달력
class MeetingMainWindow(QDialog, QWidget, form_meeting_main_window):
    def __init__(self, info):
        super(MeetingMainWindow, self).__init__()
        self.info = info
        self.user, self.team = info
        self.meet = Meeting(self.team.teamNum)
        self.meetings = self.meet.getTeamMeetings()
        color = QColor(255, 208, 138)
        self.fm = QTextCharFormat()
        self.fm.setBackground(color)
        self.init_ui()
        self.show()
        for date in self.meetings:
            date = QDate.fromString(date, "yyyyMMdd")
            self.calendarWidget.setDateTextFormat(date, self.fm)


    def init_ui(self):
        self.setupUi(self)


    def date_clicked(self):
        date = self.calendarWidget.selectedDate()
        date = date.toString("yyyyMMdd")
        
        self.meeting = MeetingListWindow(self.info, date)
        self.meeting.exec()
        self.close()

    def btn_attendance_to_main(self):
        self.close()


# 학습자: 4-1. 해당 날짜 회의 정보
class MeetingListWindow(QDialog, QWidget, form_meeting_list_window):
    def __init__(self, info, date):
        super(MeetingListWindow, self).__init__()
        self.init_ui()
        self.show()
        self.info = info
        self.user, self.team = info
        self.meeting = None
        self.date = date
        self.config()

    def init_ui(self):
        self.setupUi(self)

    def config(self):
        self.label_meeting_date.setText(self.date)
        members = self.team.membersName
        self.table_attendant.setRowCount(len(members))
        for i in range(len(members)):
            self.table_attendant.setItem(i, 0, QTableWidgetItem(members[i]))
            self.table_attendant.setCellWidget(i, 1, QCheckBox())

        self.meetings = Meeting(self.team.teamNum)

        if self.date in self.meetings.getTeamMeetings():
            self.meeting = self.meetings.getTeamMeeting(self.date)
            self.meeting_memo.setPlainText(self.meeting["memo"])

            attendant = self.meeting["attendant"]
            for i in range(len(members)):
                checkbox = self.table_attendant.cellWidget(i, 1)
                if members[i] in attendant: checkbox.toggle()


    def btn_previous_clicked(self):
        self.calendar = MeetingMainWindow(self.info)
        self.calendar.exec()
        self.close()

    def btn_delete_clicked(self):
        if self.meeting:
            self.meetings.deleteMeeting(self.date)
        self.calendar = MeetingMainWindow(self.info)
        self.calendar.exec()
        self.close()

    def btn_save_clicked(self):
        if self.date not in self.meetings.getTeamMeetings():
            self.meetings.addMeeting(self.date)
        attendant = []
        members = self.team.membersName
        for i in range(len(members)):
            checkbox = self.table_attendant.cellWidget(i, 1)
            if checkbox.isChecked(): attendant.append(members[i])
        self.meetings.setMeetingAllAttendant(self.date, attendant)
        
        memo = self.meeting_memo.toPlainText()
        self.meetings.setMeetingMemo(self.date, memo)

        self.calendar = MeetingMainWindow(self.info)
        self.calendar.exec()
        self.close()


# 학습자: 5-1. 조장 todo 리스트 화면
class LeaderContributionWindow(QDialog, QWidget, form_leader_contribution_window):
    def __init__(self, team):
        super(LeaderContributionWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

        combo = [self.comboBox, self.comboBox_2, self.comboBox_3, self.comboBox_4, self.comboBox_5, self.comboBox_6,
                 self.comboBox_7, self.comboBox_8, self.comboBox_9, self.comboBox_10]
        check = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5, self.checkBox_6,
                 self.checkBox_7, self.checkBox_8, self.checkBox_9, self.checkBox_10]

        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        for i in range(len(groups[self.team.teamNum]["todolist"])):
            for j in range(2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(groups[self.team.teamNum]["todolist"][i][j]))
            combo[i].addItem(groups[self.team.teamNum]["todolist"][i][2])
            if groups[self.team.teamNum]["todolist"][i][3] == "o":
                check[i].setChecked(True)

        self.comboBox.addItem(None)
        self.comboBox_2.addItem(None)
        self.comboBox_3.addItem(None)
        self.comboBox_4.addItem(None)
        self.comboBox_5.addItem(None)
        self.comboBox_6.addItem(None)
        self.comboBox_7.addItem(None)
        self.comboBox_8.addItem(None)
        self.comboBox_9.addItem(None)
        self.comboBox_10.addItem(None)

        for name in self.team.membersName:
            self.comboBox.addItem(name)
            self.comboBox_2.addItem(name)
            self.comboBox_3.addItem(name)
            self.comboBox_4.addItem(name)
            self.comboBox_5.addItem(name)
            self.comboBox_6.addItem(name)
            self.comboBox_7.addItem(name)
            self.comboBox_8.addItem(name)
            self.comboBox_9.addItem(name)
            self.comboBox_10.addItem(name)

    def btn_contribution_to_main(self):
        combo = [self.comboBox, self.comboBox_2, self.comboBox_3, self.comboBox_4, self.comboBox_5, self.comboBox_6,
                 self.comboBox_7, self.comboBox_8, self.comboBox_9, self.comboBox_10]
        check = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5, self.checkBox_6,
                 self.checkBox_7, self.checkBox_8, self.checkBox_9, self.checkBox_10]

        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        for i in range(len(groups[self.team.teamNum]["todolist"])):
            groups[self.team.teamNum]["todolist"][i][2] = combo[i].currentText()
            if check[i].isChecked() != 0:
                groups[self.team.teamNum]["todolist"][i][3] = "o"
            else:
                groups[self.team.teamNum]["todolist"][i][3] = "x"

        with open(f"./databases/groups.json", "w", encoding="utf-8") as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        self.close()

    def btn_add(self):
        self.add = addToDoWindow(self.team)
        self.add.exec()

        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        for i in range(len(groups[self.team.teamNum]["todolist"])):
            for j in range(3):
                self.tableWidget.setItem(i, j, QTableWidgetItem(groups[self.team.teamNum]["todolist"][i][j]))

        self.tableWidget.update()


# 학습자: 5-2. todo todo 리스트 화면
class MemberContributionWindow(QDialog, QWidget, form_member_contribution_window):
    def __init__(self, team):
        super(MemberContributionWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

        check = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5, self.checkBox_6,
                 self.checkBox_7, self.checkBox_8, self.checkBox_9, self.checkBox_10]

        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        for i in range(len(groups[self.team.teamNum]["todolist"])):
            for j in range(3):
                self.tableWidget.setItem(i, j, QTableWidgetItem(groups[self.team.teamNum]["todolist"][i][j]))
            if groups[self.team.teamNum]["todolist"][i][3] == "o":
                check[i].setChecked(True)

    def btn_contribution_to_main(self):
        check = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5, self.checkBox_6,
                 self.checkBox_7, self.checkBox_8, self.checkBox_9, self.checkBox_10]

        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        for i in range(len(groups[self.team.teamNum]["todolist"])):
            if check[i].isChecked() != 0:
                groups[self.team.teamNum]["todolist"][i][3] = "o"
            else:
                groups[self.team.teamNum]["todolist"][i][3] = "x"

        with open(f"./databases/groups.json", "w", encoding="utf-8") as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        self.close()


class addToDoWindow(QDialog, QWidget, form_todo_window):
    def __init__(self, team):
        super(addToDoWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_add_to_list(self):
        with open(f"./databases/groups.json") as f:
            groups = json.load(f)

        todo = self.lineEdit.text()
        importance = self.lineEdit_2.text()

        groups[self.team.teamNum]["todolist"].append([todo, importance, None, 'x'])
        with open(f"./databases/groups.json", "w", encoding="utf-8") as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        self.close()


class RandomWindow(QDialog, QWidget, form_random_window):
    def __init__(self, team):
        super(RandomWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        self.label.setText(f"당첨자는?")

    def Make_Number(self):
        member = []
        for name in self.team.membersName:
            member.append(name)
        Number = []
        for i in range(1):
            Number.append(member[random.randint(0, len(member) - 1)])
        return Number

    def randperson(self, label):
        Number = self.Make_Number()
        text = f'{Number[0]} 당첨!'
        Number.sort()
        self.label.setText(text)


# 교수자: 0. 메인 화면
class TeacherWindow(QDialog, QWidget, form_teacher_window):
    def __init__(self, info):
        super(TeacherWindow, self).__init__()
        self.init_ui()
        self.show()
        self.info = info

    def init_ui(self):
        self.setupUi(self)

    def btn_main_to_ranking(self):
        self.hide()
        self.ranking = TeacherRankingWindow()
        self.ranking.exec()
        self.show()

    def btn_main_to_attendance(self):
        self.attendance = TeacherTempWindow("attendance")
        self.attendance.exec()
        self.show()

    def btn_main_to_contribution(self):
        self.contribution = TeacherTempWindow("contribution")
        self.contribution.exec()
        self.show()

    def logout(self):
        self.close()
        myWindow.show()


class TeacherTempWindow(QDialog, QWidget, form_teacher_temp_window):
    def __init__(self, menu):
        super(TeacherTempWindow, self).__init__()
        self.menu = menu
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_team_number(self):
        global teamList

        team = teamList[self.spinBox.value() - 1]
        if self.menu == "attendance":
            self.meeting = TeacherMeetingMainWindow(team)
            self.close()
        elif self.menu == "contribution":
            self.contribution = TeacherContributionWindow(team)
            self.close()


# 교수자: 1. 점수 부여 화면
class TeacherRankingWindow(QDialog, QWidget, form_teacher_ranking_window):
    def __init__(self):
        super(TeacherRankingWindow, self).__init__()
        self.score = []
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        self.label.setText(self.getscore(1))
        self.label_2.setText(self.getscore(2))
        self.label_3.setText(self.getscore(3))
        self.label_4.setText(self.getscore(4))
        self.label_5.setText(self.getscore(5))
        self.label_6.setText(self.getscore(6))
        self.label_7.setText(self.getscore(7))
        self.label_8.setText(self.getscore(8))
        self.label_9.setText(self.getscore(9))

## groups.json에서 점수 가져오기
    def getscore(self, teamnum):
        with open(f"./databases/groups.json", encoding='UTF-8') as f:
            groups = json.load(f)
        self.score.append(groups["team1"]["score"])
        self.score.append(groups["team2"]["score"])
        self.score.append(groups["team3"]["score"])
        self.score.append(groups["team4"]["score"])
        self.score.append(groups["team5"]["score"])
        self.score.append(groups["team6"]["score"])
        self.score.append(groups["team7"]["score"])
        self.score.append(groups["team8"]["score"])
        self.score.append(groups["team9"]["score"])
        return str(self.score[teamnum - 1])

    def btn_score_1(self):
        self.score_window = TeacherScoreWindow(1)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_2(self):
        self.score_window = TeacherScoreWindow(2)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_3(self):
        self.score_window = TeacherScoreWindow(3)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_4(self):
        self.score_window = TeacherScoreWindow(4)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_5(self):
        self.score_window = TeacherScoreWindow(5)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_6(self):
        self.score_window = TeacherScoreWindow(6)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_7(self):
        self.score_window = TeacherScoreWindow(7)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_8(self):
        self.score_window = TeacherScoreWindow(8)
        self.score_window.exec()
        self.label_repaint()

    def btn_score_9(self):
        self.score_window = TeacherScoreWindow(9)
        self.score_window.exec()
        self.label_repaint()

    def label_repaint(self):
        self.score = []
        self.label.setText(self.getscore(1))
        self.label_2.setText(self.getscore(2))
        self.label_3.setText(self.getscore(3))
        self.label_4.setText(self.getscore(4))
        self.label_5.setText(self.getscore(5))
        self.label_6.setText(self.getscore(6))
        self.label_7.setText(self.getscore(7))
        self.label_8.setText(self.getscore(8))
        self.label_9.setText(self.getscore(9))
        self.label.repaint()
        self.label_2.repaint()
        self.label_3.repaint()
        self.label_4.repaint()
        self.label_5.repaint()
        self.label_6.repaint()
        self.label_7.repaint()
        self.label_8.repaint()
        self.label_9.repaint()


class TeacherScoreWindow(QDialog, QWidget, form_teacher_score_window):
    def __init__(self, num):
        super(TeacherScoreWindow, self).__init__()
        self.team = num
        self.score = []
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        self.label.setText(f'{self.team}조 점수 입력 : ')

    def btn_score(self):
        with open(f"./databases/groups.json") as f:
            groups = json.load(f)
        if self.team == 1:
            groups["team1"]["score"] = int(self.spinBox.value())
        elif self.team == 2:
            groups["team2"]["score"] = int(self.spinBox.value())
        elif self.team == 3:
            groups["team3"]["score"] = int(self.spinBox.value())
        elif self.team == 4:
            groups["team4"]["score"] = int(self.spinBox.value())
        elif self.team == 5:
            groups["team5"]["score"] = int(self.spinBox.value())
        elif self.team == 6:
            groups["team6"]["score"] = int(self.spinBox.value())
        elif self.team == 7:
            groups["team7"]["score"] = int(self.spinBox.value())
        elif self.team == 8:
            groups["team8"]["score"] = int(self.spinBox.value())
        else:
            groups["team9"]["score"] = int(self.spinBox.value())
        with open(f"./databases/groups.json", "w") as f:
            json.dump(groups, f, indent=4)

        self.close()


class TeacherMeetingMainWindow(QDialog, QWidget, form_teacher_meeting_window):
    def __init__(self, team):
        super(TeacherMeetingMainWindow, self).__init__()
        self.team = team
        self.meet = Meeting(self.team.teamNum)
        self.meetings = self.meet.getTeamMeetings()
        color = QColor(255, 208, 138)
        self.fm = QTextCharFormat()
        self.fm.setBackground(color)
        self.init_ui()
        self.show()
        for date in self.meetings:
            date = QDate.fromString(date, "yyyyMMdd")
            self.calendarWidget.setDateTextFormat(date, self.fm)

    def init_ui(self):
        self.setupUi(self)

    def date_clicked(self):
        date = self.calendarWidget.selectedDate()
        date = date.toString("yyyyMMdd")

        self.meeting = TeacherMeetingListWindow(self.team, date)
        self.meeting.exec()
        self.close()

    def btn_attendance_to_main(self):
        self.close()


class TeacherMeetingListWindow(QDialog, QWidget, form_teacher_list_window):
    def __init__(self, team, date):
        super(TeacherMeetingListWindow, self).__init__()
        self.init_ui()
        self.show()
        self.team = team
        self.meeting = None
        self.date = date
        self.config()

    def init_ui(self):
        self.setupUi(self)

    def config(self):
        self.label_meeting_date.setText(self.date)
        members = self.team.membersName
        self.table_attendant.setRowCount(len(members))
        for i in range(len(members)):
            self.table_attendant.setItem(i, 0, QTableWidgetItem(members[i]))
            self.table_attendant.setCellWidget(i, 1, QCheckBox())

        self.meetings = Meeting(self.team.teamNum)

        if self.date in self.meetings.getTeamMeetings():
            self.meeting = self.meetings.getTeamMeeting(self.date)
            self.meeting_memo.setPlainText(self.meeting["memo"])

            attendant = self.meeting["attendant"]
            for i in range(len(members)):
                checkbox = self.table_attendant.cellWidget(i, 1)
                if members[i] in attendant: checkbox.toggle()

    def btn_previous_clicked(self):
        self.calendar = TeacherMeetingMainWindow(self.team)
        self.calendar.exec()
        self.close()


# 교수자: 3. 기여도 화면
class TeacherContributionWindow(QDialog, QWidget, form_person_ranking_window):
    def __init__(self, team):
        super(TeacherContributionWindow, self).__init__()
        self.team = team
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

        with open(f"./databases/meetings.json") as f:
            attendance = json.load(f)

        with open(f"./databases/groups.json") as f:
            importance = json.load(f)

        for i in range(len(self.team.membersName)):
            attend_score = 0
            for j in attendance[self.team.teamNum]:
                if self.team.membersName[i] in attendance[self.team.teamNum][j]['attendant']:
                    attend_score += 1

            import_score = 0
            for j in range(len(importance[self.team.teamNum]["todolist"])):
                if importance[self.team.teamNum]["todolist"][j][2] == self.team.membersName[i] and \
                        importance[self.team.teamNum]["todolist"][j][3] == "o":
                    import_score += int(importance[self.team.teamNum]["todolist"][j][1])

            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.team.membersName[i]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(attend_score)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(import_score)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(attend_score + import_score)))



def configureDB():
    global teamList
    teamList = []

    team1 = Team("team1")
    team2 = Team("team2")
    team3 = Team("team3")
    team4 = Team("team4")
    team5 = Team("team5")
    team6 = Team("team6")
    team7 = Team("team7")
    team8 = Team("team8")
    team9 = Team("team9")

    teamList = [team1, team2, team3, team4, team5, team6, team7, team8, team9]


if __name__ == '__main__':
    configureDB()

    app = QApplication(sys.argv)
    myWindow = StartWindow()
    myWindow.show()
    app.exec()
