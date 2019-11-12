from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    title = models.CharField( max_length=100, verbose_name='title' )
    content = models.TextField( verbose_name='content' )
    date_gen = models.DateTimeField( auto_now_add=True, verbose_name='written' )
    date_mod = models.DateTimeField( auto_now=True, verbose_name='modified' )

    author = models.ForeignKey( User, on_delete=models.CASCADE, verbose_name='author' )

    def get_absolute_url(self):
        return reverse('message-detail', kwargs={'pk': self.pk})


