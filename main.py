import os
import sys
import json

from PyQt6.QtWidgets import *
from PyQt6 import uic, QtGui
from collections import defaultdict
import resource_rc
import numpy as np
import pandas as pd

from User import *
from Group import *

global N, count
global attend
global user
global group
global teamList


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

form_start = resource_path('start.ui')
form_start_window = uic.loadUiType(form_start)[0]

form_login = resource_path('login.ui')
form_login_window = uic.loadUiType(form_login)[0]

form_student_login = resource_path('student_login.ui')
form_student_login_window = uic.loadUiType(form_student_login)[0]

form_student = resource_path('student_main.ui')
form_student_window = uic.loadUiType(form_student)[0]

form_teacher = resource_path('teacher_main.ui')
form_teacher_window = uic.loadUiType(form_teacher)[0]

form_timetable = resource_path('timetable.ui')
form_timetable_window = uic.loadUiType(form_timetable)[0]

form_show = resource_path('show_time.ui')
form_show_window = uic.loadUiType(form_show)[0]

form_ranking = resource_path('student_ranking.ui')
form_ranking_window = uic.loadUiType(form_ranking)[0]

form_attendance = resource_path('student_attendance.ui')
form_attendance_window = uic.loadUiType(form_attendance)[0]

form_contribution = resource_path('student_contribution.ui')
form_contribution_window = uic.loadUiType(form_contribution)[0]

form_teacher_attendance = resource_path('teacher_attendance.ui')
form_teacher_attendance_window = uic.loadUiType(form_teacher_attendance)[0]

form_teacher_contribution = resource_path('teacher_contribution.ui')
form_teacher_contribution_window = uic.loadUiType(form_teacher_contribution)[0]

form_teacher_ranking = resource_path('teacher_ranking.ui')
form_teacher_ranking_window = uic.loadUiType(form_teacher_ranking)[0]


