import sys
import json
import os


from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextBrowser, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup


from models.User import Student, Professor
from models.Group import Team


# class 선택단추(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.UI초기화()
#
#     def UI초기화(self):
#         rbtn = QRadioButton(self)
#         rbtn.setText('라디오 버튼1')
#         rbtn.move(60, 50)
#
#         rbtn_2 = QRadioButton('라디오 버튼2', self)
#         rbtn_2.move(60, 80)
#         rbtn_2.setChecked(True)
#
#         rbtn_3 = QRadioButton('라디오 버튼3', self)
#         rbtn_3.move(60, 110)
#         rbtn_3.setAutoExclusive(True)
#
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('QRadioButton')
#         self.show()


class memo(QWidget):

    def __init__(self):
        super().__init__()
        self.UI초기화()

    def UI초기화(self):

        self.line_edit = QLineEdit(self)
        self.line_edit.returnPressed.connect(self.addText)

        self.btn_add = QPushButton('입력')
        self.btn_add.clicked.connect(self.addText)

        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        ## 여기 DB에서 불러오면 될듯!
        self.tb.append('- XX월 XX일 XX시 XX분 XX초 ~ XX월 XX일 XX시 XX분 XX초 회의 진행\n')
        self.tb.append('- 출석 >> 김:O , 송 : X\n')

        self.btn_clear = QPushButton('전체 지우기')
        self.btn_clear.clicked.connect(self.clearText)

        self.btn_print = QPushButton('저장')
        self.btn_print.clicked.connect(self.save_tb)

        vbox = QVBoxLayout()

        vbox.addWidget(self.tb)
        vbox.addWidget(self.line_edit)
        vbox.addWidget(self.btn_add)
        vbox.addWidget(self.btn_clear)
        vbox.addWidget(self.btn_print)


        self.setLayout(vbox)
        self.setWindowTitle('메모장')
        self.setGeometry(300, 300, 300, 500)
        self.show()

    def addText(self):
        text = self.line_edit.text()
        self.tb.append(text)
        self.line_edit.clear()

    def clearText(self):
        self.tb.clear()

    ## print all tb
    def save_tb(self):
        ## 여기서 DB에 저장하면 될듯!
        print(self.tb.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = memo()

    sys.exit(app.exec())