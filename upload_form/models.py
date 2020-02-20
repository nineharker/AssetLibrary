from django.db import models
from datetime import datetime
# from imagekit.models import ImageSpecField,ProcessedImageField
# from imagekit.processors import ResizeToFill
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import sys
# Create your models here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_CHOICES = (
    ("テクスチャ", 'テクスチャ'),
    ('モデル', 'モデル'),
    ('エフェクト', 'エフェクト'),
)


class File(models.Model):
    # 画像のモデル
    class Meta:
        # モデル自体を表す文字列
        verbose_name = 'ファイル'
        verbose_name_plural = 'ファイル'
        ordering = ['-upload_time']
    owner = models.CharField(max_length=20)
    file_name = models.CharField(max_length=50)
    upload_time = models.DateTimeField(default=datetime.now)
    projects_name = models.CharField(max_length=20)
    file_path = models.CharField(max_length=100)
    thumbnail_path = models.CharField(max_length=100)
    extension = models.CharField(max_length=10)
    category = models.CharField(
        max_length=5, choices=CATEGORY_CHOICES, default=None)
    description = models.CharField(max_length=100, blank=True)
    #

    def __str__(self):
        return self.file_name


# モデル削除後に`file_field`を削除する。
@receiver(post_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    try:
        # ドライブレターを消すためにスライシング
        file_path = os.path.join(BASE_DIR, instance.file_path[1:])
        os.remove(file_path)
    except FileNotFoundError:
        print('File not found')

    if instance.thumbnail_path == 'https://user-images.githubusercontent.com/48968940/74902177-970dbf00-53e8-11ea-94d5-a93d440ba732.jpg':
        # サムネがもともとなかった場合はreturn
        return
    try:
        # ドライブレターを消すためにスライシングして合体
        thumbnail_path = os.path.join(BASE_DIR, instance.thumbnail_path[1:])
        os.remove(thumbnail_path)
    except FileNotFoundError:
        print('File not found')
