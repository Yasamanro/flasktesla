from flasktesla import app

if __name__ == '__main__':
	app.run(debug=True)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
