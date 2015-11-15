import unittest

from rcblog import db


class TestDataBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.DB_NAME = 'test'
        date_base = db.DataBase()
        try:
            db.r.table_drop('languages').run(date_base.connection)
        except Exception as e:
            print(e)
        try:
            db.r.table_drop('posts').run(date_base.connection)
        except Exception as e:
            print(e)
        try:
            date_base.init()
        except Exception as e:
            print(e)
        try:
            db.r.table('languages').delete().run(date_base.connection)
        except Exception as e:
            print(e)
        try:
            db.r.table('posts').delete().run(date_base.connection)
        except Exception as e:
            print(e)

    def setUp(self):
        self.date_base = db.DataBase()

    def tearDown(self):
        db.r.table('languages').delete().run(self.date_base.connection)
        db.r.table('posts').delete().run(self.date_base.connection)

    def test_add_translation(self):
        self.date_base.add_post({'eng': 'post1_eng.md'}, ['tag1', 'tag2'])
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        id_ = post['id']
        self.date_base.add_translation(id_, {'jbo': 'post1_jbo.md', 'rus': 'post1_rus.md'})
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        self.assertEqual(post['translations']['eng'], 'post1_eng.md')
        self.assertEqual(post['translations']['rus'], 'post1_rus.md')
        self.assertEqual(post['translations']['jbo'], 'post1_jbo.md')

    def test_add_tag(self):
        self.date_base.add_post({'eng': 'post1_eng.md', 'rus': 'post1_rus.md'}, ['tag1', 'tag2'])
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        id_ = post['id']
        self.date_base.add_tags(id_, ['tag3', 'tag4'])
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        self.assertEqual(post['tags'], ['tag1', 'tag2', 'tag3', 'tag4'])
