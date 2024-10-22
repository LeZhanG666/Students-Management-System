from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from functools import wraps
from models import User

login_manager = LoginManager()

def init_login_manager(app: Flask):
    login_manager.init_app(app)
    login_manager.login_view = "/login"  # 指定登录视图

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def role_required(role):
    """检查用户角色的装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                return redirect(url_for('auth.login'))  # 或者重定向到 403 页面
            return f(*args, **kwargs)
        return decorated_function
    return decorator
