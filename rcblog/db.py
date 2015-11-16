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

    def add_post(self, translations: dict, tags: list, draft=False):
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
            'draft': draft,
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

    def get_posts_by_tag(self, tag: str):
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor if tag in post['tags']]

    def get_post_by_id(self, id_):
        cursor = r.table('posts').get(id_).run(self.connection)
        for post in cursor:
            return post

    def get_list_of_languages(self):
        cursor = r.table('language').run(self.connection)
        return [language for language in cursor]

    def init(self):
        try:
            self._drop_posts_table()
        except Exception as e:
            print(e)
        try:
            self._drop_languages_table()
        except Exception as e:
            print(e)
        try:
            self._create_posts_table()
        except Exception as e:
            print(e)
        try:
            self._create_languages_table()
        except Exception as e:
            print(e)

