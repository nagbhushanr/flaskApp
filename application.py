from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    application.debug = True
    application.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    application.debug = False
    application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresql@localhost:5433/postgres'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200))
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

@application.route('/')
def index():
    return render_template('index.html')


@application.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='Your feedback is already received')


if __name__ == '__main__':
    application.run()
