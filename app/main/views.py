import secrets,os
from flask import render_template,url_for,flash,redirect,request
from PIL import Image
from . import main
from .. import bcrypt,db
from .forms import RegistrationForm,LoginForm,UpdateAccountForm
from ..models import User
from flask_login import login_user,current_user,logout_user,login_required


# Views
@main.route('/')
def index():
    name = "Time to get started "
    # context ={
    #     name: name
    # }
    return render_template('index.html', name=name)

@main.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # flash(f'Account created for {form.username.data}!','success')
        flash('Your account has been created! You are now able to log in' , 'success')
        return redirect(url_for('login'))
    # else:
    #     flash(f'Account created for {form.username.data}!','success')
    #     # return redirect(url_for('home'))    
    return render_template('register.html' ,title='register' ,form=form) 


@main.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page= request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:    
            flash("Login unsuccesful.Please check email and password",'danger')

    return render_template('login.html' ,title='login', form=form)        


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(main.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    
    return picture_fn

@main.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
  
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html' ,title='account', image_file=image_file, form=form)    
   