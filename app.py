from flask import Flask, render_template
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_route():
    return render_template('index.html')

@app.route('/register')
def registration_route():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route('/login')
def login_route():
    form = LoginForm()
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
