from flask import Flask, render_template, flash,url_for, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app 
from forms import RegistrationForm,LoginForm

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba205'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Nadine',
        'title': 'Pitch 1',
        'content': 'This is the first post',
        'date_posted': ' Dec 05, 2020'
    },
    {
        'author': 'Dannu',
        'title': 'Pitch 2',
        'content': 'This is the second post',
        'date_posted': 'Aug 01, 2020'
    }
]


@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html',title='About')
     
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Signup', form=form)
    
@app.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
     


if __name__ == '__main__':
    app.run(debug=True)