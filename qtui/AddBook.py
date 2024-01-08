from PyQt6.QtCore import Qt
from bookdb.DbConnection import DbConnection,User
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout,QMessageBox,QSpacerItem,
    QSizePolicy,
)
import hashlib
from bookdb.fun import getResultList


class AddBookWidget(QWidget):
    def __init__(self,dbc:DbConnection,user:User) -> None:
        super().__init__()
        self.dbconnection=dbc
        self.user=user

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('修改密码')

        ## 控件
        self.nameLabel=QLabel('书名：')
        self.nameEdit=QLineEdit(self)
        self.authLabel=QLabel('作者名：')
        self.authEdit=QLineEdit(self)
        self.publishLabel=QLabel('出版社名：')
        self.publishEdit=QLineEdit(self)
        self.countLabel=QLabel('数量')
        self.countEdit=QLineEdit(self)

        self.addButton=QPushButton('添加',self)
        self.addButton.clicked.connect(self.addBookAct)



        self.vbox=QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setSpacing(5)
        ## 添加
        self.vbox.addWidget(self.nameLabel)
        self.vbox.addWidget(self.nameEdit)
        self.vbox.addWidget(self.authLabel)
        self.vbox.addWidget(self.authEdit)
        self.vbox.addWidget(self.publishLabel)
        self.vbox.addWidget(self.publishEdit)
        self.vbox.addWidget(self.countLabel)
        self.vbox.addWidget(self.countEdit)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vbox.addItem(spacerItem)
        self.vbox.addWidget(self.addButton)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vbox.addItem(spacerItem1)

    def addBookAct(self):
        ##向书籍信息表中添加数据
        cursor=self.dbconnection.cursor()
        authorName=self.authEdit.text()
        bookName=self.nameEdit.text()
        publishName=self.publishEdit.text()
        count=0
        try:
            count=int(self.countEdit.text())
        except ValueError as ve:
            QMessageBox.warning(self,'错误','数量应为数字')
            return
        if count<=0 :
            QMessageBox.warning(self,'错误','数量不可为0或者负数')
            return
        if len(bookName)==0 or len(authorName)==0 or len(publishName)==0:
            QMessageBox.warning(self,'错误','不可为空')
            return
        '''select book_info_id from BookInfo where book_name='' and  author='' and publish_house='' '''
        sql_sl=f"select book_info_id from BookInfo where \
                book_name='{bookName}' and  author='{authorName}' and publish_house='{publishName}'"
        try:
            cursor.execute(sql_sl)
            rel=getResultList(cursor.fetchall())
            if len(rel)==0:##没有此书
                pass
            else:
                self.addSomeBook(count,sql_sl)
                self.authEdit.setText('')
                self.nameEdit.setText('')
                self.countEdit.setText('')
                self.publishEdit.setText('')
                QMessageBox.information(self,'成功','添加完毕')
                cursor.close()
                return
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'错误','添加失败')
            return cursor.close()
        try:
            cursor=self.dbconnection.cursor()
            sql=f"insert into BookInfo \
                (author, book_name, publish_house) \
                values ('{authorName}','{bookName}','{publishName}')"
            cursor.execute(sql)
            self.dbconnection.connection.commit()
        except Exception as e:
            QMessageBox.warning(self,'错误','添加失败')
            print(e)
            return cursor.close()
        finally:
            cursor.close()
        self.addSomeBook(count,sql_sl)
        self.authEdit.setText('')
        self.nameEdit.setText('')
        self.countEdit.setText('')
        self.publishEdit.setText('')
        QMessageBox.information(self,'成功','添加完毕')
        
    def addSomeBook(self,count:int,sql_sl:str):
        cursor=self.dbconnection.connection.cursor()
        id:int=-1
        try:
            cursor.execute(sql_sl)
            rel=getResultList(cursor.fetchall())
            if len(rel)==0:##没有此书
                QMessageBox.warning(self,'错误','找不到书籍')
                return cursor.close()
            else:
                id=rel[0][0]
        except Exception as e:
            QMessageBox.warning(self,'错误','添加出错')
            return cursor.close()
        finally:
            cursor.close()
        sql="insert into Book (book_info_id) values"
        cursor=self.dbconnection.connection.cursor()
        for i in range(count):
            sql+=f"({id}),"
        sql=sql[:-1]
        try:
            cursor.execute(sql)
            self.dbconnection.connection.commit()
            cursor.execute(f'update BookInfo set book_amounts=book_amounts+{count} \
                            where book_info_id={id}')
            self.dbconnection.connection.commit()
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'错误','添加出错')
            return cursor.close()
        finally:
            cursor.close()
        
            
            