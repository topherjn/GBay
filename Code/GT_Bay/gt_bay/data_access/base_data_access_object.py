import pymysql.cursors

class BaseDAO(object):
    def __init__(self):
        pass

    @staticmethod
    def get_db():
        return pymysql.connect(host='localhost',
                                 user='root',
                                 password='passw0rd',
                                 db='GT_BAY')


    def find_all(self):
        pass

    def find_by_id(self):
        pass