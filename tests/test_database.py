import unittest

from rcblog import db


class TestDataBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.DB_NAME = 'unittests'

    def setUp(self):
        self.date_base = db.DataBase()
        self.date_base.init()

    def tearDown(self):
        conn = db.r.connect()
        db.r.db_drop(db.DB_NAME).run(conn)

    def test_add_translation(self):
        eng_translation = {
            'eng': {
                'title': 'Title1',
                'markdown': '`markdown`'
            }
        }
        jbo_and_rus_translations = {
            'jbo': {
                'title': 'Titlo1',
                'markdown': '`markdowno`'
            },
            'rus': {
                'title': 'Звголовок1',
                'markdown': '`макрдаун`'
            }
        }
        self.date_base.add_post(eng_translation, ['tag1', 'tag2'])
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        id_ = post['id']
        self.date_base.add_translation(id_, jbo_and_rus_translations)
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        self.assertEqual(post['translations']['eng']['markdown'], '`markdown`')
        self.assertEqual(post['translations']['jbo']['markdown'], '`markdowno`')
        self.assertEqual(post['translations']['rus']['markdown'], '`макрдаун`')

    def test_add_tag(self):
        eng_and_rus_translations = {
            'jbo': {
                'title': 'Title1',
                'markdown': '`markdown`'
            },
            'rus': {
                'title': 'Звголовок1',
                'markdown': '`макрдаун`'
            }
        }
        self.date_base.add_post(eng_and_rus_translations, ['tag1', 'tag2'])
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        id_ = post['id']
        self.date_base.add_tags(id_, ['tag3', 'tag4'])
        posts = self.date_base.get_all_posts()
        self.assertEqual(len(posts), 1)
        post = posts[0]
        self.assertEqual(post['tags'], ['tag1', 'tag2', 'tag3', 'tag4'])
