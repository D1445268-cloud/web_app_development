from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import recipe

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def home():
    """
    首頁：顯示所有公開食譜，最新發表在前
    """
    recipes = recipe.get_all_public_recipes()
    return render_template('index.html', recipes=recipes)

@index_bp.route('/search')
def search():
    """
    一般關鍵字搜尋：透過 query parameter ?q=關鍵字 搜尋食譜
    """
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index.home'))
    
    recipes = recipe.search_recipes_by_keyword(query)
    return render_template('index.html', recipes=recipes, search_query=query)

@index_bp.route('/combo-search')
def combo_search():
    """
    食材組合搜尋：透過 query parameter ?ingredients=A,B 反向搜尋食譜
    """
    ingredients_param = request.args.get('ingredients', '').strip()
    if not ingredients_param:
        return redirect(url_for('index.home'))
    
    # 將逗號分隔的字串拆分為陣列，並去除空白
    ingredient_list = [ing.strip() for ing in ingredients_param.split(',') if ing.strip()]
    
    if not ingredient_list:
        flash('請輸入有效的食材名稱', 'warning')
        return redirect(url_for('index.home'))
        
    recipes = recipe.search_recipes_by_ingredients(ingredient_list)
    return render_template('index.html', recipes=recipes, combo_ingredients=ingredient_list)
