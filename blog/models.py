from django.db import models
from django.utils import timezone
from io import StringIO
from urllib import parse
from urllib import request
from PIL import Image
import imghdr
import copy


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
        default = 1
    )
    URL = models.URLField(
        default = 'http://img.mangastream.com/'
    )
    page = models.ImageField(
        upload_to='.',
        null=True, 
        blank=True,
    )
    caption = models.TextField(blank=True)
    manga = models.ForeignKey('Manga')

    def save(self, url='', *args, **kwargs):
        if self.page != '' and url != '':
            image = download_image(url)
            try:
                filename = parse(url).path.split('/')[-1]
                self.page = filename
                tempfile = image
                tempfile_io = StringIO()
                tempfile.save(tempfile_io, format=image.format)
                self.page.save(filename, ContentFile(tempfile_io.getvalue()), save=False) 
            except Exception as e:
                print ("Error trying to save model: saving image failed: " + str(e))
                pass
        super(Page, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.number)

def download_image(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    r = request.Request(url, headers=headers)
    req = request.urlopen(r, timeout=10)
    image_data = StringIO(req.read())
    img = Image.open(image_data)
    img_copy = copy.copy(img)
    if valid_img(img_copy):
        return img
    else:
        raise Exception('An invalid image was detected when attempting to save a Page!')

def valid_img(img):
    type = img.format
    if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except:
            return False
    else: return False
