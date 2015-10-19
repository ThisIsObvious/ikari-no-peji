import os
import shutil
import requests
from blog.models import Manga, Page

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ikari.settings')

import django
django.setup()

def add_page(num):
    p = Page.objects.get_or_create(number=num, manga_id=1)
    p.URL = 'http://img.mangastream.com/cdn/manga/53/2962/' + str(0) + str(num) +'.png'
    r = requests.get(p.URL, stream=True)
    with open(str(0)+str(num)+'.png', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
        p.Page.save(str(0)+str(num)+'.png', f, save=True)
    del response
    p.Caption = str(num*2)
    return p

if __name__ == "__main__":
    print ("Script...")
    for i in range(10):
        add_page(i)
