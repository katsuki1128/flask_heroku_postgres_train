## 仮想環境で作成したFlaskアプリをHeroku上でPostgreSQLを利用してデプロイする
VSCodeでのプレビューはCmd + Shift + V

### ターミナルで実行
```zsh
mkdir flask-app
cd flask-app

python3 -m venv venv
source venv/bin/activate

pip install flask gunicorn flask-sqlalchemy psycopg2-binary

touch .gitignore
echo "venv/" > .gitignore

touch app.py Procfile
echo "web: gunicorn app:app --log-file=-" > Procfile
pip freeze > requirements.txt

mkdir templates
touch templates/index.html

```

### `app.py` を作成

```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# HerokuのPostgreSQLデータベースURLを設定（環境変数を使用して安全に取得可能）
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u338a7ka27i73q:p7320f0260cfc56fdf05d5df29ae336ab62e38bafb5af4ab2be45dc9606641f2a@cat670aihdrkt1.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dmkcc4snini1q'

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
```
### herokuでログイン操作
### herokuでデプロイ

```zsh
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

・Heroku PostgresのAdd-onページへ行くので、Settingタブを開き、View Credentialsボタンを押す

・すると、PostgreSQLのHostやUsername, Passwordの情報が表示されるので、このデータベースに接続する場合は、こちらの情報へアクセス

```zsh
heroku pg:info --app whispering-brook-31241
```
でデータベース情報が出てくればOK
```zsh
=== DATABASE_URL

Plan:                  essential-0
Status:                Available
Connections:           0/20
PG Version:            16.3
Created:               2024-10-19 05:39 
Data Size:             7.66 MB / 1 GB (0.75%) (In compliance)
Tables:                0/4000 (In compliance)
Fork/Follow:           Unsupported
Rollback:              Unsupported
Continuous Protection: Off
Add-on:                postgresql-solid-24318
```

### PostgreSQLへアクセス
下記コマンドでHerokuのPostgreSQLに直接アクセスすることができる
```zsh
heroku pg:psql --app whispering-brook-31241
```

Heroku 上の Postgres データベースは自動的に作成される。

Postgres でテーブルを作成するには、CREATE TABLE SQL ステートメントを使う。

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
テーブルが正常に作成されたら、users テーブルにデータを挿入できる。
```sql
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
```
テーブルの内容を確認するには：
```sql
SELECT * FROM users;
```
下記でpsql セッションを終了する（データベースから抜ける）
```zsh
\q
```

psql セッションを開始する。
```zsh
heroku login
heroku pg:psql --app whispering-brook-31241
```


### app.py でデータベースの情報を取得して表示

```zsh
pip install SQLAlchemy psycopg2-binary flask-sqlalchemy
pip freeze > requirements.txt

```
・`SQLAlchemy`: データベース ORM

・`psycopg2-binary`: PostgreSQL に接続するためのドライバ

`app.py` に以下のコードを追加する。

```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Heroku PostgresのデータベースURLを設定 (環境変数またはHerokuから取得可能)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname:port/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Userモデルを定義
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

# ルートURLでユーザーデータを表示する
@app.route('/')
def index():
    users = User.query.all()  # 全てのユーザーデータを取得
    return render_template('index.html', users=users)  # テンプレートにデータを渡す

if __name__ == '__main__':
    app.run(debug=True)

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