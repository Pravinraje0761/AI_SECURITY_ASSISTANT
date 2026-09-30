import psutil
import socket
from typing import Dict, List
from datetime import datetime


class BehaviorService:
    MONITORED_PORTS = {
        4444: 'Metasploit default', 5555: 'Android debug', 1337: 'Back Orifice',
        31337: 'Back Orifice', 1234: 'Common trojan', 6667: 'IRC bot/C&C',
    }
    SUSPICIOUS_PROCS = {
        'nc.exe', 'ncat.exe', 'mimikatz.exe', 'psexec.exe', 'procdump.exe',
        'accesschk.exe', 'meterpreter', 'keylogger', 'wireshark.exe', 'nmap.exe',
    }

    def get_system_resources(self) -> Dict:
        psutil.cpu_percent(interval=None)
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        boot = psutil.boot_time()
        uptime = datetime.now().timestamp() - boot
        return {
            "cpu_percent": cpu,
            "cpu_count": psutil.cpu_count(),
            "memory_total": mem.total,
            "memory_used": mem.used,
            "memory_percent": mem.percent,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_percent": disk.percent,
            "net_bytes_sent": net.bytes_sent,
            "net_bytes_recv": net.bytes_recv,
            "uptime_seconds": int(uptime),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_running_processes(self) -> List[Dict]:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'memory_percent', 'status', 'username']):
            try:
                info = p.info
                name = (info.get('name') or '').lower()
                procs.append({
                    "pid": info['pid'],
                    "name": info.get('name', '?'),
                    "memory": round(info.get('memory_percent', 0) or 0, 1),
                    "status": info.get('status', '?'),
                    "user": info.get('username', '?'),
                    "suspicious": name in self.SUSPICIOUS_PROCS,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(procs, key=lambda x: x.get('memory', 0), reverse=True)[:100]

    def get_network_connections(self) -> List[Dict]:
        conns = []
        for c in psutil.net_connections(kind='inet'):
            try:
                remote_ip = c.raddr.ip if c.raddr else ''
                remote_port = c.raddr.port if c.raddr else 0
                local_port = c.laddr.port if c.laddr else 0
                hostname = ''
                risk = self.MONITORED_PORTS.get(remote_port)
                conns.append({
                    "local_port": local_port,
                    "remote_ip": remote_ip,
                    "remote_port": remote_port,
                    "remote_host": hostname,
                    "status": c.status,
                    "pid": c.pid,
                    "suspicious": risk is not None or c.status == 'SYN_SENT',
                    "risk_note": risk or '',
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return conns

    def get_startup_programs(self) -> List[Dict]:
        startup = []
        try:
            import winreg
            paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            ]
            for hive, path in paths:
                try:
                    key = winreg.OpenKey(hive, path)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup.append({"name": name, "path": value, "hive": "HKCU" if hive == winreg.HKEY_CURRENT_USER else "HKLM"})
                            i += 1
                        except OSError:
                            break
                    winreg.CloseKey(key)
                except OSError:
                    continue
        except ImportError:
            pass
        return startup

    def get_behavior_summary(self) -> Dict:
        resources = self.get_system_resources()
        procs = self.get_running_processes()
        conns = self.get_network_connections()
        suspicious_p = [p for p in procs if p['suspicious']]
        suspicious_c = [c for c in conns if c['suspicious']]
        risk = 0
        indicators = []
        if suspicious_p:
            risk += 40
            indicators.append(f"{len(suspicious_p)} suspicious process(es)")
        if suspicious_c:
            risk += 30
            indicators.append(f"{len(suspicious_c)} suspicious connection(s)")
        if resources['cpu_percent'] > 90:
            risk += 10
            indicators.append("CPU > 90%")
        if resources['memory_percent'] > 90:
            risk += 10
            indicators.append("Memory > 90%")
        return {
            "resources": resources,
            "process_count": len(procs),
            "connection_count": len(conns),
            "suspicious_processes": suspicious_p,
            "suspicious_connections": suspicious_c,
            "risk_score": min(risk, 100),
            "indicators": indicators,
            "timestamp": datetime.utcnow().isoformat(),
        }


behavior_service = BehaviorService()
