from flask import Flask, render_template, url_for, request, redirect, flash,\
    send_from_directory, current_app, send_from_directory
from app import app, faiss_index, sent_bert, write_to_html, write_to_db
from app.forms import TitleLink
from app.models import Paper, User
from app.forms import LoginForm
from app.utils import vector_search, allowed_file
from app.config import Config as cf
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import case
import os
from os.path import join
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@login_required
def index():
    return render_template("searchpage.html")


@app.route('/process', methods=["POST", "GET"])
@login_required
def process():
    if request.method == 'POST':
        query_form = request.form['query'].strip()
        query_arg = ''
    else:
        query_arg = request.args.get('query').strip()
        query_form = ''
    query = query_form if query_form != '' else query_arg
    if query:
        # Get paper IDs
        distances, ids = vector_search([query], sent_bert, faiss_index,
                                       cf.TOPK, cf.THRESHOLD)
        ids_dis = {ids[i]: distances[i] for i in range(len(ids))}
        # print(ids)
        ids_order = case({id: index for index, id in enumerate(ids)}, value=Paper.id)
        page = request.args.get('page', default=1, type=int)
        if ids:
            papers = Paper.query.filter(Paper.id.in_(ids)).order_by(ids_order).paginate(page=page, per_page=cf.ROWS_PER_PAGE)
        else:
            papers = None
        return render_template("results.html", papers=papers,
                               ids_dis=ids_dis, query_form=query_form,
                               query_arg=query_arg, show_score=cf.SHOW_SCORE)


@app.route('/document', methods=['GET', 'POST'])
@login_required
def document():
    # return redirect(url_for('document', filename='document.html'))
    return render_template("document.html")


@app.route('/static/docs/<path:filename>', methods=['GET', 'POST'])
@login_required
def download_file(filename):
    doc_path = join(current_app.root_path, "static/docs")
    return send_from_directory(doc_path, filename=filename,
                               as_attachment=True)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        for key, file in request.files.items():
            if key.startswith('file'):
                filename = secure_filename(file.filename)
                filepath = join(cf.UPLOAD_FOLDER, filename)
                file.save(filepath)
                write_to_db(filepath, cf.PATH_TO_DB, cf.PATH_TO_FAISS,
                            sent_bert, cf.PARSER_WIN, cf.PARSER_MAX_WORDS, cf.DOMAIN, faiss_index)
                write_to_html(filepath)
        return "indexs are update"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/login'))


if __name__ == '__main__':
    pass


