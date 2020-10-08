from django.db import models
import os
import uuid
# Create your models here.

def get_icon_path(instance, file_name):

        prefix = 'images/'
        random_num = str(uuid.uuid4()).replace('-', '')
        suffix = os.path.splitext(file_name)[-1]
        return prefix + random_num + suffix

class IconModel(models.Model):

    name = models.CharField('icon name', max_length=20)
    image = models.ImageField('icon image', upload_to=get_icon_path, blank=True, null=True)

    def __str__(self):
        return self.name
