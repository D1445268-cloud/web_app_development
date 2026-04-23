from . import get_db_connection

def create_recipe(user_id, title, ingredients, steps, image_url=None, category=None, is_public=True):
    """
    新增食譜
    """
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
    conn.close()
    return recipe_id

def get_recipe_by_id(recipe_id):
    """
    透過 ID 取得食譜
    """
    conn = get_db_connection()
    recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    conn.close()
    return recipe

def get_all_public_recipes():
    """
    取得所有公開食譜 (最新發表在前)
    """
    conn = get_db_connection()
    recipes = conn.execute(
        "SELECT * FROM recipes WHERE is_public = 1 ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return recipes

def get_recipes_by_user(user_id):
    """
    取得某位使用者的所有食譜 (包含私人)
    """
    conn = get_db_connection()
    recipes = conn.execute(
        "SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC", 
        (user_id,)
    ).fetchall()
    conn.close()
    return recipes

def update_recipe(recipe_id, title, ingredients, steps, image_url, category, is_public):
    """
    更新食譜內容
    """
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
    conn.close()

def delete_recipe(recipe_id):
    """
    刪除食譜
    """
    conn = get_db_connection()
    conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()

def search_recipes_by_keyword(keyword):
    """
    透過關鍵字搜尋食譜標題與食材 (僅限公開)
    """
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
    conn.close()
    return recipes

def search_recipes_by_ingredients(ingredient_list):
    """
    透過多個食材名稱反向搜尋食譜 (僅限公開)
    找出食材包含於給定陣列中的食譜。
    為了簡單實作 MVP，這裡使用 LIKE 搭配 OR 或 AND。
    這裡採取：只要包含任一種食材，就將其列出，
    未來可根據匹配程度排序。
    """
    if not ingredient_list:
        return []
    
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
    conn.close()
    return recipes
