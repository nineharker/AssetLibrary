from django import forms
from . import models

CATEGORY_CHOICES = (
    ('Textures', 'Textures'),
    ('Models', 'Models'),
    ('Effects', 'Effects'),
)

class ThumbnailForm(forms.Form):
    thumbnail = forms.FileField(label='サムネイル（任意）',required=False)

class OwnerForm(forms.Form):
    owner= forms.CharField(max_length=10,label='投稿者')

class ProjectsForm(forms.Form):
    projects= forms.CharField(max_length=100,label='プロジェクト名')


class FileForm(forms.Form):
    file = forms.FileField(label='ファイル')

class FileNameSearchForm(forms.Form):
   file_name_search = forms.CharField(min_length=2, max_length=100,label='ファイル名検索',required=False)


class CategoryChoiceForm(forms.Form):
    category = forms.ChoiceField(label='カテゴリ',widget=forms.Select,choices=CATEGORY_CHOICES)

class DescriptionForm(forms.Form):
    description= forms.CharField(max_length=100,label='説明',required=False)
