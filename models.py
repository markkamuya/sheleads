from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    completed_scenarios = db.relationship('ScenarioHistory', backref='user', lazy=True)

class ScenarioHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_type = db.Column(db.String(100), nullable=False)
    user_input = db.Column(db.String(500), nullable=False)
    bot_response = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
