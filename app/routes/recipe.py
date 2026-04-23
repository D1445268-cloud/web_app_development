from flask import Blueprint, render_template, request, redirect, url_for, session, flash

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/<int:id>')
def detail(id):
    """
    查看單筆食譜詳細內容
    輸入：URL Path 參數 id
    邏輯：呼叫 recipe.get_recipe_by_id(id)，若為私人需檢查 session user_id
    輸出：渲染 recipe/detail.html 或回傳 404/403
    """
    pass

@recipe_bp.route('/my-recipes')
def my_recipes():
    """
    個人食譜管理面板
    輸入：無（從 session 取得 user_id）
    邏輯：呼叫 recipe.get_recipes_by_user(user_id)
    輸出：渲染 recipe/my_recipes.html
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new_recipe():
    """
    新增食譜頁面與處理送出
    輸入：表單 title, ingredients, steps, image_url, category, is_public
    邏輯：接收並驗證表單，呼叫 recipe.create_recipe()
    輸出：成功後重導向至 /recipe/my-recipes，失敗則渲染 recipe/form.html
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯食譜頁面與處理更新
    輸入：URL Path 參數 id, 表單欄位
    邏輯：檢查使用者權限，接收並呼叫 recipe.update_recipe()
    輸出：成功後重導向至 /recipe/<id>，失敗則渲染 recipe/form.html
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除單篇食譜
    輸入：URL Path 參數 id
    邏輯：檢查使用者權限 (本人或 admin)，呼叫 recipe.delete_recipe(id)
    輸出：重導向至 /recipe/my-recipes
    """
    pass
