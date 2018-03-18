"""Unit test module for GT_Bay app

"""


#import os
import sys
import logging
sys.path.append('../gt_bay')
import gt_bay_app
import unittest
#import tempfile

from data_access.base_data_access_object import BaseDAO


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GtBayTestCase(unittest.TestCase):

    def setUp(self):
        """Setup app (connect to DB, disable CSRF)

        """

        #self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        dao = BaseDAO()
        self.db = dao.get_db()

        gt_bay_app.app.testing = True

        self.app = gt_bay_app.app.test_client()

        gt_bay_app.app.config.update(dict(
            #SECRET_KEY='development key',
            WTF_CSRF_ENABLED=False
        ))

        '''with flaskr.app.app_context():
            flaskr.init_db()'''

    def tearDown(self):
        """Close database

        """

        '''os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])'''
        self.db.close()

    def login(self, user_name, password):
        """Log in to app using the supplied user_name and password.

        """

        return self.app.post('/login', data=dict(
            user_name=user_name,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Log out of the app.

        """

        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        """Test various user_name / password combinations (both admin and regular user user types).

        """

        # missing username / password input: START
        logging.debug("\n\ntest_login_logout: no username")
        rv = self.login(None, 'password')  # missing username
        assert b'Username is required.' in rv.data

        logging.debug("\n\ntest_login_logout: no password")
        rv = self.login('admin01', None)  # missing username
        assert b'Password is required.' in rv.data

        logging.debug("\n\ntest_login_logout: no username or password")
        rv = self.login(None, None)  # missing username
        assert b'Username is required.' in rv.data
        assert b'Password is required.' in rv.data
        # missing username / password input: END

        # admin log in test: START
        logging.debug("\n\ntest_login_logout: admin valid user_name / valid password")
        rv = self.login('admin01', 'password')  # admin valid user_name / valid password
        assert b'You were logged in.' in rv.data

        logging.debug("\n\ntest_login_logout: admin log out")
        rv = self.logout()
        assert b'You were logged out' in rv.data

        logging.debug("\n\ntest_login_logout: admin valid user_name / invalid password")
        rv = self.login('admin01', 'defaultx')  # admin valid user_name / invalid password
        assert b'Username and or password is incorrect.' in rv.data

        logging.debug("\n\ntest_login_logout: admin invalid user_name / valid password")
        rv = self.login('adminx', 'password')  # admin invalid user_name / valid password
        assert b'Username and or password is incorrect.' in rv.data
        # admin log in test: END

        # regular user log in test: START
        logging.debug("\n\ntest_login_logout: regular user valid user_name / valid password")
        rv = self.login('user01', 'password')  # regular user valid user_name / valid password
        assert b'You were logged in.' in rv.data

        logging.debug("\n\ntest_login_logout: regular user log out")
        rv = self.logout()
        assert b'You were logged out' in rv.data

        logging.debug("\n\ntest_login_logout: regular user valid user_name / invalid password")
        rv = self.login('user01', 'defaultx')  # regular user valid user_name / invalid password
        assert b'Username and or password is incorrect.' in rv.data

        logging.debug("\n\ntest_login_logout: regular user invalid user_name / valid password")
        rv = self.login('userx', 'password')  # regular user invalid user_name / valid password
        assert b'Username and or password is incorrect.' in rv.data
        # regular user log in test: END

if __name__ == '__main__':
    unittest.main()