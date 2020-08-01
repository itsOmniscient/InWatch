from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '90991386503f7cbfad768b9173025cdd' #yea i know this isnt safe but its a school project
# so i will leave it like this for now and use github secrets later :)

@app.route('/')
@app.route('/home')
def home_route():
    return render_template('index.html')

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
