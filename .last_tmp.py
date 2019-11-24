from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import SetUpForm, LoginForm
from sqlalchemy.sql.expression import func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # we add some functionality to our database models and it will handle all of the sessions in the background for us.
login_manager.login_view = 'login' # for @login_required in routes /account
login_manager.login_message_category = 'info' # nicer notification

# user_loader is for reloading user from user_id stored in the session (from website). Function to get a user by id for loginManager to find by decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #

# class as a database structure, each class own table in database
class User(db.Model, UserMixin): # db.Model lets know this is a table. 4 methods expected in loginManager - is_authenticated, is_active, is_anonymous, get_id - instead class from extention UserMixin
    # now adding columns for this table
    id = db.Column(db.Integer, primary_key = True) # - primary key = "unique id for user"
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.password}')"

class Place(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    where = db.Column(db.String(100), unique = True, nullable = False)
    done = db.Column(db.Integer)

    def __repr__(self):
        return f"Place('{self.where}', '{self.done}')"


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # next_page is when you type directly "localshost:5000/account" and not logged in - so account is the next page
            next_page = request.args.get('next') # args is a dict, but if empty throws an error when accessed with []
            return redirect (next_page) if next_page else redirect(url_for('home')) # ternary conditional
        else:
            flash('Login unsuccessfull. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    form = SetUpForm()
    if form.validate_on_submit():
        place = Place(where=form.place.data, done=0)
        db.session.add(place)
        db.session.commit()
        flash('Your place has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('home.html', title='Home', form=form)

@app.route("/review")
@login_required
def review():
    places = Place.query.all()
    return render_template('review.html', title='Review', places=places)

@app.route("/result")
@login_required
def result():
    chosen = db.session.query(Place).order_by(func.random()).first()
    if chosen == None:
        chosen = 'No places in the database!'
    else:
        chosen = db.session.query(Place).order_by(func.random()).first().where
    return render_template('result.html', title='Result', chosen=chosen)

@app.route('/place/<int:place_id>/delete', methods=['POST']) # int is expected
@login_required
def delete_place(place_id):
    place = Place.query.get_or_404(place_id) # instead of get() or filter_by(),  gives 404 if doesnt exist
    db.session.delete(place)
    db.session.commit()
    flash('Your place has been deleted!', 'success')
    return redirect(url_for('review'))

@app.route('/place/<int:place_id>/status_change') # int is expected
@login_required
def status_change(place_id):
    place = Place.query.get_or_404(place_id) # instead of get() or filter_by(),  gives 404 if doesnt exist
    if place.done:
        place.done = 0
    else:
        place.done = 1
    db.session.commit()
    flash('Your ' + place.where.upper() + ' status has been changed', 'success')
    return redirect(url_for('review'))


if __name__ == '__main__':
    app.run(debug=True)