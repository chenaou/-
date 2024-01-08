from PyQt6.QtCore import Qt
from bookdb.DbConnection import DbConnection,User
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout,QMessageBox,QSpacerItem,
    QSizePolicy,
)
import hashlib
from bookdb.fun import getResultList

class ChangeBook(QWidget):
    def __init__(self,dbc:DbConnection,user:User):
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        self.isSure=False
        self.bookInfoId=-1
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.label=QLabel(self)
        self.label.setText('待修改书籍id:')
        self.idEdit=QLineEdit(self)
        self.sureButton=QPushButton('确认')
        self.sureButton.clicked.connect(self.makeSure)
        self.nameLabel=QLabel('书籍名:')
        self.nameEdit=QLineEdit(self)
        self.authorLabel=QLabel('作者:')
        self.authorEdit=QLineEdit(self)
        self.publishLabel=QLabel('出版社')
        self.publishEdit=QLineEdit(self)
        self.changeButton=QPushButton('修改')
        self.changeButton.clicked.connect(self.change)
        ## 添加到widget
        layout.addWidget(self.label)
        layout.addWidget(self.idEdit)
        layout.addWidget(self.sureButton)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameEdit)
        layout.addWidget(self.authorLabel)
        layout.addWidget(self.authorEdit)
        layout.addWidget(self.publishLabel)
        layout.addWidget(self.publishEdit)
        layout.addWidget(self.changeButton)
    def makeSure(self):
        if self.idEdit.text().__len__()==0:
            QMessageBox.warning(self,'错误','id不可为空')
            return
        id=0
        try:
            id=int(self.idEdit.text())
        except ValueError:
            QMessageBox.warning(self,'错误','id应为数字')
            return
        sql=f"select book_name,author,publish_house from BookInfo where book_info_id={id}"
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(sql)
            rsl=getResultList(cursor.fetchall())
            if len(rsl)==0:
                QMessageBox.information(self,'提示','找不到此书籍，无法确认')
            else:
                self.nameEdit.setText(rsl[0][0])
                self.authorEdit.setText(rsl[0][1])
                self.publishEdit.setText(rsl[0][2])
                self.bookInfoId=id
                self.isSure=True
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'异常',' 查询失败')
            self.isSure=False
            return cursor.close()
        finally:
            cursor.close()

    def change(self):
        if self.isSure==False or self.bookInfoId==-1:
            QMessageBox.warning(self,'异常','请先确认')
            return
        book_name=self.nameEdit.text()
        author=self.authorEdit.text()
        publish_name=self.publishEdit.text()
        sql=f"update BookInfo set book_name='{book_name}',author='{author}',\
            publish_house='{publish_name}' where book_info_id={self.bookInfoId}"
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(sql)
            self.dbconnection.connection.commit()
            QMessageBox.information(self,'成功','修改成功')
            self.idEdit.setText('')
            self.nameEdit.setText('')
            self.authorEdit.setText('')
            self.publishEdit.setText('')
            self.bookInfoId=-1
            self.isSure=False
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'错误','修改失败')
            return cursor.close()
        finally:
            cursor.close()