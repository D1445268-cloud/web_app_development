import sqlite3
from . import get_db_connection

def create_recipe(user_id, title, ingredients, steps, image_url=None, category=None, is_public=True):
    """
    新增食譜
    回傳新建立的 recipe_id，若發生錯誤則回傳 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO recipes (user_id, title, ingredients, steps, image_url, category, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (user_id, title, ingredients, steps, image_url, category, int(is_public))
        )
        conn.commit()
        recipe_id = cursor.lastrowid
        return recipe_id
    except sqlite3.Error as e:
        print(f"Error creating recipe: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_recipe_by_id(recipe_id):
    """
    透過 ID 取得食譜
    回傳 dict-like 的 Row 物件，找不到或錯誤則回傳 None
    """
    try:
        conn = get_db_connection()
        recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
        return recipe
    except sqlite3.Error as e:
        print(f"Error getting recipe by id: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_public_recipes():
    """
    取得所有公開食譜 (最新發表在前)
    回傳 list of Row 物件，錯誤則回傳空陣列
    """
    try:
        conn = get_db_connection()
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE is_public = 1 ORDER BY created_at DESC"
        ).fetchall()
        return recipes
    except sqlite3.Error as e:
        print(f"Error getting all public recipes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_recipes_by_user(user_id):
    """
    取得某位使用者的所有食譜 (包含私人)
    回傳 list of Row 物件，錯誤則回傳空陣列
    """
    try:
        conn = get_db_connection()
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC", 
            (user_id,)
        ).fetchall()
        return recipes
    except sqlite3.Error as e:
        print(f"Error getting recipes by user: {e}")
        return []
    finally:
        if conn:
            conn.close()

def update_recipe(recipe_id, title, ingredients, steps, image_url, category, is_public):
    """
    更新食譜內容
    成功回傳 True，失敗回傳 False
    """
    try:
        conn = get_db_connection()
        conn.execute(
            '''
            UPDATE recipes 
            SET title = ?, ingredients = ?, steps = ?, image_url = ?, category = ?, is_public = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (title, ingredients, steps, image_url, category, int(is_public), recipe_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating recipe: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_recipe(recipe_id):
    """
    刪除食譜
    成功回傳 True，失敗回傳 False
    """
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting recipe: {e}")
        return False
    finally:
        if conn:
            conn.close()

def search_recipes_by_keyword(keyword):
    """
    透過關鍵字搜尋食譜標題與食材 (僅限公開)
    回傳 list of Row 物件，錯誤則回傳空陣列
    """
    try:
        conn = get_db_connection()
        search_term = f"%{keyword}%"
        recipes = conn.execute(
            '''
            SELECT * FROM recipes 
            WHERE is_public = 1 AND (title LIKE ? OR ingredients LIKE ?)
            ORDER BY created_at DESC
            ''',
            (search_term, search_term)
        ).fetchall()
        return recipes
    except sqlite3.Error as e:
        print(f"Error searching recipes by keyword: {e}")
        return []
    finally:
        if conn:
            conn.close()

def search_recipes_by_ingredients(ingredient_list):
    """
    透過多個食材名稱反向搜尋食譜 (僅限公開)
    回傳 list of Row 物件，錯誤則回傳空陣列
    """
    if not ingredient_list:
        return []
    
    try:
        conn = get_db_connection()
        
        # 建立 LIKE 條件，例如: ingredients LIKE '%雞肉%' OR ingredients LIKE '%洋蔥%'
        conditions = " OR ".join(["ingredients LIKE ?"] * len(ingredient_list))
        # 準備參數
        params = [f"%{ing}%" for ing in ingredient_list]
        
        query = f'''
            SELECT * FROM recipes 
            WHERE is_public = 1 AND ({conditions})
            ORDER BY created_at DESC
        '''
        
        recipes = conn.execute(query, params).fetchall()
        return recipes
    except sqlite3.Error as e:
        print(f"Error searching recipes by ingredients: {e}")
        return []
    finally:
        if conn:
            conn.close()
