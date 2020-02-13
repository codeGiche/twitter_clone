from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired ,Length 
from  flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,UserMixin,logout_user,login_fresh,login_required,logout_user, login_user, current_user

app =Flask(__name__)



@app.before_first_request
def create():
    db.create_all()
# configuring database
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:morgan8514@127.0.0.1:5432/twitter_clone"
app.config["SECRET_KEY"]= "secret"
app.config["DEBUG"]=True
# configuring uploads
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "pictures"
configure_uploads(app,photos)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()    

db=SQLAlchemy(app)
# importing time
from other_dependancies.time_func import time_
from other_dependancies.time_func import time_post

# importig the models/tables
from models.user import Users
from models.posts import Posts

# importing wtf forms
from form.registration import Register_form
from form.login import Login_form
from form.post_form import Post_form
# routes
@app.route("/",methods=["POST","GET"])
def home():
    form = Login_form()


    return render_template("index.html" , form=form)



@app.route("/register" , methods=["POST","GET"])
def register():
    form= Register_form()
    # VALIDATING THE INPUTED VALUES BEFORE SUBMISSION
    if form.validate_on_submit():
        if request.method =="POST":
            # recieving data from register form
            name = form.name.data
            username = form.username.data
            password = form.password.data

            # saving the image passed to specified folder
            image_filename=photos.save(form.image.data)
            # getting_image url
            image_url = photos.url(image_filename)
            
            # getting date  whent account was created
            now_today= time_()
            
            # sending data to dd

            info = Users(name=name, username=username, password=generate_password_hash(password),joined_on=now_today ,profile_image=image_url)
            info.create()
            
            return render_template("index.html", form=form, message="Account created! Now Login..")

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST"])
def login():
    form = Login_form()
    if form.validate_on_submit():
        if request.method=="POST":
            username= form.username.data
            password = form.password.data
            remember_me = form.remember_me.data

            check_if_user_exist= Users.query.filter_by(username=username).first()
            if not check_if_user_exist:
                message= "no such username found!"
                print(message)
                return render_template("index.html" , form=form, message_user=message)


            checkin_username_and_password=Users.pass_username_check(username=username, password=password)
            if checkin_username_and_password:
                login_user(check_if_user_exist,remember=form.remember_me.data)
                print("loged in")
                return redirect(url_for("profile"))
               
                # logging in the user. flask login does th session for us . not that this is after all credential verification has been verified

            else:
                message= "wrong password!"
                print(message)
                return render_template("index.html" , form=form, message_password=message)
                
            
            
            

    return redirect(url_for("home"))

@app.route("/timeline", methods=["POST","GET"])
def timeline():
    form= Post_form()
    if form.validate_on_submit():
        if request.method=="POST":
            content= form.post_area.data
            # sending info to db
            time_post_var=time_post()
            post=Posts(user_id=current_user.id, post=content, date_posted=time_post_var)
            post.create()
            print("post posted")

    return render_template("timeline.html", form=form,)

@app.route("/profile")
@login_required
def profile():
    # fetching all posts made by the user
   
    current_user_id = current_user.id
    all_posts = Posts.query.filter_by(user_id=current_user_id).all()




    # current user returns the object of the user that is logged in
    return render_template("profile.html",current_user=current_user,all_posts=all_posts)

# logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))



if __name__=="__main__":
    manager.run()

