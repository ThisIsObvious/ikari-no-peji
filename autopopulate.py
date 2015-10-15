number = [str(i) for i in range(1,17)]
URL = str(http://img.mangastream.com/cdn/manga/53/2962/) + str(0) + [str(i) for i in range(1,17)]
caption = [str(i) for i in range(2,34, 2)]
manga = Bleach

import os
os.environ['DJANGO_SETTINGS_MODULE']='project.settings'

from customer.models import Customer
from django.contrib.auth.models import User

users = User.objects.all()

if __name__ == "__main__":
    for i in range(10):
        customer = Customer(first_name=choice(first_names), last_name=choice(last_names),
                        telephone=choice(phones),email=choice(emails), creator=choice(users))
        customer.save()
