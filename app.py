import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# .envファイルの環境変数をロード
load_dotenv()

app = Flask(__name__)

# HerokuのPostgreSQLデータベースURLを設定（環境変数を使用して安全に取得可能）
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     "postgresql://udeh3ob4qehaoq:pf6aec7f90ddbfe0023612e8fbaf30a2ca0264155ff950f5fce8713e358f07124@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d543itvghq5f5j"
# )

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://u338a7ka27i73q:p7320f0260cfc56fdf05d5df29ae336ab62e38bafb5af4ab2be45dc9606641f2a@cat670aihdrkt1.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dmkcc4snini1q"
)
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
