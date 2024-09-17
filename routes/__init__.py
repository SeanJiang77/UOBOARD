from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__)
auth_bp = Blueprint('auth_bp', __name__)
user_bp = Blueprint('user_bp', __name__)

# 在这里引入各自的routes文件
from . import admin_routes, auth_routes, user_routes