import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊頁面與處理註冊邏輯
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 基本驗證
        if not username or not email or not password or not confirm_password:
            flash('所有欄位皆為必填！', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('兩次輸入的密碼不一致！', 'danger')
            return render_template('auth/register.html')
        
        # 檢查 email 是否已被註冊
        existing_user = user.get_user_by_email(email)
        if existing_user:
            flash('此 Email 已經註冊過了！', 'danger')
            return render_template('auth/register.html')

        # 建立使用者
        password_hash = generate_password_hash(password)
        user_id = user.create_user(username, email, password_hash)
        
        if user_id:
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，請稍後再試。', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入頁面與處理登入邏輯
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('請輸入 Email 與密碼！', 'danger')
            return render_template('auth/login.html')

        user_record = user.get_user_by_email(email)
        
        if user_record and check_password_hash(user_record['password_hash'], password):
            session.clear()
            session['user_id'] = user_record['id']
            session['username'] = user_record['username']
            flash('登入成功！', 'success')
            return redirect(url_for('index.home'))
        else:
            flash('登入失敗：Email 或密碼錯誤。', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    登出處理邏輯
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('index.home'))
