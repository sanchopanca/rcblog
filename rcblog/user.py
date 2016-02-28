class User(object):
    def __init__(self):
        self.id = '1'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def get_by_id(user_id):
        if user_id == '1':
            return User()
        return None

    @staticmethod
    def get_by_credentials(username, password):
        if username == 'admin' and password == 'secret':
            return User()
        return None
