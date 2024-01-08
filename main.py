import sys

sys.path.append(f'{sys.path[0]}/bookdb')
sys.path.append(f'{sys.path[0]}/qtui')
from bookdb.DbConnection import DbConnection, User
from PyQt6.QtWidgets import QApplication
from qtui.Login import LoginWindow
from qtui.MainWindow import MainWindow


def main():
    # 连接数据库
    dbc = DbConnection().connect()
    # qt应用
    app = QApplication(sys.argv)
    user = User('', -1, -1)
    mainwindow: MainWindow = None
    login = LoginWindow(dbc=dbc, user=user, mainwindow=mainwindow)
    login.show()
    app.exec()
    dbc.close()


if __name__ == "__main__":
    main()
