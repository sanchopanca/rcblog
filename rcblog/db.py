import datetime

import pytz
import rethinkdb as r
from rethinkdb.errors import ReqlRuntimeError

DB_HOST = 'rethinkdb-rcblog'
DB_NAME = 'test'


class DataBase(object):
    def __init__(self):
        self.connection = r.connect(host=DB_HOST, db=DB_NAME)

    def _create_posts_table(self):
        r.table_create('posts').run(self.connection)

    def _drop_posts_table(self):
        r.table_drop('posts').run(self.connection)

    def _create_languages_table(self):
        r.table_create('languages').run(self.connection)
        r.table('languages').insert({'eng': 'English'}).run(self.connection)
        r.table('languages').insert({'rus': 'Русский'}).run(self.connection)
        r.table('languages').insert({'jbo': 'la .lojban.'}).run(self.connection)

    def _drop_languages_table(self):
        r.table_drop('languages').run(self.connection)

    def _create_credentials_table(self, username, password_hash, salt):
        r.table_create('credentials').run(self.connection)
        r.table('credentials').insert({
            'username': username,
            'password_hash': password_hash,
            'salt': salt,
        }).run(self.connection)

    def _drop_credentials_table(self):
        r.table_drop('credentials').run(self.connection)

    def add_post(self, translations: dict, tags: list, draft=False, date=None):
        """
        :param translations:
         dict {
            'lng': {
                'title': 'Title of the post',
                'markdown': 'content of post'
            }
        }
        :param tags: list of tags
        :param draft: is this post draft or not
        :param date: date of post
        """
        if date is None:
            date = datetime.datetime.now(pytz.utc)
        r.table('posts').insert({
            'translations': translations,
            'draft': draft,
            'tags': tags,
            'date': date,
        }).run(self.connection)

    def update_post(self, id_, translations: dict, tags: list, draft=False, date=None):
        if date is None:
            date = datetime.datetime.now(pytz.utc)
        r.table('posts').get(id_).update({
            'translations': translations,
            'draft': draft,
            'tags': tags,
            'date': date,
        }).run(self.connection)

    def add_translation(self, id_, translations: dict):
        r.table('posts').get(id_).update({
            'translations': translations
        }).run(self.connection)

    def add_tags(self, id_, tags: list):
        r.table('posts').get(id_).update({
            'tags': r.row['tags'].splice_at(-1, tags)
        }).run(self.connection)

    def get_all_posts(self):
        cursor = r.table('posts').filter({'draft': False}).run(self.connection)
        return [post for post in cursor]

    def get_all_drafts(self):
        cursor = r.table('posts').filter({'draft': True}).run(self.connection)
        return [post for post in cursor]

    def get_all_languages(self):
        languages = {}
        cursor = r.table('languages').run(self.connection)
        for language in cursor:
            languages.update(language)
        del languages['id']
        return languages

    def get_languages_by_codes(self, *codes):
        # TODO Optimize the query
        languages = {}
        cursor = r.table('languages').run(self.connection)
        for language in cursor:
            for code in codes:
                if code in language:
                    languages.update(language)
                    continue
        del languages['id']
        return languages

    def get_credentials(self, username):
        credentials = r.table('credentials').filter({'username': username}).limit(1).run(self.connection)
        for item in credentials:
            return item

    def get_posts_by_tag(self, tag: str):
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor if tag in post['tags']]

    def get_post_by_id(self, id_):
        post = r.table('posts').get(id_).run(self.connection)
        return post

    def get_list_of_languages(self):
        cursor = r.table('language').run(self.connection)
        return [language for language in cursor]

    def init(self, username, password_hash, salt):
        _create_db()
        try:
            self._drop_posts_table()
        except ReqlRuntimeError:
            pass
        try:
            self._drop_languages_table()
        except ReqlRuntimeError:
            pass
        try:
            self._drop_credentials_table()
        except ReqlRuntimeError:
            pass
        try:
            self._create_posts_table()
        except ReqlRuntimeError:
            pass
        try:
            self._create_languages_table()
        except ReqlRuntimeError:
            pass
        try:
            self._create_credentials_table(username, password_hash, salt)
        except ReqlRuntimeError:
            pass


def _create_db():
    conn = r.connect(host=DB_HOST)
    try:
        r.db_create(DB_NAME).run(conn)
    except ReqlRuntimeError:
        pass
