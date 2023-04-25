from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField

class Deck(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deck_detail', args=[str(self.id)])

class Card(models.Model):
    question = models.TextField()
    answer = RichTextUploadingField()
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('card_detail', args=[str(self.id)])
# Create your models here.
