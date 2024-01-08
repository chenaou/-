from PyQt6.QtCore import Qt
from bookdb.DbConnection import DbConnection,User
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout,QMessageBox,QSpacerItem,
    QSizePolicy,
)
import hashlib
from bookdb.fun import getResultList
class DelBook(QWidget):
    def __init__(self,dbc:DbConnection,user:User,delType:int):
        super().__init__()
        self.dbconnection=dbc
        self.delType=delType
        self.user=user
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('删除书籍')

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.label=QLabel(self)
        if self.delType==1:
            self.label.setText('书籍id:')
        elif self.delType==2:
            self.label.setText('书籍编号:')
        else:
            QMessageBox.warning(self,'错误','类型异常')
            return
        self.idEdit=QLineEdit(self)
        self.delButton=QPushButton('删除')
        self.delButton.clicked.connect(self.delAction)
        layout.addWidget(self.label)
        layout.addWidget(self.idEdit)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacerItem)
        layout.addWidget(self.delButton)
    def delAction(self):
        if self.idEdit.text().__len__()==0:
            QMessageBox.warning(self,'错误','id不可为空')
        id=0
        try:
            id=int(self.idEdit.text())
        except ValueError:
            QMessageBox.warning(self,'错误','id应为数字')
            return
        sql=''
        if self.delType==1:
            sql=f"delete from BookInfo where book_info_id={id}"
        elif self.delType==2:
            sql=f"call delDetailBook({id})"
        else:
            QMessageBox.warning(self,'错误','类型异常')
            return
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(sql)
            self.dbconnection.connection.commit()
            QMessageBox.information(self,'成功','删除成功')
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'错误','删除失败')
            self.idEdit.setText('')
            return cursor.close()
        finally:
            cursor.close()
            self.idEdit.setText('')

        
        