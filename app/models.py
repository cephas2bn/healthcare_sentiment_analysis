# app/models.py

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import csv
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Updated to match User's table name
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    feedback_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    def save_to_csv(self):
        """Saves feedback entry to a CSV file."""
        with open("feedback_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.timestamp, self.feedback_text, self.sentiment, self.category])

    def __repr__(self):
        return f"<Feedback {self.id} - {self.sentiment}>"
