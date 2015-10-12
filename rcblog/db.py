import rethinkdb as r


class DataBase(object):
    def __init__(self):
        self.connection = r.connect(db='test')

    def _create_posts_table(self):
        r.table_create('posts').run(self.connection)

    def add_post(self, markdown_file_name: str, tags: list):
        r.table('posts').insert({
            'filename': markdown_file_name,
            'tags': tags,
        }).run(self.connection)

    def get_all_posts(self):
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor]

    def get_posts_by_tag(self, tag: str):
        cursor = r.table('posts').run(self.connection)
        return [post for post in cursor if tag in post['tags']]

    def init(self):
        self._create_posts_table()

