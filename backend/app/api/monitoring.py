from fastapi import APIRouter, Depends, UploadFile, File
from app.services.behavior_service import behavior_service
from app.services.malware_service import malware_service
from app.services.file_monitor import file_monitor
from app.services.threat_engine import threat_engine
from app.utils.security import get_current_user
import tempfile
import os
import asyncio

router = APIRouter()


@router.get("/threat")
async def get_threat(user_id: str = Depends(get_current_user)):
    return await asyncio.get_event_loop().run_in_executor(None, threat_engine.calculate)


@router.get("/score")
async def get_score(user_id: str = Depends(get_current_user)):
    return await asyncio.get_event_loop().run_in_executor(None, threat_engine.get_security_score)


@router.get("/history")
async def get_threat_history(user_id: str = Depends(get_current_user), limit: int = 20):
    return threat_engine.get_history(limit)


@router.get("/resources")
async def get_resources(user_id: str = Depends(get_current_user)):
    return behavior_service.get_system_resources()


@router.get("/processes")
async def get_processes(user_id: str = Depends(get_current_user)):
    procs = await asyncio.get_event_loop().run_in_executor(None, behavior_service.get_running_processes)
    return {"processes": procs[:50]}


@router.get("/connections")
async def get_connections(user_id: str = Depends(get_current_user)):
    return {"connections": behavior_service.get_network_connections()[:50]}


@router.get("/startup")
async def get_startup(user_id: str = Depends(get_current_user)):
    return {"programs": behavior_service.get_startup_programs()}


@router.get("/file-monitor/status")
async def file_monitor_status(user_id: str = Depends(get_current_user)):
    return file_monitor.get_status()


@router.post("/scan-file")
async def scan_file(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    suffix = os.path.splitext(file.filename or "")[1] or ".tmp"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        return malware_service.scan_file(tmp_path)
    finally:
        os.unlink(tmp_path)
