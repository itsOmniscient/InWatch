
import os
from flask import render_template, flash, redirect, url_for, request
from movies_webstore import app, db, bcrypt
from movies_webstore.forms import RegistrationForm, LoginForm
from movies_webstore.models import User
from tmdbv3api import TMDb, Movie, Discover
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json
import re

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

@app.route('/movieID', methods = ['GET','POST'])
def get_movie_id():
    favorite_moviesList = []
    jsdata = ""
    if current_user.is_authenticated:
        jsdata = request.form['js_movieID']
        user = current_user
        if (user.favorite_movies == ""):
            user.favorite_movies = jsdata
            db.session.add(user)
            db.session.commit()
        else:
            reg2 = re.compile('[0-9]*[^,]')
            movieList2 = reg2.findall(user.favorite_movies)
            if jsdata in movieList2:
                movieList2.remove(jsdata)
                user.favorite_movies = ','.join(movieList2)
                db.session.add(user)
                db.session.commit()
                return jsdata
            else:
                user.favorite_movies = user.favorite_movies+","+jsdata
                db.session.add(user)
                db.session.commit()
                return jsdata
    return jsdata

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
            wrong = "Wrong E-mail address or password"
            return render_template('login.html', form=form, wrong=wrong)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_route():
    logout_user()
    return redirect(url_for('home_route'))

@app.route('/account',  methods=['GET', 'POST'])
@login_required
def user_profile():
    movie = Movie()
    api_key = tmdb.api_key
    user_fav_movies = current_user.favorite_movies
    reg = re.compile('[0-9]*[^,]')
    movieList = reg.findall(user_fav_movies)
    movieListFav = []
    for movie in movieList:
        r = requests.get('https://api.themoviedb.org/3/movie/'+str(movie) +str('?api_key=') +str(api_key))
        j = r.json()
        movieListFav.append(j)
    return render_template('account.html', movie=movie, movieListFav=movieListFav)

@app.route("/movie/<movie_id>/", methods=['GET', 'POST'])
def movie_route(movie_id):
    movie = Movie()
    m_detail = movie.details(movie_id)
    api_key = tmdb.api_key
    r = requests.get('https://api.themoviedb.org/3/movie/'+str(movie_id) +str('?api_key=') +str(api_key))
    j = r.json()
    try:
        genre = j['genres'][0]['name'] +" |"
    except:
        genre = "#"
    try:
        genre_2 = j['genres'][1]['name'] +" |"
    except:
        genre_2 = ''
    try:
        genre_3 = j['genres'][2]['name'] +" |"
    except:
        genre_3 = '' 
    return render_template('movie.html', movie=movie, m_detail=m_detail, genre=genre, genre_2=genre_2, genre_3=genre_3)

@app.route('/search/', methods=['GET', 'POST'])
def search():
    movie = Movie()
    user_search = request.args['search']
    m_search = movie.search(user_search)
    return render_template('search.html', movie=movie, search=user_search, m_search=m_search)

@app.route('/category/', methods=['GET', 'POST'])
def category_route():
    movie = Movie()
    discover = Discover()
    return render_template('categories.html', movie=movie, discover=discover)

@app.route('/category/action/<page>', methods=['GET', 'POST'])
def action_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    action = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 28, 'page': page})
    movies = action
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="action", page=page)

@app.route('/category/adventure/<page>', methods=['GET', 'POST'])
def adventure_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    adventure = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 12, 'page': page})
    movies = adventure
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="adventure", page=page)

@app.route('/category/animation/<page>', methods=['GET', 'POST'])
def animation_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    animation1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 16, 'page': page})
    movies = animation1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="animaction", page=page)

@app.route('/category/comedy/<page>', methods=['GET', 'POST'])
def comedy_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    comedy1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 35, 'page': page})
    movies = comedy1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="comedy", page=page)

@app.route('/category/crime/<page>', methods=['GET', 'POST'])
def crime_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    crime1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 80, 'page': page})
    movies = crime1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="crime", page=page)

@app.route('/category/documentary/<page>', methods=['GET', 'POST'])
def documentary_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    documentary1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 99, 'page': page})
    movies = documentary1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="documentary", page=page)

@app.route('/category/drama/<page>', methods=['GET', 'POST'])
def drama_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    drama1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 18, 'page': page})
    movies = drama1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="drama", page=page)

@app.route('/category/family/<page>', methods=['GET', 'POST'])
def family_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    family1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10751, 'page': page})
    movies = family1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="family", page=page)

@app.route('/category/fantasy/<page>', methods=['GET', 'POST'])
def fantasy_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    fantasy1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 14, 'page': page})
    movies = fantasy1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="fantasy", page=page)

@app.route('/category/history/<page>', methods=['GET', 'POST'])
def history_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    history1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 36, 'page': page})
    movies = history1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="history", page=page)

@app.route('/category/horror/<page>', methods=['GET', 'POST'])
def horror_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    horror1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 27, 'page': page})
    movies = horror1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="horror", page=page)

@app.route('/category/music/<page>', methods=['GET', 'POST'])
def music_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    music1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10402, 'page': page})
    movies = music1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="music", page=page)

@app.route('/category/mystery/<page>', methods=['GET', 'POST'])
def mystery_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    mystery1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 9648, 'page': page})
    movies = mystery1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="mystery", page=page)

@app.route('/category/romance/<page>', methods=['GET', 'POST'])
def romance_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    romance1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10749, 'page': page})
    movies = romance1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="romance", page=page)

@app.route('/category/scifi/<page>', methods=['GET', 'POST'])
def scifi_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    scifi1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 878, 'page': page})
    movies = scifi1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="scifi", page=page)

@app.route('/category/thriller/<page>', methods=['GET', 'POST'])
def thriller_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    thriller1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 53, 'page': page})
    movies = thriller1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="thriller", page=page)

@app.route('/category/war/<page>', methods=['GET', 'POST'])
def war_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    war1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 10752, 'page': page})
    movies = war1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="war", page=page)

@app.route('/category/western/<page>', methods=['GET', 'POST'])
def western_movies(page):
    reg_item = re.findall('\d',page)
    page = int(reg_item[0])
    movie = Movie()
    discover = Discover()
    western1 = discover.discover_movies({'sort_by': 'popularity.desc', 'with_genres': 37, 'page': page})
    movies = western1
    return render_template('category.html', movie=movie, discover=discover, movies=movies, title="western", page=page)
