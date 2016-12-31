from flask import *
from functools import *
import data

app = Flask(__name__)
app.secret_key = data.secret_key

force_log_error = None


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            global force_log_error
            force_log_error = True

            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/new', methods=['GET', 'POST'])
@login_required
def add_mac():
    if request.method == 'POST':
        name = request.form['name']
        mac = request.form['address']
        print(name)
        print(mac)
        return redirect(url_for('home'))
    return render_template('addmac.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != data.password:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
