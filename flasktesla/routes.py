from flask import render_template, url_for, flash, redirect, request
from flasktesla.forms import RegistrationForm, LoginForm
from flasktesla.models import User, Ride
from flasktesla import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


from flasktesla.badge import LinearBadgeFactory, Badge
speed_badge_factory = LinearBadgeFactory()
bronze_speed_badge = Badge('This is the bronze badge')
silver_speed_badge = Badge('This is the silver badge')
silver_speed_badge = Badge('This is the silver badge')

speed_badge_factory.add_badge(10, bronze_speed_badge)
speed_badge_factory.add_badge(20, silver_speed_badge)



@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html' , title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
	image_file = url_for('static', filename='images/' + current_user.image_file)
	#badges = 
	return render_template('account.html', title='Account', image_file=image_file) #get_)


@app.route("/ride/new")
@login_required
def new_ride():
	return render_template('create_ride.html', title='New Ride')