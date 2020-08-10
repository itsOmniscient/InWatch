
import os
from flask import render_template, flash, redirect, url_for, request
from movies_webstore import app, db, bcrypt
from movies_webstore.forms import RegistrationForm, LoginForm
from movies_webstore.models import User
from tmdbv3api import TMDb, Movie
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json

tmdb = TMDb()
tmdb.api_key = os.getenv("api_key")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_route():
    movie = Movie()
    return render_template('index.html', movie=movie)

@app.route('/register', methods=['GET', 'POST'])
def registration_route():
    if current_user.is_authenticated:
        return redirect(url_for('home_route'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_route'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('home_route'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.button.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_route'))
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_route():
    logout_user()
    return redirect(url_for('home_route'))

@app.route('/account')
@login_required
def user_profile():
    return render_template('account.html')

@app.route("/movie/<movie_id>/", methods=['GET', 'POST'])
@login_required
def movie_route(movie_id):
    movie = Movie()
    m_detail = movie.details(movie_id)
    api_key = tmdb.api_key
    r = requests.get('https://api.themoviedb.org/3/movie/'+str(movie_id) +str('?api_key=') +str(api_key))
    j = r.json()
    genre = j['genres'][0]['name']
    return render_template('movie.html', movie=movie, m_detail=m_detail, genre=genre)

@app.route('/search/<term>', methods=['GET', 'POST'])
def search_route(term):
    movie = Movie()
    m_search = movie.search(term)
    return render_template('search.html', movie=movie, m_search=m_search)

@app.route('/category', methods=['GET', 'POST'])
def category_route():
    movie = Movie()
    return render_template('categories.html', movie=movie)
