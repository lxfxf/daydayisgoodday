from . import main
from flask import render_template, flash, redirect, url_for, request, current_app
from flask.ext.login import login_required
from forms import PostForm, CommentForm
from ..models import Post, Comment
from .. import db 

@main.route('/')
@main.route('/index')
def index():
	page = request.args.get('page', 1, type = int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page = current_app.config['POSTS_PER_PAGE'], 
		error_out = False)
	posts = pagination.items
	title = "Blogs"
	return render_template('index.html', posts = posts, title = title,
		pagination = pagination)


@main.route('/write', methods = ['GET', 'POST'])
@login_required
def write():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body = form.body.data)
		db.session.add(post)
		flash('You have successed publishing a blog! Forgive my poor English!')
		return redirect(url_for('.index'))
	return render_template('write.html', form = form)

@main.route('/post/<int:id>', methods = ['GET', 'POST'])
def post(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(body = form.body.data,
						  post = post,
						  weibo_id = 1)
		db.session.add(comment)
		flash('Your comment has been published.')
		return redirect(url_for('.post', id = post.id, page = -1))
	page = request.args.get('page', 1, type = int)
	if page == -1:
		page = (post.comments.count() - 1) / current_app.config['COMMENTS_PER_PAGE']
	pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
								page,
								per_page = current_app.config['COMMENTS_PER_PAGE'],
								error_out = False)
	comments = pagination.items
	return render_template('post.html', posts = [post])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)
