from flask import render_template, redirect, url_for
from . import admin_bp
from models import db, Member, Game


@admin_bp.route('/admin31415926')
def admin_panel():
    members = Member.query.all()
    games = Game.query.all()
    return render_template('admin.html', members=members, games=games)


@admin_bp.route('/edit_member/<int:member_id>', methods=['POST'])
def edit_member(member_id):
    # 编辑成员信息的逻辑
    return redirect(url_for('admin_bp.admin_panel'))


@admin_bp.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
    return redirect(url_for('admin_bp.admin_panel'))


@admin_bp.route('/edit_game/<int:game_id>', methods=['POST'])
def edit_game(game_id):
    # 编辑游戏信息的逻辑
    return redirect(url_for('admin_bp.admin_panel'))


@admin_bp.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return redirect(url_for('admin_bp.admin_panel'))