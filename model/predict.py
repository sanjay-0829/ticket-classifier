import joblib
import re

# Load models once at module level (not on every request)
cat_model = joblib.load('model/category_classifier.pkl')
urg_model = joblib.load('model/urgency_classifier.pkl')

# Department routing map — adjusted to match the categories in tickets.csv
ROUTING = {
    'billing':           'Finance Team',
    'access/security':   'Security Operations Center',
    'hardware':          'IT Hardware Desk',
    'network':           'Network Operations Center',
    'software':          'Software Support Team',
}

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def predict_ticket(ticket_text: str) -> dict:
    cleaned = clean_text(ticket_text)

    category = cat_model.predict([cleaned])[0]
    urgency  = urg_model.predict([cleaned])[0]

    # Get confidence scores
    cat_proba = cat_model.predict_proba([cleaned])[0]
    cat_conf  = round(float(max(cat_proba)) * 100, 1)

    urg_proba = urg_model.predict_proba([cleaned])[0]
    urg_conf  = round(float(max(urg_proba)) * 100, 1)

    # Route to department
    department = ROUTING.get(category.lower(), 'Support Team')

    # SLA window based on urgency
    sla_hours = {'high': 4, 'medium': 24, 'low': 72}.get(urgency, 24)

    return {
        'category':    category,
        'cat_confidence': cat_conf,
        'urgency':     urgency,
        'urg_confidence': urg_conf,
        'department':  department,
        'sla_hours':   sla_hours,
    }

if __name__ == "__main__":
    # Test prediction logic directly if run as main
    test_text = "I cannot log in to my email account because it says my password has expired."
    print("Testing prediction on text:", test_text)
    print(predict_ticket(test_text))
