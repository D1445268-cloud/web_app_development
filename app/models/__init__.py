import sqlite3
import os

def get_db_connection():
    """
    建立並回傳一個 SQLite 資料庫連線。
    預設會連線到專案根目錄下的 instance/database.db
    """
    # 確保 instance 目錄存在
    instance_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    db_path = os.path.join(instance_dir, 'database.db')
    conn = sqlite3.connect(db_path)
    
    # 讓資料可以透過欄位名稱存取 (dict-like)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    使用 database/schema.sql 初始化資料庫
    """
    conn = get_db_connection()
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()
