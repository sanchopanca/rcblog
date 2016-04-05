class User(object):
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super(User, cls).__new__(cls, *args)
        return cls._instance

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @staticmethod
    def get_id():
        return '1'

    @staticmethod
    def get_by_id(*args):
        return User()