class StartWindow(QMainWindow, form_start_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

    def btn_login_clicked(self):
        self.login = LoginWindow()
        self.login.show()
        self.hide()


class LoginWindow(QDialog, QWidget, form_login_window):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_login_clicked(self):
        with open("users.json") as f:
            users = json.load(f)

        name = self.input_name.text()
        pw = self.input_pw.text()
        msg = QMessageBox()

        if name in users:
            if pw == users[name]["pw"]:
                msg.information(self, "Login success", f"{name}님, 환영합니다.")
                self.windowclass = WindowClass(logIn(name))
                self.windowclass.show()
                self.hide()

            else: msg.information(self, "Login failed", "비밀번호를 확인해주세요.")
        else: msg.information(self, "Login failed", "존재하지 않는 사용자입니다.")


# 접속 클래스
class WindowClass(QMainWindow, form_class):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setupUi(self)
        self.show()

    def btn_to_student(self):
        if str(type(self.name)) == "<class '__main__.Student'>":
            self.student = StudentWindow(self.name)
        else:
            msg = QMessageBox()
            msg.information(self, "Access denied", "접근 권한이 없습니다.")

    def btn_to_teacher(self):   # 교수자 DB 만들고 수정할 것
        if user.type == "professor":
            self.teacher = TeacherWindow()
        else:
            msg = QMessageBox()
            msg.information(self, "Access denied", "접근 권한이 없습니다.")


class StudentLoginWindow(QDialog, QWidget, form_student_login_window):
    def __init__(self):
        super(StudentLoginWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def login(self):
        name = self.textEdit.toPlainText()
        if logIn(name):
            self.close()
            self.student = StudentWindow(logIn(name))


# 학습자 클래스
class StudentWindow(QDialog, QWidget, form_student_window):
    def __init__(self, name):
        super(StudentWindow, self).__init__()
        self.name = name
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        self.label_2.setText("Student : %s" % self.name.studentName)
        for team in teamList:
            if self.name in team.teamMembers:
                self.label_3.setText("Team : %s" % team.teamName)
                break

    def btn_main_to_timetable(self):
        self.hide()
        self.timetable = TimetableWindow(self.name)
        self.timetable.exec()
        self.name.matchTime()
        self.show()

    def btn_main_to_show(self):
        self.hide()
        for team in teamList:
            if self.name in team.teamMembers:
                for member in team.teamMembers:
                    self.show_time_table = ShowWindow(member)
                    self.show_time_table.exec()
                self.show_time_table = ShowWindow(team)
                self.show_time_table.exec()
        self.show()

    def btn_main_to_ranking(self):
        self.hide()
        self.ranking = RankingWindow()
        self.ranking.exec()
        self.show()

    def btn_main_to_attendance(self):
        self.hide()
        self.attendance = AttendanceWindow()
        self.attendance.exec()
        self.show()

    def btn_main_to_contribution(self):
        self.hide()
        self.contribution = ContributionWindow()
        self.contribution.exec()
        self.show()

    def add_time(self, time):
        self.name.addTime(time)


class TimetableWindow(QDialog, QWidget, form_timetable_window):
    def __init__(self, name):
        super(TimetableWindow, self).__init__()
        self.name = name
        self.temp = Student("temp")
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_timetable_to_main(self):
        self.close()

    def btn_timetable_to_timetable(self):
        self.name.timeTable = self.temp.timeTable
        self.close()

    def btn_1(self):
        self.pushButton.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 09:00 ~ 10:00")
    def btn_2(self):
        self.pushButton_2.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 10:00 ~ 11:00")
    def btn_3(self):
        self.pushButton_3.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 11:00 ~ 12:00")
    def btn_4(self):
        self.pushButton_4.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 12:00 ~ 13:00")
    def btn_5(self):
        self.pushButton_5.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 13:00 ~ 14:00")
    def btn_6(self):
        self.pushButton_6.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 14:00 ~ 15:00")
    def btn_7(self):
        self.pushButton_7.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 15:00 ~ 16:00")
    def btn_8(self):
        self.pushButton_8.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 16:00 ~ 17:00")
    def btn_9(self):
        self.pushButton_9.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 17:00 ~ 18:00")
    def btn_10(self):
        self.pushButton_10.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 18:00 ~ 19:00")
    def btn_11(self):
        self.pushButton_11.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 19:00 ~ 20:00")
    def btn_12(self):
        self.pushButton_12.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 20:00 ~ 21:00")
    def btn_13(self):
        self.pushButton_13.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 21:00 ~ 22:00")
    def btn_14(self):
        self.pushButton_14.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 22:00 ~ 23:00")
    def btn_15(self):
        self.pushButton_15.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("월 23:00 ~ 24:00")

    def btn_16(self):
        self.pushButton_16.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 09:00 ~ 10:00")
    def btn_17(self):
        self.pushButton_17.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 10:00 ~ 11:00")
    def btn_18(self):
        self.pushButton_18.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 11:00 ~ 12:00")
    def btn_19(self):
        self.pushButton_19.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 12:00 ~ 13:00")
    def btn_20(self):
        self.pushButton_20.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 13:00 ~ 14:00")
    def btn_21(self):
        self.pushButton_21.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 14:00 ~ 15:00")
    def btn_22(self):
        self.pushButton_22.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 15:00 ~ 16:00")
    def btn_23(self):
        self.pushButton_23.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 16:00 ~ 17:00")
    def btn_24(self):
        self.pushButton_24.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 17:00 ~ 18:00")
    def btn_25(self):
        self.pushButton_25.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 18:00 ~ 19:00")
    def btn_26(self):
        self.pushButton_26.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 19:00 ~ 20:00")
    def btn_27(self):
        self.pushButton_27.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 20:00 ~ 21:00")
    def btn_28(self):
        self.pushButton_28.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 21:00 ~ 22:00")
    def btn_29(self):
        self.pushButton_29.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 22:00 ~ 23:00")
    def btn_30(self):
        self.pushButton_30.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("화 23:00 ~ 24:00")

    def btn_31(self):
        self.pushButton_31.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 09:00 ~ 10:00")
    def btn_32(self):
        self.pushButton_32.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 10:00 ~ 11:00")
    def btn_33(self):
        self.pushButton_33.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 11:00 ~ 12:00")
    def btn_34(self):
        self.pushButton_34.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 12:00 ~ 13:00")
    def btn_35(self):
        self.pushButton_35.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 13:00 ~ 14:00")
    def btn_36(self):
        self.pushButton_36.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 14:00 ~ 15:00")
    def btn_37(self):
        self.pushButton_37.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 15:00 ~ 16:00")
    def btn_38(self):
        self.pushButton_38.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 16:00 ~ 17:00")
    def btn_39(self):
        self.pushButton_39.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 17:00 ~ 18:00")
    def btn_40(self):
        self.pushButton_40.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 18:00 ~ 19:00")
    def btn_41(self):
        self.pushButton_41.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 19:00 ~ 20:00")
    def btn_42(self):
        self.pushButton_42.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 20:00 ~ 21:00")
    def btn_43(self):
        self.pushButton_43.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 21:00 ~ 22:00")
    def btn_44(self):
        self.pushButton_44.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 22:00 ~ 23:00")
    def btn_45(self):
        self.pushButton_45.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("수 23:00 ~ 24:00")

    def btn_46(self):
        self.pushButton_46.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 09:00 ~ 10:00")
    def btn_47(self):
        self.pushButton_47.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 10:00 ~ 11:00")
    def btn_48(self):
        self.pushButton_48.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 11:00 ~ 12:00")
    def btn_49(self):
        self.pushButton_49.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 12:00 ~ 13:00")
    def btn_50(self):
        self.pushButton_50.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 13:00 ~ 14:00")
    def btn_51(self):
        self.pushButton_51.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 14:00 ~ 15:00")
    def btn_52(self):
        self.pushButton_52.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 15:00 ~ 16:00")
    def btn_53(self):
        self.pushButton_53.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 16:00 ~ 17:00")
    def btn_54(self):
        self.pushButton_54.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 17:00 ~ 18:00")
    def btn_55(self):
        self.pushButton_55.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 18:00 ~ 19:00")
    def btn_56(self):
        self.pushButton_56.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 19:00 ~ 20:00")
    def btn_57(self):
        self.pushButton_57.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 20:00 ~ 21:00")
    def btn_58(self):
        self.pushButton_58.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 21:00 ~ 22:00")
    def btn_59(self):
        self.pushButton_59.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 22:00 ~ 23:00")
    def btn_60(self):
        self.pushButton_60.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("목 23:00 ~ 24:00")

    def btn_61(self):
        self.pushButton_61.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("금 09:00 ~ 10:00")
    def btn_62(self):
        self.pushButton_62.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("금 10:00 ~ 11:00")
    def btn_63(self):
        self.pushButton_63.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("금 11:00 ~ 12:00")
    def btn_64(self):
        self.pushButton_64.setStyleSheet("background-color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: red;"
                      "border-radius: 3px")
        self.temp.addTime("금 12:00 ~ 13:00")
    def btn_65(self):
        self.pushButton_65.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 13:00 ~ 14:00")
    def btn_66(self):
        self.pushButton_66.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 14:00 ~ 15:00")
    def btn_67(self):
        self.pushButton_67.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 15:00 ~ 16:00")
    def btn_68(self):
        self.pushButton_68.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 16:00 ~ 17:00")
    def btn_69(self):
        self.pushButton_69.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 17:00 ~ 18:00")
    def btn_70(self):
        self.pushButton_70.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 18:00 ~ 19:00")
    def btn_71(self):
        self.pushButton_71.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 19:00 ~ 20:00")
    def btn_72(self):
        self.pushButton_72.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 20:00 ~ 21:00")
    def btn_73(self):
        self.pushButton_73.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 21:00 ~ 22:00")
    def btn_74(self):
        self.pushButton_74.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 22:00 ~ 23:00")
    def btn_75(self):
        self.pushButton_75.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("금 23:00 ~ 24:00")

    def btn_76(self):
        self.pushButton_76.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 09:00 ~ 10:00")
    def btn_77(self):
        self.pushButton_77.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 10:00 ~ 11:00")
    def btn_78(self):
        self.pushButton_78.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 11:00 ~ 12:00")
    def btn_79(self):
        self.pushButton_79.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 12:00 ~ 13:00")
    def btn_80(self):
        self.pushButton_80.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 13:00 ~ 14:00")
    def btn_81(self):
        self.pushButton_81.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 14:00 ~ 15:00")
    def btn_82(self):
        self.pushButton_82.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 15:00 ~ 16:00")
    def btn_83(self):
        self.pushButton_83.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 16:00 ~ 17:00")
    def btn_84(self):
        self.pushButton_84.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 17:00 ~ 18:00")
    def btn_85(self):
        self.pushButton_85.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 18:00 ~ 19:00")
    def btn_86(self):
        self.pushButton_86.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 19:00 ~ 20:00")
    def btn_87(self):
        self.pushButton_87.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 20:00 ~ 21:00")
    def btn_88(self):
        self.pushButton_88.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 21:00 ~ 22:00")
    def btn_89(self):
        self.pushButton_89.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 22:00 ~ 23:00")
    def btn_90(self):
        self.pushButton_90.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("토 23:00 ~ 24:00")

    def btn_91(self):
        self.pushButton_91.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 09:00 ~ 10:00")
    def btn_92(self):
        self.pushButton_92.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 10:00 ~ 11:00")
    def btn_93(self):
        self.pushButton_93.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 11:00 ~ 12:00")
    def btn_94(self):
        self.pushButton_94.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 12:00 ~ 13:00")
    def btn_95(self):
        self.pushButton_95.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 13:00 ~ 14:00")
    def btn_96(self):
        self.pushButton_96.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 14:00 ~ 15:00")
    def btn_97(self):
        self.pushButton_97.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 15:00 ~ 16:00")
    def btn_98(self):
        self.pushButton_98.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 16:00 ~ 17:00")
    def btn_99(self):
        self.pushButton_99.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 17:00 ~ 18:00")
    def btn_100(self):
        self.pushButton_100.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 18:00 ~ 19:00")
    def btn_101(self):
        self.pushButton_101.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 19:00 ~ 20:00")
    def btn_102(self):
        self.pushButton_102.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 20:00 ~ 21:00")
    def btn_103(self):
        self.pushButton_103.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 21:00 ~ 22:00")
    def btn_104(self):
        self.pushButton_104.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 22:00 ~ 23:00")
    def btn_105(self):
        self.pushButton_105.setStyleSheet("background-color: red;"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "border-color: red;"
                                       "border-radius: 3px")
        self.temp.addTime("일 23:00 ~ 24:00")


class ShowWindow(QDialog, QWidget, form_show_window):
    def __init__(self, name):
        super(ShowWindow, self).__init__()
        self.name = name
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        time = ['09:00 ~ 10:00', '10:00 ~ 11:00', '11:00 ~ 12:00', '12:00 ~ 13:00', '13:00 ~ 14:00', '14:00 ~ 15:00', '15:00 ~ 16:00', '16:00 ~ 17:00', '17:00 ~ 18:00', '18:00 ~ 19:00', '19:00 ~ 20:00', '20:00 ~ 21:00', '21:00 ~ 22:00', '22:00 ~ 23:00', '23:00 ~ 24:00']
        day = ['월', '화', '수', '목', '금', '토', '일']

        if str(type(self.name)) == "<class '__main__.Student'>":
            self.label.setText("%s" % self.name.studentName)
        else:
            self.label.setText("<<  %s  >>" % self.name.teamName)
        for i in range(15):
            for j in range(7):
                if self.name.timeTable[day[j]][time[i]] == 1:
                    self.tableWidget.setItem(i, j, QTableWidgetItem())
                    self.tableWidget.item(i, j).setBackground(QtGui.QColor(230, 0, 0))


class RankingWindow(QDialog, QWidget, form_ranking_window):
    def __init__(self):
        super(RankingWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        global teamList

        self.setupUi(self)

        for i in range(9):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(teamList[i].teamName))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(teamList[i].teamScore)))


