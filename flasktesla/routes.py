from flask import render_template, url_for, flash, redirect, request
from flasktesla.forms import RegistrationForm, LoginForm, RideForm
from flasktesla.models import User, Ride
from flasktesla import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
from sqlalchemy import and_
import json
import pdb

from flasktesla.badge import LinearBadgeFactory, Badge, SpeedBadge, DriftBadge, WeaveBadge, CommunityBadge

speed_badge_factory = LinearBadgeFactory()
speed_badge_factory.add_badge(10, SpeedBadge('Complete 200 Journeys within Community Average Speed', 'speed_bronze.png', 200, 's'))
speed_badge_factory.add_badge(20, SpeedBadge('Complete 500 Journeys within Community Average Speed', 'speed_silver.png', 500, 's'))
speed_badge_factory.add_badge(30, SpeedBadge('Complete 700 Journeys within Community Average Speed', 'speed_gold.png', 700, 's'))


drift_badge_factory = LinearBadgeFactory()
drift_badge_factory.add_badge(10, DriftBadge('Complete 200 Journeys with Safe Drifting Scores', 'drift_bronze.png', 200, 'd'))
drift_badge_factory.add_badge(20, DriftBadge('Complete 500 Journeys with Safe Drifting Scores', 'drift_silver.png', 500, 'd'))
drift_badge_factory.add_badge(30, DriftBadge('Complete 700 Journeys with Safe Drifting Scores', 'drift_gold.png', 700, 'd'))

weave_badge_factory = LinearBadgeFactory()
weave_badge_factory.add_badge(10, WeaveBadge('Complete 200 Journeys with Safe Weaving Scores', 'weave_bronze.png', 200, 'w'))
weave_badge_factory.add_badge(20, WeaveBadge('Complete 500 Journeys with Safe Weaving Scores', 'weave_silver.png', 500, 'w'))
weave_badge_factory.add_badge(30, WeaveBadge('Complete 700 Journeys with Safe Weaving Scores', 'weave_gold.png', 700, 'w'))

community_badge_factory = LinearBadgeFactory()
community_badge_factory.add_badge(10, CommunityBadge('Top 25 Percent of Safe Drivers', 'community_bronze.png', 25, 'c'))
community_badge_factory.add_badge(20, CommunityBadge('Top 50 Percent of Safe Drivers', 'community_silver.png', 50, 'c'))
community_badge_factory.add_badge(30, CommunityBadge('Top 75 Percent of Safe Drivers', 'community_gold.png', 75, 'c'))

badge_factories = {
	'speed': speed_badge_factory,
	'drift': drift_badge_factory,
	'weave': weave_badge_factory,
	'community': community_badge_factory,
}

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

	# Badges
	badge_names = ['speed', 'drift', 'weave', 'community']
	scores 	    = [current_user.speed_score, current_user.drift_score, current_user.weave_score, current_user.community_score]
	completed_badges, remaining_badges = [], []
	for name, score in zip(badge_names,scores):
		completed, remaining = badge_factories[name].get_completed_remaining(score)
		completed_badges.extend(completed)
		remaining_badges.extend(remaining)

	# Journeys
	a_day_ago = datetime.today() - timedelta(days = 1)
	a_week_ago = datetime.today() - timedelta(days = 7)
	a_month_ago = datetime.today() - timedelta(days = 30)

	day_rides = Ride.query.filter(Ride.date_of_ride >= a_day_ago).filter_by(user_id=current_user.id).all()
	week_rides = Ride.query.filter(Ride.date_of_ride >= a_week_ago).filter_by(user_id=current_user.id).all()
	month_rides = Ride.query.filter(Ride.date_of_ride >= a_month_ago).filter_by(user_id=current_user.id).all()

	return render_template('account.html', title='Account', image_file=image_file, 
		completed_badges=completed_badges, remaining_badges=remaining_badges,
		day_rides=day_rides, week_rides=week_rides, month_rides=month_rides) 


@app.route("/ride/new", methods=['GET', 'POST'])
@login_required
def new_ride():
	form = RideForm()
	if form.validate_on_submit():
		print(type(form.date_of_ride.data))
		print(form.date_of_ride.data)
		ride = Ride(date_of_ride=form.date_of_ride.data, start_lat=form.start_lat.data, 
			        start_lng=form.start_lng.data, end_lat=form.end_lat.data, end_lng=form.end_lng.data,
			        avg_speed=form.avg_speed.data, speed_limit=form.speed_limit.data, user_id=current_user.id)
		db.session.add(ride)
		db.session.commit()
		flash('Ride has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('create_ride.html', title='New Ride', form=form)

@app.route("/processjson", methods=['POST'])
@login_required
def processjson():
	data = json.loads(request.data)
	start = data['start_date']
	end = data['end_date']

	# parse start and end strings into actual date objects
	start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
	end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')

	# build and exec query
	driver_data = Ride.query.filter(Ride.date_of_ride >= start, Ride.date_of_ride <= end).filter_by(user_id=current_user.id).all()
	community_data = Ride.query.filter(Ride.date_of_ride >= start, Ride.date_of_ride <= end).filter_by(user_id=1).all()

	driver_data_jsons = [ride.as_dict() for ride in driver_data]
	community_data_jsons = [ride.as_dict() for ride in community_data]

	# return json serialized data
	return json.dumps({'driver_data': driver_data_jsons, 'community_data': community_data_jsons})
