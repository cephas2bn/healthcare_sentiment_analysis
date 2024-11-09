# app/main.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import FeedbackForm
from .models import Feedback
from .sentiment_analysis import analyze_sentiment
from datetime import datetime
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/dashboard")
@login_required
def dashboard():
    # Retrieve all feedback submitted by the current user for display on the dashboard
    feedback_list = Feedback.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", feedback_list=feedback_list)

@main.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback_text = form.feedback.data
        category = form.category.data
        sentiment, score = analyze_sentiment(feedback_text)

        # Create a new feedback entry
        new_feedback = Feedback(
            user_id=current_user.id,
            timestamp=datetime.now(),
            feedback=feedback_text,
            sentiment=sentiment,
            category=category
        )

        # Add and commit the new feedback to the database
        db.session.add(new_feedback)
        db.session.commit()

        # Save to CSV
        save_feedback_to_csv(new_feedback)

        flash("Your feedback has been submitted!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("feedback.html", form=form)

def save_feedback_to_csv(feedback):
    """Saves feedback entry to a CSV file."""
    with open("feedback_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([feedback.timestamp, feedback.feedback, feedback.sentiment, feedback.category])

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