class AttendanceWindow(QDialog, QWidget, form_attendance_window):
    def __init__(self):
        super(AttendanceWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_attendance_to_main(self):
        self.close()


class ContributionWindow(QDialog, QWidget, form_contribution_window):
    def __init__(self):
        super(ContributionWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_contribution_to_main(self):
        self.close()


# 교수자 클래스
class TeacherWindow(QDialog, QWidget, form_teacher_window):
    def __init__(self):
        super(TeacherWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_main_to_ranking(self):
        self.hide()
        self.ranking = TeacherRankingWindow()
        self.ranking.exec()
        self.show()

    def btn_main_to_attendance(self):
        self.hide()
        self.attendance = TeacherAttendanceWindow()
        self.attendance.exec()
        self.show()

    def btn_main_to_contribution(self):
        self.hide()
        self.contribution = TeacherContributionWindow()
        self.contribution.exec()
        self.show()


class TeacherRankingWindow(QDialog, QWidget, form_teacher_ranking_window):
    def __init__(self):
        super(TeacherRankingWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_ranking_to_main(self):
        self.close()


class TeacherAttendanceWindow(QDialog, QWidget, form_teacher_attendance_window):
    def __init__(self):
        super(TeacherAttendanceWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_attendance_to_main(self):
        self.close()


class TeacherContributionWindow(QDialog, QWidget, form_teacher_contribution_window):
    def __init__(self):
        super(TeacherContributionWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)

    def btn_contribution_to_main(self):
        self.close()


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


def logIn(name):
    for team in teamList:
        for member in team.teamMembers:
            if member.studentName == name:
                return member


def configureDB():
    global teamList
    team1 = Team('건우 없는 건우 팀', 100)
    team2 = Team('B1A3', 100)
    team3 = Team('알리바이', 100)
    team4 = Team('아이즈', 100)
    team5 = Team('조장이 기쁨', 100)
    team6 = Team('재수강은 안 된다', 100)
    team7 = Team('CEPO', 100)
    team8 = Team('한컴', 100)
    team9 = Team('김이강', 100)

    teamList = [team1, team2, team3, team4, team5, team6, team7, team8, team9]
    team1.addTeamMember(['박정수', '안정후', '윤태현'])
    team2.addTeamMember(['박민성', '양동석', '윤세린', '정일묵'])
    team3.addTeamMember(['김지윤', '김회민', '이재림', '임혜림'])
    team4.addTeamMember(['송준영', '이지윤', '정은희', '지윤호'])
    team5.addTeamMember(['김태건', '손동민', '송영민', '이준호'])
    team6.addTeamMember(['권민선', '최예준', '하서현', '한우석'])
    team7.addTeamMember(['김민서', '엄지우', '윤상진', '전혜진'])
    team8.addTeamMember(['송지원', '윤정연', '이수현', '한솔'])
    team9.addTeamMember(['강서현', '김소미', '김은서', '이채영'])


if __name__ == '__main__':
    configureDB()

    app = QApplication(sys.argv)
    myWindow = StartWindow()
    myWindow.show()
    app.exec()
