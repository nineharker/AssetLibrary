from django.urls import path
from . import views


app_name = 'upload_form'
urlpatterns = [
    path('upload/',views.upload, name='upload'),
    path('list/',views.list, name='list'),
    path('file_del/',views.file_del,name = 'file_del')
]
