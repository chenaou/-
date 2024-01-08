from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget,QVBoxLayout,QLabel,QHBoxLayout
from bookdb.DbConnection import DbConnection,User


class MainWindow(QMainWindow):
    def __init__(self,dbc:DbConnection,user:User) -> None:
        super().__init__()
        self.dbconnection=dbc
        self.user=user
        self.init_ui()
    
    def init_ui(self):
        self.vbox=QVBoxLayout()
        centralWidget=QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(self.vbox)
        self.resize(800,600)
        self.setWindowTitle('图书管理系统')
        self.tmpWidget:QWidget=None

        helloWidget=HelloWidget(parent=self.centralWidget(),user=self.user)
        self.tmpWidget=helloWidget
        self.vbox.addWidget(self.tmpWidget)
        

class HelloWidget(QWidget):
    def __init__(self, parent: QWidget,user:User) -> None:
        super().__init__(parent=parent)
        self.user=user
        self.init_ui()
    def init_ui(self):
        hbox=QHBoxLayout(self)
        self.helloLabel=QLabel()
        self.helloLabel.setText(f'你好，{self.user.user_name}')
        hbox.addWidget(self.helloLabel)

        