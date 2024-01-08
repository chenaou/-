import sys
from bookdb.DbConnection import DbConnection,User
from bookdb.fun import getResultList
import hashlib
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QMessageBox
)
from MainWindow import MainWindow
from Register import RegisterWindow
from Menu import Menu
class LoginWindow(QWidget):
    def __init__(self,dbc:DbConnection,user:User,mainwindow:MainWindow):
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        self.mainwinodw=mainwindow
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('登录')
        self.setGeometry(300, 300, 300, 150)
        self.resize(400,300)
        self.username_label = QLabel('用户名:')
        self.username_edit = QLineEdit(self)

        self.password_label = QLabel('密码:')
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('登录', self)
        self.login_button.clicked.connect(self.login)
        self.register_button=QPushButton('注册',self)
        self.register_button.clicked.connect(self.registerui)
        self.reg=RegisterWindow(dbc=self.dbconnection)
        self.reg.move(self.x()+20,self.y()+20)
        layout = QVBoxLayout(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

    def login(self):
        if self.dbconnection.is_connected==False:
            QMessageBox.warning(self,"数据库似乎没有连接")
        else:
            cursor=self.dbconnection.cursor()
            sql=f'select passwd from User where user_name=\'{self.username_edit.text()}\''
            cursor.execute(sql)
            rs=cursor.fetchall()
            rsl=getResultList(rs)
            cursor.close()
            if len(rsl)==0:
                QMessageBox.warning(self,"登陆失败","用户名或者密码不正确")
            else:
                result=rsl[0][0]
                if result==hashlib.sha256(self.password_edit.text().encode()).hexdigest():
                    cursor=self.dbconnection.cursor()
                    cursor.execute(f"select user_id,user_name,user_type \
                                   from User where user_name='{self.username_edit.text()}'")
                    rsl=getResultList(cursor.fetchall())
                    if len(rsl)!=1:
                        QMessageBox.warning(self,"登陆失败","用户名或者密码不正确")
                    else:
                        self.user.user_id=rsl[0][0]
                        self.user.user_name=rsl[0][1]
                        self.user.user_type=rsl[0][2]
                        self.user.is_login=True
                        self.mainwinodw=MainWindow(dbc=self.dbconnection,user=self.user)
                        self.menuBar=Menu(parent=self.mainwinodw,dbc=self.dbconnection,
                                          user=self.user,mainwindow=self.mainwinodw)
                        self.mainwinodw.setMenuBar(self.menuBar)
                        self.mainwinodw.show()
                        
                        self.close()

                else:
                    QMessageBox.warning(self,"登陆失败","用户名或者密码不正确")
            
    def registerui(self):
        if self.reg.isHidden()==False:
            self.reg.hide()
        else:
            self.reg.show()
        


