from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
from io import BytesIO
from urllib import parse
from urllib import request
from PIL import Image
import imghdr
import copy

def get_upload_path(instance, filename):
    name, extension = filename.split('.')
    file_path = '{manga}/{ch}/{name}.{extension}'.format(
         manga = instance.manga.title, ch = instance.chapter,
         name = name, extension = extension
    ) 
    return file_path

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
    chapter = models.PositiveIntegerField(
        blank = True, null = True,
        editable = True,
        default = 1
    )
    URL = models.URLField(
        default = 'http://img.mangastream.com/'
    )
    page = models.ImageField(
        upload_to=get_upload_path,
        null=True, 
        blank=True,
    )
    caption = models.TextField(blank=True)
    manga = models.ForeignKey('Manga')

    def save(self, url='', *args, **kwargs):
        if self.page != '' and url != '':
            image = download_image(url)
            try:
                self.URL=str(url)
                filename = str(self.manga.title) + str('{:04}'.format(self.chapter)) + str('{:02}'.format(self.number)) + "." + parse.urlparse(url).path.split('.')[-1]
                self.page = filename
                tempfile = image
                tempfile_io = BytesIO()
                tempfile.save(tempfile_io, format=image.format)
                self.page.save(filename, ContentFile(tempfile_io.getvalue()), save=False)
            except Exception as e:
                print ("Error trying to save model: saving image failed: " + str(e))
                pass
        super(Page, self).save(*args, **kwargs)
    def __str__(self):
        return str(str(self.manga.title) + str('{:04}'.format(self.chapter)) + str('{:02}'.format(self.number)))

def download_image(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    r = request.Request(url, headers=headers)
    req = request.urlopen(r, timeout=10)
    image_data = BytesIO(req.read())
    img = Image.open(image_data)
    img_copy = copy.copy(img)
    ##if valid_img(img_copy):
    return img
    ##else:
     ##   raise Exception('An invalid image was detected when attempting to save a Page!')

def valid_img(img):
    type = img.format
    if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except:
            return False
    else: return False
