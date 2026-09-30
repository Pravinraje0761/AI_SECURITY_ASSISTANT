from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.scan import ScanRequest, ScanResponse
from app.services.phishing_service import phishing_service
from app.services.malware_service import malware_service
from app.models.scan_history import ScanHistory
from app.utils.security import get_current_user
from datetime import datetime
import uuid
import json

router = APIRouter()


@router.post("/url", response_model=ScanResponse)
async def scan_url(request: ScanRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    result = phishing_service.scan_url(request.target)
    scan_result = "malicious" if result["is_phishing"] else "safe"
    scan_id = str(uuid.uuid4())
    record = ScanHistory(
        id=scan_id, user_id=user_id, scan_type="url",
        target=request.target, result=scan_result,
        score=result["probability"], details=json.dumps(result),
    )
    db.add(record)
    db.commit()
    return ScanResponse(
        id=scan_id, type="url", target=request.target,
        result=scan_result, score=result["probability"],
        details=result, created_at=datetime.utcnow(),
    )


@router.get("/history")
async def get_history(user_id: str = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 50):
    records = db.query(ScanHistory).filter(ScanHistory.user_id == user_id).order_by(ScanHistory.created_at.desc()).limit(limit).all()
    return [
        {"id": r.id, "type": r.scan_type, "target": r.target, "result": r.result,
         "score": r.score, "details": json.loads(r.details) if r.details else None,
         "created_at": r.created_at.isoformat() if r.created_at else None}
        for r in records
    ]
