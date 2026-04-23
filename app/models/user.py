from . import get_db_connection

def create_user(username, email, password_hash, role='user'):
    """
    建立新使用者並寫入資料庫
    回傳新建立的 user_id，若 email 已存在則可能拋出 sqlite3.IntegrityError
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
        (username, email, password_hash, role)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user_by_id(user_id):
    """
    透過 ID 取得使用者
    回傳 dict-like 的 Row 物件，找不到則回傳 None
    """
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    """
    透過 Email 取得使用者 (用於登入驗證)
    回傳 dict-like 的 Row 物件，找不到則回傳 None
    """
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def get_user_by_username(username):
    """
    透過 Username 取得使用者
    回傳 dict-like 的 Row 物件，找不到則回傳 None
    """
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def get_all_users():
    """
    取得所有使用者 (用於後台管理)
    回傳 list of Row 物件
    """
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return users

def update_user_role(user_id, new_role):
    """
    更新使用者角色
    """
    conn = get_db_connection()
    conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """
    刪除使用者 (需注意外鍵關聯，若刪除使用者可能也須刪除他的食譜)
    """
    conn = get_db_connection()
    # 這裡實作直接刪除，未來可考慮實作 soft delete 或 cascade delete
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
