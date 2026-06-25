# Ticket3D: AI-Powered Support Triage & Cinematic 3D Analytics

![Ticket3D Scrolling Animation Showcase](website/animation.gif)

Ticket3D is a state-of-the-art, end-to-end Support Operations platform. It leverages machine learning to automatically classify incoming customer support tickets by category and urgency in real-time, route them to the correct department, and calculate dynamic SLA response windows.

The system features:
1. 🎬 **Apple-Style Cinematic 3D Scrollytelling Showcase**: A highly immersive, high-performance product landing page using GSAP, ScrollTrigger, and HTML5 Canvas.
2. 📊 **Interactive Analytics Dashboard**: A Streamlit application offering detailed insights, ticket volume trends, SLA status tracking, and batch CSV processing.
3. ⚡ **FastAPI Backend**: A high-performance REST API with Swagger documentation for real-time and batch predictions.
4. 🧠 **Machine Learning Pipeline**: A clean Scikit-Learn training and inference workflow using TF-IDF vectorization and Logistic Regression.

---

## 🎨 Visual Journey & Showcase

Here is a visual breakdown of the operational concepts behind **Ticket3D**:

| **The Support Overload Problem** | **AI Routing Core** |
| :---: | :---: |
| ![Enterprise Support Overload](images/Enterprise_support_center_overwh._202606141806.jpeg) <br> *Manual routing leads to bottlenecks and delays.* | ![AI Routing Core](images/AI_classification_core_global_ne._202606141804.jpeg) <br> *Intelligent classification of urgency and category.* |

| **Department Network Routing** | **Unified Operations Center** |
| :---: | :---: |
| ![Network Routing](images/Network_of_enterprise_department._202606141805.jpeg) <br> *Dynamic SLA matching and direct department assignment.* | ![Operations Center](images/AI_support_command_center_visual._202606141805.jpeg) <br> *Seamless real-time support monitoring dashboard.* |

---

## 📁 Repository Structure

```text
Ticket3D/
├── api/
│   └── main.py                 # FastAPI web server & endpoints
├── app/
│   └── dashboard.py            # Streamlit analytics dashboard & UI
├── data/
│   ├── tickets.csv             # Raw support tickets dataset
│   └── tickets_clean.csv       # Preprocessed and cleaned dataset
├── images/
│   └── [Screenshots & Visuals] # Concept artwork & screenshots
├── model/
│   ├── train.py                # Model training pipeline
│   ├── predict.py              # Real-time prediction & SLA routing logic
│   ├── category_classifier.pkl # Serialized category model
│   └── urgency_classifier.pkl  # Serialized urgency model
├── website/
│   ├── index.html              # Apple-style scrollytelling landing page
│   ├── styles.css              # Premium custom CSS system
│   ├── script.js               # Canvas frame-by-frame scroll animation
│   ├── gsap.min.js             # GSAP animation library
│   ├── ScrollTrigger.min.js    # GSAP scroll plugin
│   ├── animation.gif           # Loop showcase animation (540x304)
│   └── animation_frames/       # 229 high-fidelity animation frames
├── data_prep.py                # Text preprocessing and mapping script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## ⚡ Tech Stack

- **ML Pipeline**: Python, Scikit-Learn, Pandas, NumPy, Joblib
- **FastAPI Backend**: FastAPI, Uvicorn, Pydantic
- **Dashboard**: Streamlit, Plotly Express, Requests
- **Cinematic Frontend**: HTML5 Canvas, Vanilla CSS3 (Custom design system), GSAP 3.12.5, ScrollTrigger

---

## 🚀 Getting Started

### 1. Install Dependencies

Ensure you have Python 3.9+ installed, then install all project requirements:

```bash
pip install -r requirements.txt
```

### 2. Preprocess the Data

Run the preprocessing script to clean text, map priority labels to urgency levels, split dataset, and prepare data for training:

```bash
python data_prep.py
```

*This generates `data/tickets_clean.csv` from the raw `data/tickets.csv`.*

### 3. Train the Models

Train the category and urgency classification pipelines (TF-IDF + Logistic Regression):

```bash
python model/train.py
```

*This outputs evaluation metrics (accuracy, precision, recall) and saves the serialized pipelines to `model/category_classifier.pkl` and `model/urgency_classifier.pkl`.*

### 4. Run the REST API

Launch the FastAPI backend server using Uvicorn:

```bash
uvicorn api.main:app --reload --port 8000
```

- **API Root**: `http://localhost:8000/`
- **Swagger Documentation (Interactive UI)**: `http://localhost:8000/docs`

### 5. Run the Streamlit Analytics Dashboard

Launch the interactive triaging and analytics dashboard:

```bash
streamlit run app/dashboard.py
```

- **Dashboard UI**: `http://localhost:8501/`
- Paste individual ticket descriptions for real-time classification, view dynamic workload analytics, or upload a CSV in batch format.

### 6. Explore the Cinematic Landing Page

Open the beautiful landing page locally:

- Open `website/index.html` in any modern web browser.
- Scroll through to experience the Apple-style canvas scroll animation, interactive metrics, and holographic components detailing the ticket-routing flow.

---

## 🎯 SLA & Routing Architecture

When a ticket description is submitted, Ticket3D processes it through parallel classifier heads:

| Predicted Category | Target Department | Urgency Level | SLA Window |
| :--- | :--- | :--- | :--- |
| **Billing** | Billing & Accounts | High / Medium / Low | 4h / 24h / 48h |
| **Technical** | Tech Support | High / Medium / Low | 2h / 12h / 24h |
| **Login/Auth** | Security Operations | High / Medium / Low | 1h / 6h / 12h |
| **Feedback/General**| Customer Relations | High / Medium / Low | 8h / 48h / 72h |
