class SQLStatements(object):
    select_gt_bay_user = """SELECT RegularUser.username, AdminUser.position 
                            FROM RegularUser LEFT JOIN AdminUser ON RegularUser.username = AdminUser.username 
                            WHERE RegularUser.username = '{}' AND RegularUser.password = '{}'"""

    insert_regular_user = """INSERT INTO RegularUser(username, password, first_name, last_name) 
                          VALUES ('{}', '{}', '{}', '{}')"""
