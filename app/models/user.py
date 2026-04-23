import sqlite3
from . import get_db_connection

def create_user(username, email, password_hash, role='user'):
    """
    建立新使用者並寫入資料庫
    回傳新建立的 user_id，若發生錯誤則回傳 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_by_id(user_id):
    """
    透過 ID 取得使用者
    回傳 dict-like 的 Row 物件，找不到或錯誤則回傳 None
    """
    try:
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error getting user by id: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_by_email(email):
    """
    透過 Email 取得使用者 (用於登入驗證)
    回傳 dict-like 的 Row 物件，找不到或錯誤則回傳 None
    """
    try:
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error getting user by email: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_by_username(username):
    """
    透過 Username 取得使用者
    回傳 dict-like 的 Row 物件，找不到或錯誤則回傳 None
    """
    try:
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error getting user by username: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_users():
    """
    取得所有使用者 (用於後台管理)
    回傳 list of Row 物件，錯誤則回傳空陣列
    """
    try:
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
        return users
    except sqlite3.Error as e:
        print(f"Error getting all users: {e}")
        return []
    finally:
        if conn:
            conn.close()

def update_user_role(user_id, new_role):
    """
    更新使用者角色
    成功回傳 True，失敗回傳 False
    """
    try:
        conn = get_db_connection()
        conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating user role: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_user(user_id):
    """
    刪除使用者
    成功回傳 True，失敗回傳 False
    """
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        if conn:
            conn.close()
