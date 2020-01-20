# AssetLibrary について

python3 の Django を使ったアセット共有 WEB アプリケーションです。

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
ディレクトリがないとエラーになるので空のフォルダを作成する必要があります。
upload_form/static/files

下記のディレクトリにアップロードしたサムネイルが保存されますサムネがない場合 None.jpg を参照するようになっています。  
upload_form/static/files/thumbnail
