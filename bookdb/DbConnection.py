import pymysql
class DbConnection:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'bookAdmin'
        self.password = '123456'
        self.db = 'book'
        self.charset = 'utf8'
        self.connection = None
        self.is_connected=False
    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.password,
                db=self.db,
                charset=self.charset
            )
            self.is_connected=True
        except:
            print('连接失败')
        finally:
            return self
    def close(self):
        if self.connection!=None:
            self.connection.close()
    def __str__(self) -> str:
        return f'{self.user}@{self.host}:{self.port} in {self.db}'
    def cursor(self):
        if (self.connection!=None):
            try:
                return self.connection.cursor()
            except Exception:
                return None
class User:
    def __init__(self,name,id,type) -> None:
        self.user_name=name
        self.user_id=id
        self.user_type=type
        self.is_login=False
    