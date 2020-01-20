from django.contrib import admin
from .models import File
# Register your models here.



class FileAdmin(admin.ModelAdmin):
    list_display =("file_name","owner","upload_time")  # 一覧に出したい項目
    # list_display_links = ('id', 'name')  # 修正リンクでクリックできる項目





admin.site.register(File,FileAdmin)
