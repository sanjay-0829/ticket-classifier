# Support Ticket Classifier

An end-to-end Machine Learning pipeline that auto-classifies support tickets by category and urgency level, routing them to the correct department with an auto-calculated SLA response window.

## Folder Structure

```text
ticket-classifier/
├── data/
│   ├── tickets.csv            # Raw dataset
│   └── tickets_clean.csv      # Cleaned and processed dataset
├── model/
│   ├── train.py               # Model training script
│   ├── predict.py             # Inference/prediction module
│   ├── category_classifier.pkl# Trained category model
│   └── urgency_classifier.pkl # Trained urgency model
├── api/
│   └── main.py                # FastAPI web server
├── app/
│   └── dashboard.py           # Streamlit user interface
├── data_prep.py               # Preprocessing & cleaning script
├── requirements.txt           # Python project requirements
└── README.md                  # Project documentation
```

---

## Getting Started

### 1. Install Dependencies
Make sure you have installed all dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Preprocess the Data
Run the cleaning script to preprocess the raw tickets dataset:
```bash
python data_prep.py
```
This loads `data/tickets.csv`, cleans the text, maps priority labels to urgency levels, splits the data, and saves the cleaned dataset to `data/tickets_clean.csv`.

### 3. Train the Models
Train both the category and urgency classifiers using TF-IDF + Logistic Regression:
```bash
python model/train.py
```
This script will output accuracy metrics and save the trained pipelines to `model/category_classifier.pkl` and `model/urgency_classifier.pkl`.

### 4. Run the REST API
Launch the FastAPI server using Uvicorn:
```bash
uvicorn api.main:app --reload --port 8000
```
- Access the API root at: http://localhost:8000/
- Access the auto-generated Swagger UI interactive documentation at: http://localhost:8000/docs

### 5. Run the Streamlit Dashboard
Launch the dashboard interface:
```bash
streamlit run app/dashboard.py
```
- Open your browser to: http://localhost:8501
- You can paste single tickets to get immediate predictions, view workload analytics, see weekly volume trends, or upload a CSV in batch format (under the sidebar).
