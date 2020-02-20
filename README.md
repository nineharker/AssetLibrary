# AssetLibrary について

python の Django を使ったアセット共有 WEB アプリケーションです。open(path,'wb')を使っているので基本的になんでもアップロードできます。

サムネイルを同時にアップした場合、サムネイルが表示されます。画像ファイルや PSD の場合アップロードしたフィイルからサムネイル作成を試みます。

サムネがない場合もしくはサムネ作成に失敗した場合 NOTHUMBNAIL が表示されます。

# 使い方

クローン

```bash
git clone https://github.com/nineharker/AssetLibrary.git
cd AssetLibrary
```

pipenv でパッケージ管理しています。

```bash
# pipenvをインストール
pip install pipenv
# pipenvで依存パッケージをインストール
pipenv install
# pipenvで仮想環境に入る
pipenv shell

# Djangoでマイグレーション
python manage.py migrate
# Djangoでローカルサーバー起動
python manage.py runserver
```

下記の URL にアップロードしたファイルが表示されます。  
http://127.0.0.1:8000/upload_form/list

下記のディレクトリにアップロードしたファイルが保存されます。  
AssetLibrary/upload_form/static/files

下記のディレクトリにアップロードしたサムネイルが保存されますサムネがない場合 NOTHUMBNAIL を参照するようになっています。  
AssetLibrary/upload_form/static/files/thumbnail
