from django.shortcuts import render,redirect,get_object_or_404
from .forms import ThumbnailForm,OwnerForm,ProjectsForm,FileForm,\
                    FileNameSearchForm,CategoryChoiceForm,DescriptionForm
from .models import File
from datetime import datetime
from PIL import Image,ImageFilter
from psd_tools import PSDImage
import sys,os
# Create your views here.

UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'
THUMBNAIL_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/thumbnail/'




def upload(request):
    """
    最初が画像ファイルのみの想定だったが、やっぱり色々なファイルのアップロードに対応するために改良
    FileFieldを使わずにopen(path,'wb')でコピーしている
    サムネイル作成対応
    18/10/22
    momo: 現在フォームを個別に設定しているが一つのクラスにまとめてforループで処理したほうがよさそう・・
    """
    if not request.method == 'POST':#methodが'POST'ではない　＝最初のページ表示時の処理
        return render(request, 'upload_form/upload.html',{
            'FileForm'  : FileForm(),
            'ThumbnailForm' : ThumbnailForm(),
            'OwnerForm' : OwnerForm(),
            'ProjectsForm' : ProjectsForm(),
            'CategoryChoiceForm' : CategoryChoiceForm(),
            'DescriptionForm' : DescriptionForm(),
            # 'images': ImageFile.objects.all(),
        })


    """パス作成してファイルコピー"""
    # リクエストオブジェクト取得
    file = request.FILES['file']
    try:
        thumbnail = request.FILES['thumbnail']
    except:
        thumbnail = ''
    # ファイルをアップロードする場所
    path = os.path.join(UPLOADE_DIR,file.name)
    #拡張子を分離
    root,ext = os.path.splitext(path)

    # サムネイル用のパス
    thumbnail_path = os.path.join(THUMBNAIL_DIR,file.name)
    thumbnail_root,thumbnail_ext = os.path.splitext(thumbnail_path)
    thumbnail_root =thumbnail_root + "_thumbnail"
    thumbnail_path = thumbnail_root + thumbnail_ext
    if os.path.exists(path):
        # すでに同じ名前のファイルが存在する場合、ファイル名の最後に日付を書き足して保存する
        path = root +'_'+ datetime.now().strftime('%Y%m%d%H%M%S') + ext
        thumbnail_path = thumbnail_root +'_'+ datetime.now().strftime('%Y%m%d%H%M%S') + ext

    # ファイルをコピーする
    destination = open(path,'wb')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

    """
    サムネ作成
    """
    #そのファイル自体からサムネイルを作成できるもののリスト
    image_file_extension = ['.jpg','.png','.bmp','.tga']
    if thumbnail:
        # サムネイルがアップされているときはコピーする
        destination = open(thumbnail_path,'wb')
        for chunk in thumbnail.chunks():
            destination.write(chunk)
        destination.close()
    elif ext =='.psd':
        # PSDのときサムネイル作成
        thumbnail_root,thumbnail_ext = os.path.splitext(thumbnail_path)
        # サムネイルのパスの拡張子をjpgにしておく
        thumbnail_path =thumbnail_root + ".jpg"
        psd = PSDImage.load(path)
        merged_image = psd.as_PIL()
        merged_image.thumbnail((512,512), Image.ANTIALIAS)
        merged_image.save(thumbnail_path)
    elif ext in image_file_extension:
        # 画像ファイルの場合サムネイルを作成
        try:
            thumbnail_root,thumbnail_ext = os.path.splitext(thumbnail_path)
            # サムネイルのパスの拡張子をjpgにしておく
            thumbnail_path =thumbnail_root + ".jpg"
            # サムネイルをファイルから作成する
            img = Image.open(path)
            # resizeではなくthumbnailを利用して縮小
            img.thumbnail((512, 512), Image.ANTIALIAS)
            # リサイズ後の画像を保存
            img.save(thumbnail_path, 'JPEG', quality=100, optimize=True)
        except:
            #Pillowが画像処理できなかった場合の処理
            print('Pillow can not create thumbnail image..')
            thumbnail_path = os.path.join(THUMBNAIL_DIR,'None.jpg')
    else:
        # サムネイルを作成できない場合はこのサムネにする
        thumbnail_path = os.path.join(THUMBNAIL_DIR,'None.jpg')


    """データベース更新"""
    file_model = File()
    file_path = os.path.join('/static/files/'+os.path.basename(path))
    file_model.file_path= file_path
    # サムネイル実装
    file_model.thumbnail_path = os.path.join('/static/files/thumbnail/'+os.path.basename(thumbnail_path))
    file_model.file_name = os.path.basename(path)
    file_model.owner = request.POST['owner']
    file_model.projects_name = request.POST['projects']
    file_model.category = request.POST['category']
    file_model.description = request.POST['description']
    file_model.extension = ext

    file_model.save()


    return redirect('upload_form:list')


def list(request):
    """
    フィルター実装
    ファイル名の検索フォーム実装
    リストのフィルターフォームからのPOSTを受け取って、フィルタリングする
    """
    # クエリセット作成
    files =File.objects.all()
    extension = File.objects.values('extension').order_by('extension').distinct()
    projects_name = File.objects.values('projects_name').order_by('projects_name').distinct()
    owner = File.objects.values('owner').order_by('owner').distinct()


    """GETの内容を取得してフィルタリングする"""
    category = request.GET.get('category')

    q_file_name_search = request.GET.get('file_name_search')
    q_ext = request.GET.get('extension')
    q_owner = request.GET.get('owner')
    q_projects_name = request.GET.get('projects_name')
    # q_category = request.POST['category']
    # フィルタリングする
    if category and not category == 'AssetLibrary':
        files = files.filter(category__contains=category)
    if q_file_name_search:
        files = files.filter(file_name__contains=q_file_name_search)
    if q_ext:
        files = files.filter(extension__contains=q_ext)
    if q_owner:
        files = files.filter(owner__contains=q_owner)
    if q_projects_name:
        files = files.filter(projects_name__contains=q_projects_name)

    return render (request,'upload_form/list.html',{
                'FileNameSearchForm'  : FileNameSearchForm(),
                'files': files,
                'extension' : extension,
                'projects_name' : projects_name,
                'owner' : owner,
    })


def file_del(request):
    """ファイルの削除"""
    if not request.method == 'POST':#methodが'POST'ではない　＝最初のページ表示時の処理
        return redirect('upload_form:list')

    del_id = request.POST['del_id']
    file = get_object_or_404(File, pk=del_id)
    file.delete()
    return redirect('upload_form:list')
