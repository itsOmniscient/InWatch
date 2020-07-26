from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_route():
    return render_template('index.html')

@app.route('/registration')
def reg_route():
    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)
