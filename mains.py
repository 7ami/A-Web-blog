from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

with open('config.json', 'r') as abc:
    para = json.load(abc)["parameters"]

local_server = True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=para['gmail_name'],
    MAIL_PASSWORD=para['gmail_pass']
)
mail = Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = para['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = para['prod_uri']
db = SQLAlchemy(app)


class Contactinfo(db.Model):
    SN = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    PhoneNo = db.Column(db.String(30), nullable=False)
    Message = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(20), nullable=True)


class Post(db.Model):
    SN = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80), nullable=False)
    subheading = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    Content = db.Column(db.String(200), nullable=False)
    Post_info = db.Column(db.String(50), nullable=False)
    img_file = db.Column(db.String(25), nullable=True)
    Date = db.Column(db.String(20), nullable=True)


@app.route('/')
def home():
    return render_template('index.html', params=para)


@app.route('/about')
def about():
    return render_template('about.html', params=para)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_way(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=para, post=post)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    """

        SN Name Email PhoneNo Message Date

        """
    if request.method == 'POST':
        """
         add info into the databse
        """
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        mess = request.form.get('mess')
        entry = Contactinfo(Name=name, Email=email, PhoneNo=phone, Message=mess, Date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New Message from ' + name, sender=email, recipients=[para['gmail_name']],
                          body=mess + "\n" + phone)
    return render_template('contact.html', params=para)


app.run(debug=True)
