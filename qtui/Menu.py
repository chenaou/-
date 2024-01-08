import sys
from PyQt6.QtWidgets import QMainWindow, QApplication,QMenuBar,QMenu, QWidget,QVBoxLayout,QMessageBox
from PyQt6.QtGui import QIcon, QAction
from bookdb.DbConnection import DbConnection,User
from ChangePW import ChangePw
from MainWindow import MainWindow
from AddBook import AddBookWidget
from SearchWidget import SearchWidget
from DelBook import DelBook
from ChangeBook import ChangeBook
from BorrowBook import Borrow,BorrowInfo
from ScoreWidget import ScoreWidget
class Menu(QMenuBar):
    def __init__(self, parent: QWidget,dbc:DbConnection,user:User,mainwindow:MainWindow) -> None:
        super().__init__(parent)
        self.dbc=dbc
        self.user=user
        self.mainwindow=mainwindow
        self.init_ui()
    def init_ui(self):
        ##账户菜单
        self.accMenu=self.addMenu('账户')
        # 修改密码
        self.changpw=QAction('修改密码',self)
        self.changpw.setStatusTip('修改密码')
        self.changpw.triggered.connect(self.changepasswd)
        self.accMenu.addAction(self.changpw)
        
        # 退出
        self.exitAct=QAction('退出',self)
        self.exitAct.setStatusTip('退出应用')
        self.exitAct.triggered.connect(QApplication.instance().quit)
        self.accMenu.addAction(self.exitAct)

        if self.user.user_id==0:
            ## 管理菜单
            self.mainMenu=self.addMenu('管理')
            # 添加书籍
            self.addBookAction=QAction('添加书籍')
            self.addBookAction.setStatusTip('添加书籍')
            self.addBookAction.triggered.connect(self.addBook)
            self.mainMenu.addAction(self.addBookAction)
            # 删除书籍
            self.delBookAction=QAction('删除书籍')
            self.delBookAction.setStatusTip('删除书籍')
            self.delBookAction.triggered.connect(self.delBook)
            self.mainMenu.addAction(self.delBookAction)
            # 删除单本书籍
            self.delBookActionS=QAction('删除单本书籍')
            self.delBookActionS.setStatusTip('删除单本书籍')
            self.delBookActionS.triggered.connect(self.delBookS)
            self.mainMenu.addAction(self.delBookActionS)
            # 修改信息
            self.changeAction=QAction('修改书籍信息')
            self.changeAction.setStatusTip('修改书籍信息')
            self.changeAction.triggered.connect(self.changeBookInfo)
            self.mainMenu.addAction(self.changeAction)

        ## 查询菜单
        self.selMenu=self.addMenu('查询')
        # 按作者查询
        self.selAuthor=QAction('按作者')
        self.selAuthor.setStatusTip('按作者查询书籍')
        self.selAuthor.triggered.connect(self.selAuthorBook)
        self.selMenu.addAction(self.selAuthor)
        # 按书名查询（模糊查询）
        self.selBookName=QAction('按书名')
        self.selBookName.setStatusTip('按书名查询书籍')
        self.selBookName.triggered.connect(self.selBook)
        self.selMenu.addAction(self.selBookName)

        # 查找具体书籍
        self.selBookNameP=QAction('查找具体书籍')
        self.selBookNameP.setStatusTip('查找到具体的某一本书')
        self.selBookNameP.triggered.connect(self.selBookP)
        self.selMenu.addAction(self.selBookNameP)

        


        ## 借还书
        self.borMenu=self.addMenu('借阅')
        # 借书
        self.borBook=QAction('借书')
        self.borBook.setStatusTip('借书')
        self.borBook.triggered.connect(self.borrowBook)
        self.borMenu.addAction(self.borBook)
        # 还书
        self.retBook=QAction('还书')
        self.retBook.setStatusTip('还书')
        self.retBook.triggered.connect(self.returnBook)
        self.borMenu.addAction(self.retBook)
        # 借书信息
        self.bowInfo=QAction('借阅信息')
        self.bowInfo.setStatusTip('借阅信息')
        self.bowInfo.triggered.connect(self.bowInfoAction)
        self.borMenu.addAction(self.bowInfo)

        # 评分
        self.scoreMenu=self.addMenu('评分')
        self.scoreAction=QAction('评分')
        self.scoreAction.setStatusTip('评分')
        self.scoreAction.triggered.connect(self.scoreBook)
        self.scoreMenu.addAction(self.scoreAction)



        


    def changepasswd(self):
        if self.user.user_id==0:
            QMessageBox.warning(self,'错误','请联系数据库管理员修改管理员密码')
        else:
            self.changeWindow=ChangePw(self.dbc,self.user)
            self.changeWindow.show()


    def addBook(self):
        self.addBookwidget=AddBookWidget(dbc=self.dbc,user=self.user)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.addBookwidget
        self.mainwindow.vbox.addWidget(self.addBookwidget)
        self.addBookwidget.show()
    def delBook(self):
        self.delWindow=DelBook(self.dbc,self.user,1)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.delWindow
        self.mainwindow.vbox.addWidget(self.delWindow)
        self.delWindow.show()
    def delBookS(self):
        self.delWindow=DelBook(self.dbc,self.user,2)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.delWindow
        self.mainwindow.vbox.addWidget(self.delWindow)
        self.delWindow.show()
    def selAuthorBook(self):
        self.searchWindow=SearchWidget(self.dbc,self.user,1)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.searchWindow
        self.mainwindow.vbox.addWidget(self.searchWindow)
        self.searchWindow.show()
    def selBook(self):
        self.searchWindow=SearchWidget(self.dbc,self.user,2)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.searchWindow
        self.mainwindow.vbox.addWidget(self.searchWindow)
        self.searchWindow.show()
    def selBookP(self):
        self.searchWindow=SearchWidget(self.dbc,self.user,3)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.searchWindow
        self.mainwindow.vbox.addWidget(self.searchWindow)
        self.searchWindow.show()
    def changeBookInfo(self):
        self.changeInfoWindow=ChangeBook(self.dbc,self.user)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.changeInfoWindow
        self.mainwindow.vbox.addWidget(self.changeInfoWindow)
        self.changeInfoWindow.show()

    def borrowBook(self):
        self.borrowWindow=Borrow(self.dbc,self.user,1)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.borrowWindow
        self.mainwindow.vbox.addWidget(self.borrowWindow)
        self.borrowWindow.show()
    def returnBook(self):
        self.borrowWindow=Borrow(self.dbc,self.user,2)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.borrowWindow
        self.mainwindow.vbox.addWidget(self.borrowWindow)
        self.borrowWindow.show()

    def bowInfoAction(self):
        self.bowInfoWindow=BorrowInfo(self.dbc,self.user)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.bowInfoWindow
        self.mainwindow.vbox.addWidget(self.bowInfoWindow)
        self.bowInfoWindow.show()
    def scoreBook(self):
        self.scoreWindow=ScoreWidget(self.dbc,self.user)
        self.mainwindow.tmpWidget.close()
        self.mainwindow.tmpWidget=self.scoreWindow
        self.mainwindow.vbox.addWidget(self.scoreWindow)
        self.scoreWindow.show()