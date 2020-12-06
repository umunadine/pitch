from flask import render_template, flash,url_for, redirect, request
from app import app,db, bcrypt
from app.forms import RegistrationForm,LoginForm,UpdateAccountForm
from app.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account is successfully created,Now you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)
    
@app.route("/login",methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else :
             flash('Login Unsuccessful. Please check username and password', 'danger')   
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Succcessfully updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file= url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='account', image_file = image_file, form=form)
  