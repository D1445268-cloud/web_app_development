from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊頁面與處理註冊邏輯
    輸入：表單 username, email, password, confirm_password
    邏輯：驗證資料後呼叫 user.create_user()，成功則導向登入頁面
    輸出：渲染 auth/register.html 或重導向 /auth/login
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入頁面與處理登入邏輯
    輸入：表單 email, password
    邏輯：呼叫 user.get_user_by_email() 驗證，成功則將 user_id 存入 session
    輸出：渲染 auth/login.html 或重導向首頁 /
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    登出處理邏輯
    輸入：無
    邏輯：清除 session 中的 user_id
    輸出：重導向首頁 /
    """
    pass
