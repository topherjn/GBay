import MySQLdb

class BaseDAO(object):
    def __init__(self):
        pass

    @staticmethod
    def get_db():
        return MySQLdb.connect("localhost", "root", "Passw0rd", "gt_bay")



    def find_all(self):
        pass

    def find_by_id(self):
        pass
