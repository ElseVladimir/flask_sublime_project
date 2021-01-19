from flask import Blueprint, render_template, request
from models import Post

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/')
def index_blog():
    posts = Post.query.all()
    return render_template('blog/blog.html',posts=posts)

@blog.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    return render_template('blog/post_detail.html', post=post)