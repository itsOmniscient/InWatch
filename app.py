import os
from flask import Flask, render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm
from tmdbv3api import TMDb, Movie
import requests
import json
tmdb = TMDb()
tmdb.api_key = os.getenv("api_key")

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("CSRF_SECRET_KEY")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_route():
    movie = Movie()
    return render_template('index.html', movie=movie)

@app.route('/register', methods=['GET', 'POST'])
def registration_route():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('home_route'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home_route'))
    return render_template('login.html', form=form)

@app.route("/movie/<movie_id>/", methods=['GET', 'POST'])
def movie_route(movie_id):
    movie = Movie()
    m_detail = movie.details(movie_id)
    api_key = tmdb.api_key
    r = requests.get('https://api.themoviedb.org/3/movie/'+str(movie_id) +str('?api_key=') +str(api_key))
    j = r.json()
    return render_template('movie.html', movie=movie, m_detail=m_detail)

@app.route('/search/<term>', methods=['GET', 'POST'])
def search_route(term):
    movie = Movie()
    m_search = movie.search(term)
    return render_template('search.html', movie=movie, m_search=m_search)

if __name__ == '__main__':
    app.run(debug=True)
