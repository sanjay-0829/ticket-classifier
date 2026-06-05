from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from model.predict import predict_ticket

app = FastAPI(
    title="Support Ticket Classifier API",
    description="Auto-classifies support tickets by category and urgency",
    version="1.0.0"
)

# Allow Streamlit to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response schemas
class TicketRequest(BaseModel):
    text: str
    ticket_id: Optional[str] = None

class TicketResponse(BaseModel):
    ticket_id:       Optional[str]
    category:        str
    cat_confidence:  float
    urgency:         str
    urg_confidence:  float
    department:      str
    sla_hours:       int

# ── Endpoints
@app.get("/")
def root():
    return {"status": "running", "model": "TF-IDF Logistic Regression"}

@app.post("/classify", response_model=TicketResponse)
def classify_ticket(req: TicketRequest):
    if not req.text or len(req.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="Ticket text too short")

    result = predict_ticket(req.text)
    return TicketResponse(ticket_id=req.ticket_id, **result)

@app.post("/classify/batch")
def classify_batch(tickets: list[TicketRequest]):
    if len(tickets) > 100:
        raise HTTPException(status_code=400, detail="Max 100 tickets per batch")
    return [{"ticket_id": t.ticket_id, **predict_ticket(t.text)} for t in tickets]

@app.get("/health")
def health():
    return {"status": "healthy"}
