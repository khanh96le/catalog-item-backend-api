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
        resp = _create_article(testclient, user)
        first_article = json.loads(resp.data)
        assert all(
            key in first_article
            for key in ['id', 'created_at', 'updated_at', 'slug', 'title']
        )
        assert resp.status_code == 201

        # Now, he/she create another article with the same title. The system
        # should generate different slug for him/her
        resp = _create_article(testclient, user)
        print(resp.data)
        assert resp.status_code == 201
        second_article = json.loads(resp.data)
        assert second_article['slug'] != first_article['slug']
