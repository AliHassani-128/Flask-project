from flask import Blueprint, session
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from myblog.db import get_db


bp = Blueprint("api", __name__)


@bp.route("/posts_list/")
def list_post():
    return render_template('')



@bp.route("/post-delete/<post_id>/")
def post_delete(post_id):
    return render_template('')



@bp.route("/post-deactive/<post_id>/")
def post_deactive(post_id):
    return render_template('')


@bp.route("/categorys-list/")
def list_categorys():
    sub_categories=get_db().subcategory.find()
    return render_template('test.html',categories=sub_categories)


@bp.route("/tags-list/")
def list_tags():
    return render_template('')



@bp.route("/search/")
def search():
    return render_template('')



@bp.route("/user-profile/<user_id>/")
def user_profile(user_id):
    return render_template('')


@bp.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("blog.home"))
