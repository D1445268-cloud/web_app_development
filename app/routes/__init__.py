def init_app(app):
    """
    註冊所有的 Flask Blueprints
    """
    from .index import index_bp
    from .auth import auth_bp
    from .recipe import recipe_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp, url_prefix='/recipe')
