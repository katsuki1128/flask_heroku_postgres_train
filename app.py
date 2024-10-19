import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# .envファイルの環境変数をロード
load_dotenv()

app = Flask(__name__)

# 環境変数からそれぞれの値を取得
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

# データベースの接続URLを作成
database_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"

# HerokuのPostgreSQLデータベースURLを設定（環境変数を使用して安全に取得可能）
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     "postgresql://udeh3ob4qehaoq:pf6aec7f90ddbfe0023612e8fbaf30a2ca0264155ff950f5fce8713e358f07124@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d543itvghq5f5j"
# )
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Userモデルを定義
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


# ルートURLでユーザーデータを表示
@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)
