from django.db import models

# Create your models here.
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField(max_length=1000)

    author = models.ForeignKey(
        'auth.User',
        on_delete = models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('bbs:detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    text = models.TextField('本文')
    target = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(
        'auth.User',
        on_delete = models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]