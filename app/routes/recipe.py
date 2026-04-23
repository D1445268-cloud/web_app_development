from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.models import recipe

recipe_bp = Blueprint('recipe', __name__)

def login_required(f):
    """
    登入驗證的裝飾器
    保護需要登入才能存取的路由
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入系統才能進行此操作！', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@recipe_bp.route('/<int:id>')
def detail(id):
    """
    查看單筆食譜詳細內容
    """
    recipe_data = recipe.get_recipe_by_id(id)
    if not recipe_data:
        abort(404)
        
    # 如果是私人食譜，檢查是否有權限
    if not recipe_data['is_public']:
        if 'user_id' not in session or session['user_id'] != recipe_data['user_id']:
            flash('您沒有權限查看此私人食譜。', 'danger')
            return redirect(url_for('index.home'))
            
    return render_template('recipe/detail.html', recipe=recipe_data)

@recipe_bp.route('/my-recipes')
@login_required
def my_recipes():
    """
    個人食譜管理面板
    """
    user_id = session['user_id']
    recipes = recipe.get_recipes_by_user(user_id)
    return render_template('recipe/my_recipes.html', recipes=recipes)

@recipe_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    """
    新增食譜頁面與處理送出
    """
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        image_url = request.form.get('image_url')
        category = request.form.get('category')
        is_public = request.form.get('is_public') == 'on'  # Checkbox value
        
        if not title or not ingredients or not steps:
            flash('食譜標題、食材清單與製作步驟皆為必填！', 'danger')
            # 將已填資料保留回傳（暫不實作複雜保留邏輯，交由前端處理或直接回傳）
            return render_template('recipe/form.html', action='new')
            
        recipe_id = recipe.create_recipe(
            user_id=session['user_id'],
            title=title,
            ingredients=ingredients,
            steps=steps,
            image_url=image_url,
            category=category,
            is_public=is_public
        )
        
        if recipe_id:
            flash('食譜新增成功！', 'success')
            return redirect(url_for('recipe.detail', id=recipe_id))
        else:
            flash('新增失敗，請稍後再試。', 'danger')
            
    return render_template('recipe/form.html', action='new')

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    """
    編輯食譜頁面與處理更新
    """
    recipe_data = recipe.get_recipe_by_id(id)
    if not recipe_data:
        abort(404)
        
    # 檢查權限
    if recipe_data['user_id'] != session['user_id']:
        flash('您只能編輯自己的食譜！', 'danger')
        return redirect(url_for('recipe.my_recipes'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        image_url = request.form.get('image_url')
        category = request.form.get('category')
        is_public = request.form.get('is_public') == 'on'
        
        if not title or not ingredients or not steps:
            flash('食譜標題、食材清單與製作步驟皆為必填！', 'danger')
            return render_template('recipe/form.html', action='edit', recipe=recipe_data)
            
        success = recipe.update_recipe(
            recipe_id=id,
            title=title,
            ingredients=ingredients,
            steps=steps,
            image_url=image_url,
            category=category,
            is_public=is_public
        )
        
        if success:
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=id))
        else:
            flash('更新失敗，請稍後再試。', 'danger')
            
    return render_template('recipe/form.html', action='edit', recipe=recipe_data)

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    """
    刪除單篇食譜
    """
    recipe_data = recipe.get_recipe_by_id(id)
    if not recipe_data:
        abort(404)
        
    # 檢查權限 (實務上可以增加 admin 權限檢查，此處僅檢查擁有者)
    if recipe_data['user_id'] != session['user_id']:
        flash('您只能刪除自己的食譜！', 'danger')
        return redirect(url_for('recipe.my_recipes'))
        
    success = recipe.delete_recipe(id)
    if success:
        flash('食譜已刪除。', 'success')
    else:
        flash('刪除失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('recipe.my_recipes'))
