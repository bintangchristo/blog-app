from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post
# Create your tests here.

class BlogTests(TestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='testuser',
			email='test@email.com',
			password='secret',
		)

		self.post = Post.objects.create(
			title='A good title',
			author=self.user,
			body='A nice content body'
		)

	def test_string_representation(self):
		post = Post(title='A sample title')
		self.assertEqual(str(post), 'A sample title')

	def test_get_absolute_url(self):
		self.assertEqual(self.post.get_absolute_url(), '/post/1/')

	def test_post_content(self):
		self.assertEqual(f'{self.post.title}', 'A good title')
		self.assertEqual(f'{self.post.author}', 'testuser')
		self.assertEqual(f'{self.post.body}', 'A nice content body')

	def test_post_list_view(self):
		resp = self.client.get(reverse('home'))
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'A nice content body')
		self.assertTemplateUsed(resp, 'home.html')

	def test_post_detail_view(self):
		resp = self.client.get('/post/1/')
		no_resp = self.client.get('/post/1000000/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(no_resp.status_code, 404)
		self.assertContains(resp, 'A good title')
		self.assertTemplateUsed(resp, 'post_detail.html')

	def test_post_create_view(self):
		resp = self.client.post(
			reverse('post_new'), {
				'title': 'A new title',
				'body': 'A new body',
				'author': self.user
			}
		)
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'A new title')
		self.assertContains(resp, 'A new body')

	def test_post_update_view(self):
		resp = self.client.post(
			reverse('post_edit', args='1'), {
				'title': 'A new updated title',
				'body': 'A new updated body'
			}
		)
		self.assertEqual(resp.status_code, 302)

	def test_post_delete_view(self):
		resp = self.client.post(
			reverse('post_delete', args='1')
		)
		self.assertEqual(resp.status_code, 302)