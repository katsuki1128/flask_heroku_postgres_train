## 仮想環境で作成したFlaskアプリをHeroku上でPostgreSQLを利用してデプロイする
VSCodeでのプレビューはCmd + Shift + V

### ターミナルで実行
```zsh
mkdir flask-app
cd flask-app

python3 -m venv venv
source venv/bin/activate

pip install flask gunicorn flask-sqlalchemy psycopg2-binary python-dotenv

touch .gitignore
echo -e "venv/\n.env" > .gitignore


touch app.py Procfile
echo "web: gunicorn app:app --log-file=-" > Procfile
pip freeze > requirements.txt

mkdir templates
touch templates/index.html

touch .env


```

### `app.py` を作成

```python
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# .envファイルの環境変数をロード
load_dotenv()

# 環境変数からそれぞれの要素を取得
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
dbname = os.getenv('DB_NAME')

# それらを結合して DATABASE_URL を作成
database_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"

app = Flask(__name__)

# HerokuのPostgreSQLデータベースURLを設定（環境変数を使用して安全に取得可能）
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Userモデルを定義
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

# ルートURLでユーザーデータを表示
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
```

### `index.html`テンプレートを作成
ユーザー情報を表示するためのHTMLテンプレートを `templates/index.html` ファイルに作成.
```html
<!-- templates/index.html -->

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Users</title>
</head>
<body>
    <h1>User List</h1>
    <ul>
        {% for user in users %}
            <li>{{ user.name }} ({{ user.email }}) - Created at: {{ user.created_at }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

### ターミナルで実行
```zsh
git init
git add .
git commit -m "first commit"
heroku login
heroku create
git push heroku main
heroku open
```
### githubでリポジトリを作って連携 
#### https://github.com/new にアクセスして新しいリポジトリを作成
🔽<>内を書き換える

```zsh
git remote add origin <git@github.com:katsuki1128/heroku_test.git>
git add .
git commit -m "github"
git push origin main
```

### herokuのプロジェクトページの「Deploy」内で「GitHub Connect to GitHub」でリポジトリをサーチしてconnect。
Enable Automatic Deploysをクリック
以降は
```zsh
git add .
git commit -m "github"
git push origin main
```
でpushされた内容が
```zsh
heroku open
```
で開くサイトに公開される。

### heroku PostgresSQLとの連携
🔽参考サイト
https://k-sasaking.net/programing/heroku-postgres-install/

・herokuのアプリの画面⇨Resources⇨Add-ons⇨「postgres」を入力して、Heroku Postgresが表示されたらクリック

・Add-onsの検索バーに “postgres“を入力をしたら、Heroku Postgresが表示されるので、クリック

・Heroku PostgresのAddonのプランを選択

・herokuアプリのOverview画面から先ほど追加したHeroku PostgresのAdd-onを開く

### .envファイルの作成、HerokuのPostgreSQLに直接アクセス

・Heroku PostgresのAdd-onページへ行くので、Settingタブを開き、View Credentialsボタンを押す。

・すると、PostgreSQLのHostやUsername, Passwordの情報が表示されるので、このデータベースに接続する場合は、こちらの情報へアクセス。`URI`と`Heroku CLI`を確認。

`URI`を下記に入れ、ターミナルで`Heroku CLI`を実行。
HerokuのPostgreSQLに直接アクセスすることができる

>`URI`は`postgresql://User:Password@Host:Port/Database`に以下５つを組み入れたもの。

>`User` `Password` `Host` `Port` `Database`

>`Heroku CLI`は下記のような形式：heroku pg:psql postgresql-solid-90670 --app boiling-escarpment-01091

```zsh
DATABASE_URL=<URI>
<Heroku CLI>
```


### テーブルの作成

Heroku 上の Postgres データベースは自動的に作成される。

Postgres でテーブルを作成するには、CREATE TABLE SQL ステートメントを使う。

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (name, email) VALUES ('test_user', 'test@example.com');
SELECT * FROM users;
```
下記でpsql セッションを終了する（データベースから抜ける）
```zsh
\q
```

psql セッションを開始する。
```zsh
heroku login
heroku pg:psql --app <herokuアプリケーション名>
```


```zsh
git add .
git commit -m "github"
git push origin main
```
でpushして、下記で確認。
```zsh
heroku open
```

git add .
git commit -m "connect"
git push origin main
heroku open