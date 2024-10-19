import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# .envファイルの環境変数をロード
load_dotenv()

app = Flask(__name__)

# HerokuのPostgreSQLデータベースURLを設定（環境変数を使用して安全に取得可能）
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
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
