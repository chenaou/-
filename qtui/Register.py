import sys
from bookdb.DbConnection import DbConnection
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QMessageBox
)
import hashlib

class RegisterWindow(QWidget):
    def __init__(self,dbc:DbConnection):
        super().__init__()
        self.init_ui()
        self.dbconnection=dbc
        

    def init_ui(self):
        self.setWindowTitle('注册')
        self.setGeometry(300, 300, 300, 150)
        self.resize(400,300)
        self.username_label = QLabel('用户名:')
        self.username_edit = QLineEdit(self)

        self.password_label = QLabel('密码:')
        self.password_edit = QLineEdit(self)
        self.repassword_label = QLabel('重复密码:')
        self.repassword_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.repassword_edit.setEchoMode(QLineEdit.EchoMode.Password)


        
        self.register_button=QPushButton('注册',self)
        self.register_button.clicked.connect(self.register)
        

        layout = QVBoxLayout(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.repassword_label)
        layout.addWidget(self.repassword_edit)
        layout.addWidget(self.register_button)

    def register(self):
        if len(self.username_edit.text())<=0 and \
            len(self.password_edit.text())<=0 and \
            len(self.repassword_edit.text())<=0:
            QMessageBox.warning(self,"错误","用户名和密码不能为空")
        elif self.password_edit.text()!=self.repassword_edit.text():
            QMessageBox.warning(self,"错误","两次输入的密码不相同")
        else:
            cursor=self.dbconnection.connection.cursor()
            name=self.username_edit.text()
            passwd=hashlib.sha256(self.password_edit.text().encode()).hexdigest()
            sql=f"insert into User ( user_name, user_type, passwd) values ('{name}',1,'{passwd}')"
            try:
                cursor.execute(sql)
                self.dbconnection.connection.commit()
                QMessageBox.information(self,"注册成功","注册成功")
            except Exception as e:
                print(e)
                QMessageBox.warning(self,"错误","注册失败，该用户可能存在")
            finally:
                cursor.close()