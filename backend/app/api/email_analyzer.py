from fastapi import APIRouter, Depends
from app.services.phishing_service import phishing_service
from app.ml.scam_classifier import scam_classifier
from app.utils.security import get_current_user
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models.scan_history import EmailAnalysis, WebsiteVisit
from sqlalchemy.orm import Session
import uuid
import json

router = APIRouter()


class EmailRequest(BaseModel):
    subject: str = ""
    sender: str = ""
    body: str = ""


class UrlCheckRequest(BaseModel):
    url: str
    browser: str = "unknown"


@router.post("/analyze-email")
async def analyze_email(req: EmailRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    result = phishing_service.scan_email_content(req.subject, req.body, req.sender)
    scam_label, scam_prob, scam_indicators = scam_classifier.predict(f"{req.subject} {req.body}")

    combined_score = max(result["probability"], scam_prob)
    if combined_score >= 0.6:
        final = "dangerous"
    elif combined_score >= 0.3:
        final = "suspicious"
    else:
        final = "safe"

    all_indicators = result["indicators"] + [f"Scam: {i}" for i in scam_indicators]

    record = EmailAnalysis(
        id=str(uuid.uuid4()), user_id=user_id,
        subject=req.subject, sender=req.sender,
        body_preview=req.body[:500], result=final,
        score=combined_score, indicators=json.dumps(all_indicators),
    )
    db.add(record)
    db.commit()

    return {
        "result": final,
        "score": round(combined_score, 3),
        "phishing": result,
        "scam": {"label": scam_label, "probability": scam_prob, "indicators": scam_indicators},
        "indicators": all_indicators,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.post("/check-url")
async def check_url(req: UrlCheckRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    result = phishing_service.scan_url(req.url)
    final = "dangerous" if result["is_phishing"] else "safe"

    record = WebsiteVisit(
        id=str(uuid.uuid4()), user_id=user_id,
        url=req.url, domain=result.get("domain", ""),
        result=final, score=result["probability"],
        browser=req.browser,
    )
    db.add(record)
    db.commit()

    return {
        "result": final,
        "score": result["probability"],
        "indicators": result["indicators"],
        "domain": result.get("domain", ""),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/email-history")
async def email_history(user_id: str = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 50):
    records = db.query(EmailAnalysis).filter(EmailAnalysis.user_id == user_id).order_by(EmailAnalysis.created_at.desc()).limit(limit).all()
    return [
        {"id": r.id, "subject": r.subject, "sender": r.sender, "result": r.result,
         "score": r.score, "indicators": json.loads(r.indicators) if r.indicators else [],
         "created_at": r.created_at.isoformat() if r.created_at else None}
        for r in records
    ]


@router.get("/website-history")
async def website_history(user_id: str = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 50):
    records = db.query(WebsiteVisit).filter(WebsiteVisit.user_id == user_id).order_by(WebsiteVisit.created_at.desc()).limit(limit).all()
    return [
        {"id": r.id, "url": r.url, "domain": r.domain, "result": r.result,
         "score": r.score, "browser": r.browser,
         "created_at": r.created_at.isoformat() if r.created_at else None}
        for r in records
    ]
