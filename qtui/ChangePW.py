from bookdb.DbConnection import DbConnection,User
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QMessageBox
)
import hashlib
from bookdb.fun import getResultList

class ChangePw(QWidget):
    def __init__(self,dbc:DbConnection,user:User):
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        self.init_ui()
        
        

    def init_ui(self):
        self.setWindowTitle('修改密码')
        self.setGeometry(300, 300, 300, 150)
        self.resize(400,300)
        self.agopw_label = QLabel('原密码:')
        self.agopw_edit = QLineEdit(self)
        self.agopw_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_label = QLabel('新密码:')
        self.password_edit = QLineEdit(self)
        self.repassword_label = QLabel('重复密码:')
        self.repassword_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.repassword_edit.setEchoMode(QLineEdit.EchoMode.Password)

        
        
        self.register_button=QPushButton('修改',self)
        self.register_button.clicked.connect(self.changepw)
        

        layout = QVBoxLayout(self)
        layout.addWidget(self.agopw_label)
        layout.addWidget(self.agopw_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.repassword_label)
        layout.addWidget(self.repassword_edit)
        layout.addWidget(self.register_button)

    def changepw(self):
        if self.agopw_edit.text().__len__()<=0 \
            or self.repassword_edit.text().__len__()<=0 \
            or self.password_edit.text().__len__()<=0:
            QMessageBox.warning(self,"错误","密码不可为空值")
        elif self.repassword_edit.text()!=self.password_edit.text():
            QMessageBox.warning(self,"错误","两次输入的新密码不相同")
        else:
            cursor=self.dbconnection.cursor()
            sql=f'select passwd from User where user_id={self.user.user_id}'
            cursor.execute(sql)
            rs=cursor.fetchall()
            rsl=getResultList(rs)
            cursor.close()
            if len(rsl)==0:
                QMessageBox.warning(self,"错误","密码错误")
            else:
                result=rsl[0][0]
                if result==hashlib.sha256(self.agopw_edit.text().encode()).hexdigest():
                    passwd=hashlib.sha256(self.password_edit.text().encode()).hexdigest()
                    try:
                        cursor=self.dbconnection.cursor()
                        cursor.execute(f"update User set passwd='{passwd}' \
                                    where user_id={self.user.user_id}")
                        self.dbconnection.connection.commit()
                        QMessageBox.information(self,'成功','修改成功')
                        cursor.close()
                        self.close()
                    except Exception as e:
                        QMessageBox.warning(self,"错误","修改失败")
                else:
                        QMessageBox.warning(self,"错误","密码不正确")


    def show(self) -> None:
        self.agopw_edit.setText('')
        self.password_edit.setText('')
        self.repassword_edit.setText('')
        return super().show()