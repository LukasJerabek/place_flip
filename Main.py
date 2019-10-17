from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import SetUpForm
from  sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Place(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    where = db.Column(db.String(100), unique = True, nullable = False)

    def __repr__(self):
        return f"Place('{self.where}')"

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SetUpForm()
    if form.validate_on_submit():
        place = Place(where=form.place.data)
        db.session.add(place)
        db.session.commit()
        flash('Your place has been added!', 'success')
        return redirect(url_for('review'))
    return render_template('home.html', title='Home', form=form)

@app.route("/review")
def review():
    places = Place.query.all()
    return render_template('review.html', title='Review', places=places)

@app.route("/result")
def result():
    chosen = db.session.query(Place).order_by(func.random()).first()
    if chosen == None:
        chosen = 'No places in the database!'
    else:
        chosen = db.session.query(Place).order_by(func.random()).first().where
    return render_template('result.html', title='Result', chosen=chosen)

@app.route('/place/<int:place_id>/delete', methods=['POST']) # int is expected
def delete_place(place_id):
    place = Place.query.get_or_404(place_id) # instead of get() or filter_by(),  gives 404 if doesnt exist
    db.session.delete(place)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('review'))

if __name__ == '__main__':
    app.run(debug=True)
