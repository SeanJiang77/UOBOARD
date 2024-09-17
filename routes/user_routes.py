from flask import render_template
from flask_login import login_required, current_user
from . import user_bp


@user_bp.route('/dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html', user=current_user)