import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
import pymysql


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        username = self.email.text()
        password = self.password.text()
        # database connect
        conn = pymysql.connect(host="", user="", passwd="", database="")
        cur = conn.cursor()
        sql = '''select username,password from #table where username=%s and password=%s'''
        data = (username, password)
        cur.execute(sql, data)
        re = cur.fetchall()
        if len(re) > 0:
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Successfully logged in")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Incorrect Username or Password")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

    def gotocreate(self):
        Adminacc = AdminAcc()
        widget.addWidget(Adminacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AdminAcc(QDialog):
    def __init__(self):
        super(AdminAcc, self).__init__()
        loadUi("admin.ui", self)
        self.loginbutton.clicked.connect(self.adminfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def adminfunction(self):
        username = self.email.text()
        password = self.password.text()
        # database connect
        conn = pymysql.connect(host="", user="", passwd="", database="")
        cur1 = conn.cursor()
        query = "select * from #table where username=%s and password=%s"
        data = cur1.execute(query, (username, password))
        #username redudancy check
        if data > 0:
            return (self.gotocreate1())
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Incorrect Username or Password")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

    def gotocreate1(self):
        Createacc = CreateAcc()
        widget.addWidget(Createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        un = self.email.text()
        # database connect
        conn = pymysql.connect(host="", user="", passwd="", database="")
        cur1 = conn.cursor()
        query = "select * from #admintable where username=%s"
        data = cur1.execute(query, (un))
        #username redudancy check
        if data > 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Enter Valid ID")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            username = self.email.text()
        #password redudancy check
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Enter Correct Password")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

        idn = self.id.text()
        cur2 = conn.cursor()
        query = "select * from #table where id=%s"
        data = cur2.execute(query, (idn))
        #id redudancy check
        if data > 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Enter Valid ID")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            id = self.id.text()

        cur3 = conn.cursor()
        query = "INSERT INTO student(username,id,password) VALUES(%s,%s,%s)"
        value = (username, id, password)
        cur3.execute(query, value)
        conn.commit()
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("User added successfully")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
        return (self.gotocreate2())

    def gotocreate2(self):
        loginre = Login()
        widget.addWidget(loginre)
        widget.setCurrentIndex(widget.currentIndex() + 1)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()
