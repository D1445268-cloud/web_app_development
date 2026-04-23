from flask import Blueprint, render_template, request, redirect, url_for

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def home():
    """
    首頁：顯示所有公開食譜，最新發表在前
    輸入：無
    邏輯：呼叫 recipe.get_all_public_recipes()
    輸出：渲染 index.html
    """
    pass

@index_bp.route('/search')
def search():
    """
    一般關鍵字搜尋：透過 query parameter ?q=關鍵字 搜尋食譜
    輸入：URL 參數 q
    邏輯：呼叫 recipe.search_recipes_by_keyword(q)
    輸出：渲染 index.html
    """
    pass

@index_bp.route('/combo-search')
def combo_search():
    """
    食材組合搜尋：透過 query parameter ?ingredients=A,B 反向搜尋食譜
    輸入：URL 參數 ingredients (以逗號分隔)
    邏輯：呼叫 recipe.search_recipes_by_ingredients(list)
    輸出：渲染 index.html
    """
    pass
