from textblob import TextBlob
import re

# Define categories with related keywords
CATEGORIES = {
    "Wait Time": ["wait", "delay", "time", "slow", "long"],
    "Staff Interaction": ["staff", "nurse", "doctor", "rude", "friendly", "helpful", "care"],
    "Cleanliness": ["clean", "dirty", "hygiene", "sanitary", "messy"],
    "Facilities": ["room", "equipment", "facility", "bed", "waiting area"],
    "Billing and Insurance": ["billing", "insurance", "cost", "price", "expensive", "charge"],
}

def categorize_feedback(feedback):
    """
    Categorizes feedback based on predefined keywords.
    Returns a list of matched categories.
    """
    feedback_lower = feedback.lower()
    matched_categories = []

    for category, keywords in CATEGORIES.items():
        if any(re.search(rf"\b{kw}\b", feedback_lower) for kw in keywords):
            matched_categories.append(category)

    return matched_categories if matched_categories else ["General"]

def analyze_sentiment(feedback):
    """
    Analyzes the sentiment of the feedback and provides:
    - Sentiment type (Positive, Negative, Neutral)
    - Sentiment intensity (-1.0 to 1.0)
    - Categories (e.g., Wait Time, Staff Interaction)
    """
    # Analyze sentiment polarity using TextBlob
    blob = TextBlob(feedback)
    polarity = blob.sentiment.polarity

    # Determine sentiment type based on polarity score
    if polarity > 0.2:
        sentiment_type = "Positive"
    elif polarity < -0.2:
        sentiment_type = "Negative"
    else:
        sentiment_type = "Neutral"

    # Categorize feedback
    categories = categorize_feedback(feedback)

    # Package the result as a dictionary
    result = {
        "sentiment_type": sentiment_type,
        "sentiment_intensity": round(polarity, 2),
        "categories": categories,
    }

    return result

def analyze_feedback_batch(feedback_list):
    """
    Analyzes a batch of feedback entries.
    Returns a list of results with sentiment and categorization for each feedback entry.
    """
    analysis_results = []

    for feedback in feedback_list:
        result = analyze_sentiment(feedback)
        analysis_results.append(result)

    return analysis_results

# Example Usage
if __name__ == "__main__":
    sample_feedback = [
        "The wait time was too long and the staff were not very helpful.",
        "The facility was clean and the doctor was extremely professional and friendly.",
        "Billing was confusing and the charges were too high."
    ]

    # Analyze sample feedback in a batch
    results = analyze_feedback_batch(sample_feedback)
    for i, feedback_result in enumerate(results):
        print(f"Feedback {i+1}: {feedback_result}")
