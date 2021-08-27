import json
import pprint

from bson import ObjectId
from flask import Blueprint, session, jsonify
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from myblog.blog import login_required
from myblog.db import get_db

bp = Blueprint("api", __name__, url_prefix='/api/')

#for encoding an object to json
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@bp.route("/posts_list/")
def list_post():
    return render_template('')


@bp.route("/delete-post/<post_id>")
@login_required
def delete_post(post_id):
    get_db().posts.delete_one({'_id': ObjectId(post_id)})
    db = get_db()
    posts = db.posts.find()
    return JSONEncoder().encode(list(posts))


@bp.route("/post-deactive/<post_id>/")
def post_deactive(post_id):
    get_db().posts.update({'_id': ObjectId(post_id)},
                          {'$set': {'status': False}})
    db = get_db()
    posts = db.posts.find()
    return JSONEncoder().encode(list(posts))


@bp.route("/post-active/<post_id>/")
def post_active(post_id):
    get_db().posts.update({'_id': ObjectId(post_id)},
                          {'$set': {'status': True}})
    db = get_db()
    posts = db.posts.find()
    return JSONEncoder().encode(list(posts))


@bp.route("/search/", methods=['POST'])
def search():

    error = None
    if request.method == 'POST':
        input = request.data.decode("utf-8")
        posts = list(get_db().posts.find({'$or': [{'title': {'$regex': f'{input}'}}, {'content': {'$regex': f'{input}'}},
                                                  {'user.username': {
                                                      '$regex': f'{input}'}},
                                                  {'tag': {'$regex': f'{input}'}}]}))

        if len(posts) == 0:
            error = 'موردی یافت نشد'
            return json.dumps({'error': error})

        else:
            dict_posts = {str(post['_id']): [
                post['title'], post['image']] for post in list(posts)}

    return json.dumps(dict_posts)



@bp.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("blog.home"))
