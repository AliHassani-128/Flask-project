import json
import functools
from flask import Blueprint, session
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from myblog.db import get_db

bp = Blueprint("blog", __name__)


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().user.find_one({"_id": ObjectId(user_id)})


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view



#Home page of site that show all posts
@bp.route("/")
def home():
    db = get_db()
    posts = db.posts.find()
    categories=db.categories.find()
    subcategories=db.subcategories.find()
    return render_template('all_posts.html', posts=list(posts),categories=categories,subcategories=list(subcategories))


#for showing all detail of one post
@bp.route("/post/<post_id>/")
def post(post_id):
    db = get_db()
    post = db.posts.find({'_id': ObjectId(post_id)})
    return render_template('detail_post.html', posts=list(post))



@bp.route("/category-posts/<category_id>/")
def category(category_id):
    return render_template('')


@bp.route("/tag-posts/<tag_id>")
def tag(tag_id):
    return render_template('')



#for register a new user to site
@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get('email')
        phone = request.form.get('phone')
        image = request.files.get('image')
        error = None
        if image:
            image.save('myblog/static/media/uploads/profiles/' +
                       secure_filename(image.filename))
        else:

            error = 'عکس برای پنل کاربری خود انتخاب نکردید'
        db = get_db()


        if not username:
            error = "نام کاربری الزامی است"
        elif not password:
            error = "رمز عبور الزامی است"
        elif db.user.find_one({"username": username}) is not None:
            error = f"وجود دارد.لطفا نام دیگری انتخاب کنید {username} نام کاربری"

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            user = {'username': username, 'password': generate_password_hash(password),
                    'email': email, 'phone': phone, 'image': image.filename}
            db.user.insert_one(user)
            flash('پنل کاربری شما با موفقیت ثبت شد','alert-success')
            return redirect(url_for("blog.login"))
        else:
            flash(error, "alert-danger")

    return render_template("auth/register.html")

#for login users who were registered
@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        user = db.user.find_one({"username": username})

        if not username:
            error = "! نام کاربری وارد نشده است "
        elif not password:
            error = "! رمز عبور وارد نشده است "
        else:
            if user is None:
                error = 'کاربری با این مشخصات وجود ندارد'
            elif not check_password_hash(user["password"], password):
                error = "! رمز عبور نادرست است"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            user['_id'] = str(user['_id'])
            session["user_id"] = user["_id"]
            flash(f"عزیز،خوش آمدید {user['username']} ", "alert-success")
            return redirect(url_for("blog.home"))
        else:
            flash(error, "alert-danger")

    return render_template("auth/login.html")

#for shoiwng all posts that a user with id (user_id) was written
@bp.route('/user-posts/<user_id>/')
def user_posts(user_id):
    posts = get_db().posts.find({'user._id': ObjectId(user_id)})
    return render_template('all_posts.html', posts=list(posts))


#for shoiwng all posts that are with a common tag
@bp.route('/tag-posts/<tag>/')
def tag_posts(tag):
    posts = get_db().posts.find({'tag': {'$in':[tag]}})
    return render_template('all_posts.html', posts=list(posts))

#like a post
@bp.route('/like/',methods=['POST'])
def like():

    post_id = request.args.get('post_id')
    user_id = request.args.get('user_id')

    post = get_db().posts.find_one({'_id':ObjectId(post_id)})

    if user_id :
        if ObjectId(user_id) not in post['like']:

            get_db().posts.update({ '_id':ObjectId(post_id)},{ '$push': { 'like': ObjectId(user_id)} })
            likes= list(get_db().posts.aggregate(
                                           [{'$match':{'_id':ObjectId(post_id)}},
                                               {'$project':
                                                 {'like':{'$size':'$like'}}}
                                            ]))[0]
            return json.dumps({'likes':likes['like'],'color':'red'})
        else:
            get_db().posts.update({'_id': ObjectId(post_id)}, {'$pull': {'like': ObjectId(user_id)}})
            likes = list(get_db().posts.aggregate(
                [{'$match': {'_id': ObjectId(post_id)}},
                 {'$project':
                      {'like': {'$size': '$like'}}}
                 ]))[0]
            return json.dumps({'likes': likes['like'],'color':'lightslategray'})
    else:
        return json.dumps({'error': 'برای لایک کردن پست ها باید کاربر سایت باشید'})

#dislike a post
@bp.route('/dislike/',methods=['POST'])
def dislike():
    post_id = request.args.get('post_id')
    user_id = request.args.get('user_id')

    post = get_db().posts.find_one({'_id': ObjectId(post_id)})

    if user_id:
        if ObjectId(user_id) not in post['dislike']:

            get_db().posts.update({'_id': ObjectId(post_id)}, {'$push': {'dislike': ObjectId(user_id)}})
            dislikes = list(get_db().posts.aggregate(
                [{'$match': {'_id': ObjectId(post_id)}},
                 {'$project':
                      {'dislike': {'$size': '$dislike'}}}
                 ]))[0]
            return json.dumps({'dislikes': dislikes['dislike']})
        else:
            get_db().posts.update({'_id': ObjectId(post_id)}, {'$pull': {'dislike': ObjectId(user_id)}})
            dislikes = list(get_db().posts.aggregate(
                [{'$match': {'_id': ObjectId(post_id)}},
                 {'$project':
                      {'dislike': {'$size': '$dislike'}}}
                 ]))[0]
            return json.dumps({'dislikes': dislikes['dislike']})
    else:
        return json.dumps({'error': 'برای نپسندیدن پست ها باید کاربر سایت باشید'})


