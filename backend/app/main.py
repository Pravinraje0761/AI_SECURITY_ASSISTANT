from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import engine, Base
from app.api import auth, scan, monitoring, alerts, email_analyzer
from app.services.monitoring_agent import monitoring_agent
from app.services.file_monitor import file_monitor
import logging

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(settings.LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Digital Bodyguard...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready")
    monitoring_agent.start(interval=30)
    file_monitor.start(interval=10)
    logger.info("All monitors started")
    yield
    monitoring_agent.stop()
    file_monitor.stop()
    engine.dispose()
    logger.info("Shutdown complete")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Digital Bodyguard - Personal Cybersecurity System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(scan.router, prefix="/api/v1/scan", tags=["Scanning"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["Monitoring"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(email_analyzer.router, prefix="/api/v1/protection", tags=["Protection"])


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "monitoring": monitoring_agent.is_running,
        "file_monitor": file_monitor.is_running,
    }


@app.get("/api/v1/dashboard")
async def dashboard():
    from app.services.alert_service import alert_service
    from app.services.behavior_service import behavior_service
    from app.services.malware_service import malware_service
    from app.services.phishing_service import phishing_service

    resources = behavior_service.get_system_resources()
    alert_counts = alert_service.counts()
    malware_stats = malware_service.get_stats()
    phishing_stats = phishing_service.get_stats()

    score = max(100 - resources.get("cpu_percent", 0) * 0.3 - resources.get("memory_percent", 0) * 0.2, 0)

    return {
        "security_score": {
            "security_score": int(score),
            "threat_level": "safe" if score > 70 else "medium" if score > 40 else "high",
        },
        "alerts": alert_counts,
        "resources": resources,
        "stats": {
            "malware_scans": malware_stats.get("total_scans", 0),
            "url_scans": phishing_stats.get("total_scans", 0),
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
