import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class User:
    def __init__(self, user_name=None, password=None, first_name=None, last_name=None):
        self._id = None
        self._user_name = user_name
        self._password = password
        self._position = None
        self._first_name = first_name
        self._last_name = last_name

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        self._user_name = value

    @property
    def password(self):
        return self._password

    @property
    def position(self):
        return self._position

    @property
    def is_admin(self):
        ret_val = False
        if self._position is not None:
            ret_val = True
        return ret_val

    def to_json(self):
        dict = {'user_name': self._user_name, 'password': self._password, 'position': self._position}
        return dict

    # todo create some data access object (DAO) layer
    # just putting this here for now to get something to work
    @staticmethod
    def login(user_name=None, password=None):
        ret_val = None
        error = None
        logging.debug("sss user_name={}, password={}".format(user_name, password))
        if user_name == 'user01' and password == 'password':
            ret_val = User(user_name, password)

        if user_name == 'admin' and password == 'password':
            ret_val = User(user_name, password)
            ret_val._position = 'DBA'

        if ret_val is None:
            error = 'Incorrect Username or Password'

        return ret_val, error

    @staticmethod
    def create_user(user_name=None, password=None, first_name=None, last_name=None):
        ret_val = None
        error = None
        logging.debug("sss user_name={}, password={}".format(user_name, password))
        if user_name == 'user01' or user_name == 'admin':
            error = 'User Name already take'
        else:
            ret_val = User(user_name, password, first_name, last_name)

        return ret_val, error
