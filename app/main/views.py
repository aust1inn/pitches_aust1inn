from flask import render_template,url_for,flash,redirect,request
from . import main
from .. import bcrypt,db
from forms import RegistrationForm,LoginForm,UpdateAccountForm
from models import User
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