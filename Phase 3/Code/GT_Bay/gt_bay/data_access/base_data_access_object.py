import pymysql.cursors

class BaseDAO(object):
    def __init__(self):
        pass

    @staticmethod
    def get_db():
        return pymysql.connect(host='127.0.0.1',
                                 user='debian-sys-maint',
                                 password='2SYRPmF5XUFSIQgq',
                                 db='GT_BAY')

    def find_all(self):
        pass

    def find_by_id(self):
        pass
