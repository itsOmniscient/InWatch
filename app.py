import os
from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from tmdbv3api import TMDb, Movie
tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("CSRF_SECRET_KEY")

@app.route('/')
@app.route('/home')
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

if __name__ == '__main__':
    app.run(debug=True)
