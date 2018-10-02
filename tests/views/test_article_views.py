# -*- coding: utf-8 -*-
import json


def _create_article(testclient, user):
    data = {
        'title': 'This is a blog ...',
        'content': 'This is the blog content ...',
        'user_id': user['id']
    }
    headers = {
        'Authorization': 'Bearer {}'.format(user['token'])
    }
    resp = testclient.post('/articles', data=data, headers=headers)
    return resp


class TestArticleView(object):
    @staticmethod
    def user_create_article(testclient, user):
        resp = _create_article(testclient, user)
        article = json.loads(resp.data)
        assert all(
            key in article
            for key in ['id', 'created_at', 'updated_at', 'slug', 'title']
        )
        assert resp.status_code == 201
        return resp.status_code, article

    def test_create_article(self, testclient, user):
        # Login to get access token
        resp = testclient.post('/users/auth/email', data={
            'email': user.email,
            'password': '12345678@ABC'
        })
        assert resp.status_code == 200

        # Load user data
        user = json.loads(resp.data)

        # Let the user post a new article
        status_code, first_article = self.user_create_article(testclient, user)
        assert status_code == 201

        # Now, he/she create another article with the same title. The system
        # should generate different slug for him/her
        status_code, second_article = self.user_create_article(testclient, user)
        assert status_code == 201
        assert second_article['slug'] != first_article['slug']

    def test_get_articles(self, testclient, user):
        # Login to get access token
        resp = testclient.post('/users/auth/email', data={
            'email': user.email,
            'password': '12345678@ABC'
        })

        # Load user data
        user = json.loads(resp.data)

        # Let the user post 2 articles
        self.user_create_article(testclient, user)
        self.user_create_article(testclient, user)

        # Now, get the list articles
        resp = testclient.get('/articles')
        assert resp.status_code == 200
        articles = json.loads(resp.data)
        assert len(articles) == 2

    def test_get_article(self, testclient, user):
        # Login to get access token
        resp = testclient.post('/users/auth/email', data={
            'email': user.email,
            'password': '12345678@ABC'
        })
        user = json.loads(resp.data)

        # Create article
        _, article = self.user_create_article(testclient, user)

        # Get article
        resp = testclient.get(
            '/articles/{}'.format(article['slug'])
        )
        assert resp.status_code == 200
        assert json.loads(resp.data)['slug'] == article['slug']

    def test_update_article(self, testclient, user):
        # Login to get access token
        resp = testclient.post('/users/auth/email', data={
            'email': user.email,
            'password': '12345678@ABC'
        })
        user = json.loads(resp.data)

        # Create article
        _, article = self.user_create_article(testclient, user)
        update_article = article.copy()
        update_article['title'] = 'New article'

        # Update article
        headers = {
            'Authorization': 'Bearer {}'.format(user['token'])
        }
        resp = testclient.put(
            '/articles/{}'.format(article['slug']),
            data=update_article,
            headers=headers
        )
        assert resp.status_code == 200
        article = json.loads(resp.data)
        assert article['title'] == update_article['title']
        assert article['slug'] == update_article['slug']

    def test_delete_article(self, testclient, user):
        # Login to get access token
        resp = testclient.post('/users/auth/email', data={
            'email': user.email,
            'password': '12345678@ABC'
        })
        user = json.loads(resp.data)

        # Create article
        _, article = self.user_create_article(testclient, user)

        # Delete it
        headers = {
            'Authorization': 'Bearer {}'.format(user['token'])
        }
        resp = testclient.delete(
            '/articles/{}'.format(article['slug']),
            headers=headers
        )
        assert resp.status_code == 204

        # Get article, it should not found
        resp = testclient.get(
            '/articles/{}'.format(article['slug'])
        )
        assert resp.status_code == 404
