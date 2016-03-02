import sys

from rcblog import db
from rcblog.crypto import make_hash

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 init.py <username> <password>')
        sys.exit(1)
    username, password = sys.argv[-2:]
    password_hash, salt = make_hash(password)
    db.DataBase().init(username, password_hash, salt)
