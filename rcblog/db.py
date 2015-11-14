import rethinkdb as r

DB_NAME = 'test'


class DataBase(object):
    def __init__(self):
        self.connection = r.connect(db=DB_NAME)

    def _create_posts_table(self):
        r.table_create('posts').run(self.connection)

    def _create_languages_table(self):
        r.table_create('languages').run(self.connection)
        r.table('languages').insert({'eng': 'English'})
        r.table('languages').insert({'rus': 'Русский'})
        r.table('languages').insert({'jbo': 'la .lojban.'})

    def add_post(self, markdown_files: dict, tags: list):
        r.table('posts').insert({
            'translations': markdown_files,
            'tags': tags,
        }).run(self.connection)

    def add_translation(self, id_, markdown_files: dict):
        # TODO insert all in once
        for lang, markdown_file in markdown_files.items():
            r.table('posts').get(id_).update({
                'translations': {lang: markdown_file}
            }).run(self.connection)

    def add_tags(self, id_, tags: list):
        # TODO Insert all in once
        for tag in tags:
            r.table('posts').get(id_).update({
                'tags': r.row['tags'].append(tag)
            }).run(self.connection)

    def get_all_posts(self):
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor]

    def get_posts_by_tag(self, tag: str):
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor if tag in post['tags']]

    def get_list_of_languages(self):
        cursor = r.table('language').run(self.connection)
        return [language for language in cursor]

    def init(self):
        self._create_posts_table()
        self._create_languages_table()

