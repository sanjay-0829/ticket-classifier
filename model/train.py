import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# ── Load cleaned data
df = pd.read_csv('data/tickets_clean.csv')

# Ensure clean_text has no NaN values
df['clean_text'] = df['clean_text'].fillna('')

from sklearn.model_selection import train_test_split
X_train, X_test, yc_train, yc_test, yu_train, yu_test = train_test_split(
    df['clean_text'], df['category'], df['urgency'],
    test_size=0.2, random_state=42
)

# ── Build TF-IDF pipeline — category classifier
cat_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=15000,
        ngram_range=(1, 2),     # unigrams + bigrams
        min_df=2,
        sublinear_tf=True       # apply log normalization
    )),
    ('clf', LogisticRegression(
        max_iter=1000,
        C=5.0,                  # regularization strength
        class_weight='balanced' # handles class imbalance
    ))
])

# ── Train category model
print("Training category classifier...")
cat_pipeline.fit(X_train, yc_train)
yc_pred = cat_pipeline.predict(X_test)
print(f"\nCategory Accuracy: {accuracy_score(yc_test, yc_pred):.3f}")
print(classification_report(yc_test, yc_pred))

# ── Build urgency classifier (same pipeline, different labels)
urg_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ('clf', LogisticRegression(
        max_iter=1000,
        C=3.0,
        class_weight='balanced'
    ))
])

print("\nTraining urgency classifier...")
urg_pipeline.fit(X_train, yu_train)
yu_pred = urg_pipeline.predict(X_test)
print(f"\nUrgency Accuracy: {accuracy_score(yu_test, yu_pred):.3f}")
print(classification_report(yu_test, yu_pred))

# ── Save both models
joblib.dump(cat_pipeline, 'model/category_classifier.pkl')
joblib.dump(urg_pipeline, 'model/urgency_classifier.pkl')
print("\nModels saved to model/ folder")
