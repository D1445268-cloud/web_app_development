import os
from flask import Flask
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def create_app():
    # 建立 Flask 實例，因為 main.py 在外層，需要手動指定 templates 與 static 的路徑
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 設定 SECRET_KEY，用於 Session 與 CSRF 防護
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_default_secret_key')

    # 註冊所有的 Blueprints
    from app.routes import init_app
    init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
