from flask import Flask, render_template, url_for
from app import app 

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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',title='About')
     


if __name__ == '__main__':
    app.run(debug=True)