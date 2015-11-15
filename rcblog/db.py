import rethinkdb as r

DB_NAME = 'test'


class DataBase(object):
    def __init__(self):
        self.connection = r.connect(db=DB_NAME)

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

    def add_post(self, translations: dict, tags: list):
        """
        :param translations:
         dict {
            'lng': {
                'title': 'Title of the post',
                'markdown_file': 'path/to/markdown/file.md'
            }
        }
        """
        r.table('posts').insert({
            'translations': translations,
            'tags': tags,
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
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor]

    def get_all_languages(self):
        languages = {}
        cursor = r.table('languages').run(self.connection)
        for language in cursor:
            print('i am here')
            print(language)
            languages.update(language)
        del languages['id']
        return languages

    def get_posts_by_tag(self, tag: str):
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor if tag in post['tags']]

    def get_list_of_languages(self):
        cursor = r.table('language').run(self.connection)
        return [language for language in cursor]

    def init(self):
        self._drop_posts_table()
        self._drop_languages_table()
        self._create_posts_table()
        self._create_languages_table()

