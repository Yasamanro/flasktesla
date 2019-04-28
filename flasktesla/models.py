from datetime import datetime
from flasktesla import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	speed_score = db.Column(db.Integer, nullable=False, default=0)
	drift_score = db.Column(db.Integer, nullable=False, default=0)
	weave_score = db.Column(db.Integer, nullable=False, default=0)
	community_score = db.Column(db.Integer, nullable=False, default=0)
	password = db.Column(db.String(60), nullable=False)
	rides = db.relationship('Ride', backref='driver', lazy=True)

	def get_community_score(self):
		return 21  # TODO: actually implement

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.speed_score}', '{self.weave_score}', '{self.drift_score}', , '{self.community_score}')"

class Ride(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_of_ride = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	start_lat = db.Column(db.Float, nullable=False, default=0)
	start_lng = db.Column(db.Float, nullable=False, default=0)
	end_lat = db.Column(db.Float, nullable=False, default=0)
	end_lng = db.Column(db.Float, nullable=False, default=0)
	avg_speed = db.Column(db.Integer, nullable=False, default=0)
	speed_limit = db.Column(db.Integer, nullable=False, default=0)
	duration = db.Column(db.Integer, default=0)
	battery_consumed = db.Column(db.Integer, default=0)
	speed_score = db.Column(db.Integer, default=0)
	weave_score = db.Column(db.Integer, default=0)
	drift_score = db.Column(db.Integer, default=0)	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Ride('{self.id}', '{self.date_of_ride}', '{self.avg_speed}', '{self.speed_limit}', '{self.duration}', '{self.battery_consumed}', '{self.speed_score}', '{self.weave_score}', '{self.drift_score}', '{self.start_lat}', '{self.start_lng}', '{self.end_lat}', '{self.end_lng}')"

	def as_dict(self):
		
		return {'date_of_ride':self.date_of_ride.strftime('%Y-%m-%d %H:%M:%S.%f'), 'speed_score': self.speed_score, weave_score:self.weave_score, drift_score:self.drift_score}