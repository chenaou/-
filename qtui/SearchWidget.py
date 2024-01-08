from PyQt6.QtCore import Qt
from bookdb.DbConnection import DbConnection,User
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout,QMessageBox,QSpacerItem,
    QSizePolicy,QTableWidget,QTableWidgetItem
)
import hashlib
from bookdb.fun import getResultList


class SearchWidget(QWidget):
    def __init__(self,dbc:DbConnection,user:User,serType:int) -> None:
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        self.serType=serType
        self.init_ui()
    def init_ui(self):
        self.vbox=QVBoxLayout()
        self.setLayout(self.vbox)

        self.smVbox=QVBoxLayout()
        self.lowVbox=QVBoxLayout()
        ## 搜索框
        if self.serType==1:
            self.serLabel=QLabel('作者名：')
        else:
            self.serLabel=QLabel('书籍名：')
        self.serEdit=QLineEdit(self)
        self.smVbox.addWidget(self.serLabel)
        self.smVbox.addWidget(self.serEdit)
        self.vbox.addLayout(self.smVbox)
        self.vbox.addLayout(self.lowVbox)

        self.searchButton=QPushButton('查询')
        self.searchButton.clicked.connect(self.search)
        self.smVbox.addWidget(self.searchButton)
        ## 结果展示
        self.rsTable:QTableWidget=QTableWidget()

        self.lowVbox.addWidget(self.rsTable)

    def search(self):
        sql=''
        if self.serType==1:
            sql=f"select book_info_id,book_name,author,publish_house,\
            book_amounts,book_score from BookInfo where author='{self.serEdit.text()}'"
        elif self.serType==2:
            sql=f"select book_info_id,book_name,author,publish_house,\
                book_amounts,book_score from BookInfo where book_name like '%{self.serEdit.text()}%';"
        elif self.serType==3:
            sql=f"select infoid,book_id,book_name,author,\
           publish_house,book_amounts,book_score,is_borrowed from DetailBookInfo \
            where book_name like '%{self.serEdit.text()}%'"
        else:
            QMessageBox.warning(self,'错误','类型异常')
            return
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
        print(rsl)
        if len(rsl)==0:
            QMessageBox.warning(self,'错误','找不到书籍')
        else:
            self.rsTable.close()
            self.rsTable=QTableWidget(len(rsl),len(rsl[0]),self)
            
            for i in range(len(rsl)):
                for j in range(len(rsl[0])):
                    if rsl[i][j]==None:
                        self.rsTable.setItem(i, j, QTableWidgetItem('暂无'))
                    else:
                        self.rsTable.setItem(i, j, QTableWidgetItem(f'{rsl[i][j]}'))
            self.rsTable.resizeColumnsToContents()
            index=0
            self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('id'));index+=1
            if self.serType==3:
                self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('书籍号'));index+=1
            self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('书名'));index+=1
            self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('作者'));index+=1
            self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('出版社'));index+=1
            self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('数量'));index+=1
            self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('评分'));index+=1
            if self.serType==3:
                self.rsTable.setHorizontalHeaderItem(index,QTableWidgetItem('是否借出'));index+=1
            self.lowVbox.addWidget(self.rsTable)
            self.rsTable.show()




            