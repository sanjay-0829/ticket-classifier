import pandas as pd
import re
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('data/tickets.csv')

# Combine subject and description to create ticket_text
if 'ticket_text' not in df.columns:
    df['ticket_text'] = df['subject'].fillna('') + " " + df['description'].fillna('')

# ── 1. Inspect what columns exist
print("Available columns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
print("\nCategory counts:")
print(df['category'].value_counts())

# ── 2. Keep only what you need
df = df[['ticket_text', 'category', 'priority']].dropna()

# ── 3. Clean text
def clean(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)        # remove URLs
    text = re.sub(r'[^a-z0-9\s]', '', text)   # remove special chars
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['clean_text'] = df['ticket_text'].apply(clean)

# ── 4. Map priority to urgency labels you control
urgency_map = {
    'critical': 'high', 'high': 'high',
    'medium': 'medium', 'normal': 'medium',
    'low': 'low'
}
df['urgency'] = df['priority'].str.lower().map(urgency_map).fillna('medium')

# ── 5. Split data
X = df['clean_text']
y_cat = df['category']
y_urg = df['urgency']

X_train, X_test, yc_train, yc_test, yu_train, yu_test = train_test_split(
    X, y_cat, y_urg, test_size=0.2, random_state=42, stratify=y_cat
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Test samples:     {len(X_test)}")
print(f"\nCategories: {y_cat.unique()}")
print(f"Urgency levels: {y_urg.unique()}")

# Save cleaned version
df.to_csv('data/tickets_clean.csv', index=False)
print("\nSaved to data/tickets_clean.csv")
