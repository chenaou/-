from PyQt6.QtCore import Qt
from bookdb.DbConnection import DbConnection,User
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout,QMessageBox,QSpacerItem,
    QSizePolicy,QTableWidget,QTableWidgetItem
)
import hashlib
from bookdb.fun import getResultList

class Borrow(QWidget):
    def __init__(self,dbc:DbConnection,user:User,actType:int):
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        self.isSure=False
        self.actType=actType
        self.isBorrowed=True
        self.bookId=-1
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.label=QLabel(self)
        if self.actType==1:##借书
            self.label.setText('待借取书籍id:')
        else:
            self.label.setText('待归还书籍id:')
        self.idEdit=QLineEdit(self)
        self.sureButton=QPushButton('确认')
        self.sureButton.clicked.connect(self.makeSure)

        self.infoLabel=QLabel('\n\n\n\n\n\n')

        self.borrowButton=QPushButton(self)
        if self.actType==1:##借书
            self.borrowButton.setText('借取')
            self.borrowButton.clicked.connect(self.borrowAction)
        else:
            self.borrowButton.setText('归还')
            self.borrowButton.clicked.connect(self.returnAction)

        layout.addWidget(self.label)
        layout.addWidget(self.idEdit)
        layout.addWidget(self.sureButton)
        layout.addWidget(self.infoLabel)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacerItem)
        layout.addWidget(self.borrowButton)

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
        sql=f"select infoid,book_id,book_name,author,\
            publish_house,is_borrowed from DetailBookInfo where book_id={id};"
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(sql)
            rsl=getResultList(cursor.fetchall())
            if len(rsl)==0:
                QMessageBox.information(self,'提示','找不到此书籍，无法确认')
            else:
                information=f"\
                书籍id:{rsl[0][0]}\n \
                书籍编号:{rsl[0][1]}\n \
                书籍名:{rsl[0][2]}\n \
                作者:{rsl[0][3]}\n \
                出版社:{rsl[0][4]}\n \
                是否借出:{rsl[0][5]}\n \
                "
                self.bookId=int(rsl[0][1])
                self.infoLabel.setText(information)
                self.isBorrowed=(rsl[0][5]=='是')
                self.isSure=True
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'异常',' 查询失败')
            self.isSure=False
            return cursor.close()
        finally:
            cursor.close()
    def borrowAction(self):
        if self.isSure==False or self.bookId==-1:
            QMessageBox.warning(self,'异常','请先确认')
            return
        sql=''
        if self.isBorrowed==True:
            QMessageBox.warning(self,'错误','你所确认的书籍已经被借出了')
            return
        else:
            sql=f"call borrowBook({self.bookId},{self.user.user_id})"
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(sql)
            self.dbconnection.connection.commit()
            QMessageBox.information(self,'成功','借阅成功')
            self.bookId=-1
            self.isBorrowed=False
            self.idEdit.setText('')
            self.isSure=False
            self.infoLabel.setText('\n\n\n\n\n\n')
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'错误','请保证确认后的书籍编号未被修改')
            return cursor.close()
        finally:
            cursor.close()

    def returnAction(self):
        if self.isSure==False or self.bookId==-1:
            QMessageBox.warning(self,'异常','请先确认')
            return
        
        if self.isBorrowed==False:
            QMessageBox.warning(self,'错误','你所确认的书籍尚未被借出')
            return
        selSql=f"select user_id from Borrow where book_id={self.bookId}"
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(selSql)
            rsl=getResultList(cursor.fetchall())
            if len(rsl)==0:
                QMessageBox.warning(self,'错误','你所确认的书籍尚未被借出')
                return cursor.close()
            elif rsl[0][0]!=self.user.user_id:
                QMessageBox.warning(self,'错误','你不能归还别人借的书')
                return cursor.close()
            else:## 还书
                retSQl=f"call returnBook({self.bookId},{self.user.user_id})"
                cursor.close()
                cursor=self.dbconnection.cursor()
                cursor.execute(retSQl)
                self.dbconnection.connection.commit()
                QMessageBox.information(self,'成功','归还成功')
                self.bookId=-1
                self.isBorrowed=False
                self.idEdit.setText('')
                self.isSure=False
                self.infoLabel.setText('\n\n\n\n\n\n')
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'错误','请保证确认后的书籍编号未被修改')
            return cursor.close()
        finally:
            cursor.close()

class BorrowInfo(QWidget):
    def __init__(self,dbc:DbConnection,user:User):
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        
        self.init_ui()
    def init_ui(self):
        layout=QVBoxLayout()
        self.setLayout(layout)
        sql=''
        if self.user.user_id==0:
            sql=f"select user_name,bookId,book_name,author,publish_house from BorrowInfo"
        else:
            sql=f"select user_name,bookId,book_name,author,publish_house \
                  from BorrowInfo where user_name={self.user.user_name}"
        cursor=self.dbconnection.cursor()
        rsl=[]
        try:
            cursor.execute(sql)
            rsl=getResultList(cursor.fetchall())
            print('查询完毕')
        except Exception as e:
            QMessageBox.warning(self,'错误','查询失败')
            return cursor.close()
        finally:
            cursor.close()
        if len(rsl)==0:
            QMessageBox.information(self,'提示','未借阅任何书籍')
            return
        self.rsTable=QTableWidget(len(rsl),len(rsl[0]),self)
        for i in range(len(rsl)):
            for j in range(len(rsl[0])):    
                self.rsTable.setItem(i, j, QTableWidgetItem(f'{rsl[i][j]}'))
        self.rsTable.resizeColumnsToContents()
        self.rsTable.setHorizontalHeaderItem(0,QTableWidgetItem('用户名'))
        self.rsTable.setHorizontalHeaderItem(1,QTableWidgetItem('书籍号'))
        self.rsTable.setHorizontalHeaderItem(2,QTableWidgetItem('书名'))
        self.rsTable.setHorizontalHeaderItem(3,QTableWidgetItem('作者'))
        self.rsTable.setHorizontalHeaderItem(4,QTableWidgetItem('出版社'))
        layout.addWidget(self.rsTable)

