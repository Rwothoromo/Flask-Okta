# third party imports
from flask import Blueprint, abort, flash, g, render_template, redirect, request, url_for
from slugify import slugify

# local imports
from blog.cache import cache
from blog.auth.controllers import oidc, okta_client
from ..db import db
from ..models.post import Post


main = Blueprint('main', __name__)


@main.route("/")
@cache.cached(300, key_prefix='display_posts')
def index():
    """Render the homepage."""

    posts = Post.query.order_by(Post.created.desc())

    posts_final = []
    for post in posts:
        user = okta_client.get_user(post.author_id)
        post.author_name = user.profile.firstName + " " + user.profile.lastName
        posts_final.append(post)

    return render_template("blog/index.html", posts=posts_final)


def get_posts(author_id):
    """Return all posts by this author, ordered (descending) by date."""

    return Post.query.filter_by(author_id=author_id).order_by(Post.created.desc())


@main.route("/dashboard", methods=["GET", "POST"])
@oidc.require_login
def dashboard():
    """Render user's dashboard."""

    if request.method == "GET":
        return render_template("blog/dashboard.html", posts=get_posts(g.user.id))

    title = request.form["title"]
    error = None

    if not title:
        error = 'Title is required.'

    if error is not None:
        flash(error)
    else:
        body = request.form["body"]

        # a blog post titled “Day out in Moscow” can have a slug 'day-out-in-moscow'
        # and be available at https://someblog.com/day-out-in-moscow
        slug = slugify(title)

        # create a blog post from the dashboard
        post = Post(
            title=title,
            body=body,
            author_id=g.user.id,
            slug=slug
        )

        db.session.add(post)
        db.session.commit()

        # reset the cache
        cache.delete('display_posts')

    return render_template("blog/dashboard.html", posts=get_posts(g.user.id))


@main.route("/<slug>")
def view_post(slug):
    """View a post based off slug URL."""

    post = Post.query.filter_by(slug=slug).first()
    if not post:
        abort(404)

    user = okta_client.get_user(post.author_id)
    post.author_name = user.profile.firstName + " " + user.profile.lastName

    return render_template("blog/post.html", post=post)


@main.route("/<slug>/edit", methods=["GET", "POST"])
def edit_post(slug):
    """Edit a post based off the slug URL."""

    post = Post.query.filter_by(slug=slug).first()
    if not post:
        abort(404)

    if post.author_id != g.user.id:
        abort(403)

    # details of logged in user
    post.author_name = g.user.profile.firstName + " " + g.user.profile.lastName
    if request.method == "GET":
        return render_template("blog/edit.html", post=post)

    title = request.form["title"]
    error = None

    if not title:
        error = 'Title is required.'

    if error is not None:
        flash(error)
    else:
        body = request.form["body"]
        slug = slugify(title)

        post.title = title
        post.body = body
        post.slug = slug

        db.session.commit()

        # reset the cache
        cache.delete('display_posts')

    return redirect(url_for(".view_post", slug=post.slug))


@main.route("/<slug>/delete", methods=["POST"])
def delete_post(slug):
    """Delete a post based off the slug URL."""

    post = Post.query.filter_by(slug=slug).first()
    if not post:
        abort(404)

    if post.author_id != g.user.id:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    # reset the cache
    cache.delete('display_posts')

    return redirect(url_for(".dashboard"))
