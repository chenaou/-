from PyQt6.QtCore import Qt
from bookdb.DbConnection import DbConnection,User
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout,QMessageBox,QSpacerItem,
    QSizePolicy,QTableWidget,QTableWidgetItem
)
import hashlib
from bookdb.fun import getResultList

class ScoreWidget(QWidget):
    def __init__(self,dbc:DbConnection,user:User,):
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        self.isSure=False
        self.bookId=-1
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.label=QLabel('待评价书籍id:')

        
        self.idEdit=QLineEdit(self)
        self.sureButton=QPushButton('确认')
        self.sureButton.clicked.connect(self.makeSure)

        self.infoLabel=QLabel('\n\n\n\n\n')
        self.scoreButton=QPushButton('添加评分')
        self.scoreLabel=QLabel('评分：')
        self.scoreEdit=QLineEdit(self)
        

        self.scoreButton.clicked.connect(self.scoreAction)

        layout.addWidget(self.label)
        layout.addWidget(self.idEdit)
        layout.addWidget(self.sureButton)
        layout.addWidget(self.infoLabel)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacerItem)
        
        layout.addWidget(self.scoreLabel)
        layout.addWidget(self.scoreEdit)


        layout.addWidget(self.scoreButton)

        

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
        sql=f"select book_info_id,book_name,author,publish_house, \
            book_score from BookInfo where book_info_id={id}"
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(sql)
            rsl=getResultList(cursor.fetchall())
            if len(rsl)==0:
                QMessageBox.information(self,'提示','找不到此书籍，无法确认')
            else:
                information=f"\
                书籍id:{rsl[0][0]}\n \
                书籍名:{rsl[0][1]}\n \
                作者:{rsl[0][2]}\n \
                出版社:{rsl[0][3]}\n \
                评分:{rsl[0][4]}\n \
                "
                self.bookId=int(rsl[0][0])
                self.infoLabel.setText(information)
                self.isSure=True
        except Exception as e:
            print(e)
            QMessageBox.warning(self,'异常',' 查询失败')
            self.isSure=False
            return cursor.close()
        finally:
            cursor.close()
    def scoreAction(self):
        isInsert=False
        isUpdate=False
        if self.isSure==False or self.bookId==-1:
            QMessageBox.warning(self,'异常','请先确认')
            return
        if self.scoreEdit.text().__len__()==0:
            QMessageBox.warning(self,'错误','id不可为空')
            return
        score=0
        try:
            score=int(self.scoreEdit.text())
        except ValueError:
            QMessageBox.warning(self,'错误','score应为数字')
            return
        if score>10 or score<0:
            QMessageBox.warning(self,'错误','评分在0~10之间')
            return
        insertSql=f"insert into Evaluation (user_id, book_info_id, scores) \
              values ({self.user.user_id},{self.bookId},{score})"
        updateSql=f"update Evaluation set scores={score} \
            where book_info_id={self.bookId} and user_id={self.user.user_id}"
        ## 添加新评分
        cursor=self.dbconnection.cursor()
        
        try:
            cursor.execute(insertSql)
            self.dbconnection.connection.commit()
            QMessageBox.information(self,'成功','添加评分成功')
            self.idEdit.setText('')
            self.scoreEdit.setText('')
            self.infoLabel.setText('\n\n\n\n\n')
            isInsert=True
            print(isInsert)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        if isInsert==True:
            return
        cursor=self.dbconnection.cursor()
        try:
            cursor.execute(updateSql)
            self.dbconnection.connection.commit()
            QMessageBox.information(self,'成功','修改评分成功')
            self.idEdit.setText('')
            self.scoreEdit.setText('')
            self.infoLabel.setText('\n\n\n\n\n')
            isUpdate=True
            print(isUpdate)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        if isInsert==False and isUpdate==False:
            QMessageBox.warning(self,'失败','评分失败')
        
