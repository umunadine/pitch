from flask import render_template, flash,url_for, redirect
from app import app,db, bcrypt
from app.forms import RegistrationForm,LoginForm
from app.models import User,Post

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
        return render_template('home.html', posts=posts)

@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html", title='About')
     
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account successfully created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Signup', form=form)
    
@app.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
  