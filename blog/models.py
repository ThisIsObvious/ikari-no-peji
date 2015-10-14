from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
class Manga(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    refreshed_date = models.DateTimeField(
            blank=True, null=True)
    def __str__(self):
        return self.title
        
class Page(models.Model):
    number = models.PositiveIntegerField(
        blank = True, null = True,
        editable = True,
        default = 0
    )
    page = models.ImageField(
        upload_to='ikari-no-peji/', 
        height_field='height', 
        width_field='width'
    )
    caption = models.TextField(blank=True)
    manga = models.ForeignKey('Manga')
    width = models.PositiveIntegerField(
        blank = True, null = True,
        editable = False,
        default = 0
    )
    height = models.PositiveIntegerField(
        blank = True, null = True,
        editable = False,
        default = 0
    )
    def __str__(self):
        return self.number
