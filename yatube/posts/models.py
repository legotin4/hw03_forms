from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField()
	description = models.TextField()

	def __str__(self):
		return self.title

class Post(models.Model):
	text = models.TextField()
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField('Картинка', upload_to='posts/img/', blank=True)

	def __str__(self):
		return self.text

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	created = models.DateTimeField('date published', auto_now_add=True)

	def __str__(self):
		return self.text