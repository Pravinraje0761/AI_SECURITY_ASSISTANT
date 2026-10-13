# Real-Time Monitoring System
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. SYSTEM OVERVIEW

This document provides complete implementation details for the Real-Time Monitoring System, including monitoring services, data collection, and backend integration.

### 1.1 System Purpose

Monitor system activities in real-time for threat detection:
- Process monitoring
- CPU and RAM usage tracking
- Network connection monitoring
- File system change detection
- Browser activity tracking
- Real-time data transmission to backend

### 1.2 Monitoring Components

- **Process Monitor**: Track running processes and resource usage
- **Resource Monitor**: CPU, RAM, disk usage monitoring
- **Network Monitor**: Network connections and traffic
- **File Monitor**: File system change detection
- **Browser Monitor**: Browser activity tracking
- **Data Transmitter**: Send monitoring data to backend

### 1.3 Performance Requirements

- **CPU Usage**: < 5% overhead
- **Memory Usage**: < 100 MB
- **Data Collection Interval**: 2-5 seconds
- **Network Bandwidth**: < 1 MB/min

---

## 2. PROCESS MONITORING

### 2.1 Process Monitor Implementation

```python
import psutil
import time
from datetime import datetime
from typing import List, Dict

class ProcessMonitor:
    """Monitor system processes"""
    
    def __init__(self):
        self.suspicious_processes = set()
        self.high_cpu_threshold = 80.0
        self.high_memory_threshold = 90.0
    
    def get_processes(self) -> List[Dict]:
        """Get all running processes with details"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'create_time', 'status']):
            try:
                proc_info = proc.info
                proc_info['timestamp'] = datetime.now().isoformat()
                proc_info['is_suspicious'] = self._is_suspicious_process(proc_info)
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return processes
    
    def get_process_details(self, pid: int) -> Dict:
        """Get detailed information about a specific process"""
        try:
            proc = psutil.Process(pid)
            details = {
                'pid': proc.pid,
                'name': proc.name(),
                'exe': proc.exe(),
                'cmdline': proc.cmdline(),
                'username': proc.username(),
                'cpu_percent': proc.cpu_percent(interval=1),
                'memory_percent': proc.memory_percent(),
                'memory_info': dict(proc.memory_info()._asdict()),
                'num_threads': proc.num_threads(),
                'create_time': proc.create_time(),
                'status': proc.status(),
                'connections': len(proc.connections()),
                'open_files': len(proc.open_files()) if hasattr(proc, 'open_files') else 0
            }
            return details
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
    
    def _is_suspicious_process(self, proc_info: Dict) -> bool:
        """Check if process is suspicious"""
        suspicious_indicators = 0
        
        # High CPU usage
        if proc_info.get('cpu_percent', 0) > self.high_cpu_threshold:
            suspicious_indicators += 1
        
        # High memory usage
        if proc_info.get('memory_percent', 0) > self.high_memory_threshold:
            suspicious_indicators += 1
        
        # Suspicious process names
        suspicious_names = ['miner', 'cryptonight', 'xmr', 'bitcoin', 'malware']
        proc_name = proc_info.get('name', '').lower()
        if any(susp in proc_name for susp in suspicious_names):
            suspicious_indicators += 2
        
        # Running from temp directory
        exe_path = proc_info.get('exe', '')
        if exe_path and ('temp' in exe_path.lower() or 'tmp' in exe_path.lower()):
            suspicious_indicators += 1
        
        return suspicious_indicators >= 2
    
    def kill_process(self, pid: int) -> bool:
        """Kill a process by PID"""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=5)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def monitor_processes(self, interval: int = 5):
        """Continuously monitor processes"""
        while True:
            processes = self.get_processes()
            suspicious = [p for p in processes if p['is_suspicious']]
            
            if suspicious:
                print(f"Found {len(suspicious)} suspicious processes")
                for proc in suspicious:
                    print(f"  PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, Memory: {proc['memory_percent']}%")
            
            time.sleep(interval)
```

---

## 3. RESOURCE MONITORING

### 3.1 Resource Monitor Implementation

```python
import psutil
import time
from datetime import datetime

class ResourceMonitor:
    """Monitor system resources (CPU, RAM, Disk)"""
    
    def __init__(self):
        self.cpu_threshold = 90.0
        self.memory_threshold = 90.0
        self.disk_threshold = 90.0
    
    def get_cpu_usage(self) -> Dict:
        """Get CPU usage statistics"""
        cpu_info = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_count': psutil.cpu_count(),
            'cpu_count_logical': psutil.cpu_count(logical=True),
            'cpu_freq': dict(psutil.cpu_freq()._asdict()) if psutil.cpu_freq() else None,
            'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
            'is_high_usage': False
        }
        
        cpu_info['is_high_usage'] = cpu_info['cpu_percent'] > self.cpu_threshold
        
        return cpu_info
    
    def get_memory_usage(self) -> Dict:
        """Get memory usage statistics"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        memory_info = {
            'timestamp': datetime.now().isoformat(),
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent,
            'is_high_usage': memory.percent > self.memory_threshold,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_free': swap.free,
            'swap_percent': swap.percent
        }
        
        return memory_info
    
    def get_disk_usage(self) -> Dict:
        """Get disk usage statistics"""
        disk_info = {
            'timestamp': datetime.now().isoformat(),
            'partitions': []
        }
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partition_info = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent,
                    'is_high_usage': usage.percent > self.disk_threshold
                }
                disk_info['partitions'].append(partition_info)
            except (PermissionError, OSError):
                continue
        
        return disk_info
    
    def get_all_resources(self) -> Dict:
        """Get all resource information"""
        return {
            'cpu': self.get_cpu_usage(),
            'memory': self.get_memory_usage(),
            'disk': self.get_disk_usage()
        }
    
    def monitor_resources(self, interval: int = 2):
        """Continuously monitor resources"""
        while True:
            resources = self.get_all_resources()
            
            # Check for high usage
            if resources['cpu']['is_high_usage']:
                print(f"WARNING: High CPU usage: {resources['cpu']['cpu_percent']}%")
            
            if resources['memory']['is_high_usage']:
                print(f"WARNING: High memory usage: {resources['memory']['percent']}%")
            
            for partition in resources['disk']['partitions']:
                if partition['is_high_usage']:
                    print(f"WARNING: High disk usage on {partition['mountpoint']}: {partition['percent']}%")
            
            time.sleep(interval)
```

---

## 4. NETWORK MONITORING

### 4.1 Network Monitor Implementation

```python
import psutil
import socket
from datetime import datetime
from typing import List, Dict

class NetworkMonitor:
    """Monitor network connections and traffic"""
    
    def __init__(self):
        self.suspicious_ports = [6666, 31337, 12345, 54321]
        self.suspicious_ips = set()
        self.known_malicious_ips = self._load_malicious_ips()
    
    def _load_malicious_ips(self) -> set:
        """Load known malicious IP addresses"""
        # In production, load from threat intelligence feed
        return set()
    
    def get_connections(self) -> List[Dict]:
        """Get all network connections"""
        connections = []
        
        for conn in psutil.net_connections(kind='inet'):
            try:
                conn_info = {
                    'timestamp': datetime.now().isoformat(),
                    'pid': conn.pid,
                    'local_address': conn.laddr[0] if conn.laddr else None,
                    'local_port': conn.laddr[1] if conn.laddr else None,
                    'remote_address': conn.raddr[0] if conn.raddr else None,
                    'remote_port': conn.raddr[1] if conn.raddr else None,
                    'status': conn.status,
                    'protocol': conn.type,
                    'is_suspicious': self._is_suspicious_connection(conn)
                }
                connections.append(conn_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return connections
    
    def _is_suspicious_connection(self, conn) -> bool:
        """Check if connection is suspicious"""
        suspicious_indicators = 0
        
        # Check for suspicious ports
        if conn.raddr:
            remote_port = conn.raddr[1]
            if remote_port in self.suspicious_ports:
                suspicious_indicators += 2
            
            # Check for known malicious IPs
            remote_ip = conn.raddr[0]
            if remote_ip in self.known_malicious_ips:
                suspicious_indicators += 3
        
        # Check connection status
        if conn.status == 'ESTABLISHED' and not conn.raddr:
            suspicious_indicators += 1
        
        return suspicious_indicators >= 2
    
    def get_network_stats(self) -> Dict:
        """Get network statistics"""
        stats = psutil.net_io_counters()
        
        network_info = {
            'timestamp': datetime.now().isoformat(),
            'bytes_sent': stats.bytes_sent,
            'bytes_recv': stats.bytes_recv,
            'packets_sent': stats.packets_sent,
            'packets_recv': stats.packets_recv,
            'errin': stats.errin,
            'errout': stats.errout,
            'dropin': stats.dropin,
            'dropout': stats.dropout
        }
        
        return network_info
    
    def get_network_interfaces(self) -> Dict:
        """Get network interface information"""
        interfaces = {}
        
        for name, addrs in psutil.net_if_addrs().items():
            interface_info = {
                'name': name,
                'addresses': []
            }
            
            for addr in addrs:
                addr_info = {
                    'family': str(addr.family),
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast
                }
                interface_info['addresses'].append(addr_info)
            
            interfaces[name] = interface_info
        
        return interfaces
    
    def block_connection(self, local_port: int) -> bool:
        """Block a connection by local port (requires admin privileges)"""
        # This would typically use firewall rules
        # Implementation depends on OS
        return False
    
    def monitor_network(self, interval: int = 5):
        """Continuously monitor network"""
        while True:
            connections = self.get_connections()
            suspicious = [c for c in connections if c['is_suspicious']]
            
            if suspicious:
                print(f"Found {len(suspicious)} suspicious connections")
                for conn in suspicious:
                    print(f"  PID: {conn['pid']}, Remote: {conn['remote_address']}:{conn['remote_port']}")
            
            time.sleep(interval)
```

---

## 5. FILE SYSTEM MONITORING

### 5.1 File Monitor Implementation

```python
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from typing import List, Dict

class FileEventHandler(FileSystemEventHandler):
    """Handle file system events"""
    
    def __init__(self, callback):
        self.callback = callback
    
    def on_created(self, event):
        if not event.is_directory:
            self.callback({
                'event_type': 'created',
                'path': event.src_path,
                'timestamp': datetime.now().isoformat()
            })
    
    def on_modified(self, event):
        if not event.is_directory:
            self.callback({
                'event_type': 'modified',
                'path': event.src_path,
                'timestamp': datetime.now().isoformat()
            })
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.callback({
                'event_type': 'deleted',
                'path': event.src_path,
                'timestamp': datetime.now().isoformat()
            })
    
    def on_moved(self, event):
        if not event.is_directory:
            self.callback({
                'event_type': 'moved',
                'src_path': event.src_path,
                'dest_path': event.dest_path,
                'timestamp': datetime.now().isoformat()
            })

class FileMonitor:
    """Monitor file system changes"""
    
    def __init__(self):
        self.observer = Observer()
        self.monitored_paths = []
        self.file_events = []
        self.suspicious_extensions = ['.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.jar']
        self.suspicious_directories = ['temp', 'tmp', 'appdata', 'startup']
    
    def add_watch_path(self, path: str):
        """Add a path to monitor"""
        if os.path.exists(path):
            event_handler = FileEventHandler(self._on_file_event)
            self.observer.schedule(event_handler, path, recursive=True)
            self.monitored_paths.append(path)
            print(f"Added watch path: {path}")
        else:
            print(f"Path does not exist: {path}")
    
    def _on_file_event(self, event: Dict):
        """Handle file event"""
        # Check if event is suspicious
        event['is_suspicious'] = self._is_suspicious_event(event)
        
        self.file_events.append(event)
        
        # Keep only last 1000 events
        if len(self.file_events) > 1000:
            self.file_events = self.file_events[-1000:]
        
        if event['is_suspicious']:
            print(f"Suspicious file event: {event['event_type']} - {event.get('path', event.get('src_path'))}")
    
    def _is_suspicious_event(self, event: Dict) -> bool:
        """Check if file event is suspicious"""
        suspicious_indicators = 0
        
        path = event.get('path') or event.get('src_path', '')
        
        # Check file extension
        for ext in self.suspicious_extensions:
            if path.lower().endswith(ext):
                suspicious_indicators += 2
        
        # Check directory
        path_lower = path.lower()
        for dir_name in self.suspicious_directories:
            if dir_name in path_lower:
                suspicious_indicators += 1
        
        # Check event type
        if event['event_type'] in ['created', 'modified']:
            suspicious_indicators += 1
        
        return suspicious_indicators >= 2
    
    def start_monitoring(self):
        """Start file system monitoring"""
        self.observer.start()
        print("File monitoring started")
    
    def stop_monitoring(self):
        """Stop file system monitoring"""
        self.observer.stop()
        self.observer.join()
        print("File monitoring stopped")
    
    def get_recent_events(self, count: int = 100) -> List[Dict]:
        """Get recent file events"""
        return self.file_events[-count:]
```

---

## 6. BROWSER MONITOR

### 6.1 Browser Monitor Implementation

```python
import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict

class BrowserMonitor:
    """Monitor browser activities"""
    
    def __init__(self):
        self.browser_paths = self._get_browser_paths()
        self.suspicious_keywords = ['phishing', 'malware', 'crack', 'hack', 'torrent']
    
    def _get_browser_paths(self) -> Dict[str, str]:
        """Get browser history database paths"""
        paths = {}
        
        # Chrome
        chrome_path = os.path.expanduser(
            r'~\AppData\Local\Google\Chrome\User Data\Default\History'
        )
        if os.path.exists(chrome_path):
            paths['chrome'] = chrome_path
        
        # Firefox
        firefox_path = os.path.expanduser(
            r'~\AppData\Roaming\Mozilla\Firefox\Profiles'
        )
        if os.path.exists(firefox_path):
            # Find default profile
            for profile in os.listdir(firefox_path):
                if 'default' in profile.lower():
                    history_path = os.path.join(firefox_path, profile, 'places.sqlite')
                    if os.path.exists(history_path):
                        paths['firefox'] = history_path
                        break
        
        # Edge
        edge_path = os.path.expanduser(
            r'~\AppData\Local\Microsoft\Edge\User Data\Default\History'
        )
        if os.path.exists(edge_path):
            paths['edge'] = edge_path
        
        return paths
    
    def get_chrome_history(self, limit: int = 100) -> List[Dict]:
        """Get Chrome browsing history"""
        history = []
        
        if 'chrome' not in self.browser_paths:
            return history
        
        try:
            # Copy database to avoid lock
            import shutil
            temp_path = self.browser_paths['chrome'] + '.tmp'
            shutil.copy2(self.browser_paths['chrome'], temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT url, title, last_visit_time, visit_count
                FROM urls
                ORDER BY last_visit_time DESC
                LIMIT ?
            """, (limit,))
            
            for row in cursor.fetchall():
                history.append({
                    'browser': 'chrome',
                    'url': row[0],
                    'title': row[1],
                    'timestamp': self._chrome_time_to_datetime(row[2]),
                    'visit_count': row[3],
                    'is_suspicious': self._is_suspicious_url(row[0])
                })
            
            conn.close()
            os.remove(temp_path)
            
        except Exception as e:
            print(f"Error reading Chrome history: {e}")
        
        return history
    
    def get_firefox_history(self, limit: int = 100) -> List[Dict]:
        """Get Firefox browsing history"""
        history = []
        
        if 'firefox' not in self.browser_paths:
            return history
        
        try:
            import shutil
            temp_path = self.browser_paths['firefox'] + '.tmp'
            shutil.copy2(self.browser_paths['firefox'], temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT url, title, last_visit_date, visit_count
                FROM moz_places
                ORDER BY last_visit_date DESC
                LIMIT ?
            """, (limit,))
            
            for row in cursor.fetchall():
                history.append({
                    'browser': 'firefox',
                    'url': row[0],
                    'title': row[1],
                    'timestamp': self._firefox_time_to_datetime(row[2]),
                    'visit_count': row[3],
                    'is_suspicious': self._is_suspicious_url(row[0])
                })
            
            conn.close()
            os.remove(temp_path)
            
        except Exception as e:
            print(f"Error reading Firefox history: {e}")
        
        return history
    
    def _chrome_time_to_datetime(self, chrome_time: int) -> str:
        """Convert Chrome timestamp to datetime"""
        return datetime.fromtimestamp(chrome_time / 1000000 - 11644473600).isoformat()
    
    def _firefox_time_to_datetime(self, firefox_time: int) -> str:
        """Convert Firefox timestamp to datetime"""
        return datetime.fromtimestamp(firefox_time / 1000000).isoformat()
    
    def _is_suspicious_url(self, url: str) -> bool:
        """Check if URL is suspicious"""
        url_lower = url.lower()
        return any(keyword in url_lower for keyword in self.suspicious_keywords)
    
    def get_all_history(self, limit: int = 100) -> List[Dict]:
        """Get history from all browsers"""
        all_history = []
        
        if 'chrome' in self.browser_paths:
            all_history.extend(self.get_chrome_history(limit))
        
        if 'firefox' in self.browser_paths:
            all_history.extend(self.get_firefox_history(limit))
        
        # Sort by timestamp
        all_history.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_history[:limit]
    
    def get_downloads(self, browser: str = 'chrome') -> List[Dict]:
        """Get download history"""
        downloads = []
        
        # Implementation depends on browser
        # Chrome: downloads table in History database
        # Firefox: downloads table in places.sqlite
        
        return downloads
```

---

## 7. DATA TRANSMITTER

### 7.1 Data Transmitter Implementation

```python
import requests
import json
import time
from datetime import datetime
from typing import Dict, Optional

class DataTransmitter:
    """Transmit monitoring data to backend"""
    
    def __init__(self, backend_url: str, api_key: str):
        self.backend_url = backend_url
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def send_monitoring_data(self, data: Dict) -> bool:
        """Send monitoring data to backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/monitoring/data",
                headers=self.headers,
                json=data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending data: {e}")
            return False
    
    def send_alert(self, alert: Dict) -> bool:
        """Send alert to backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/alerts",
                headers=self.headers,
                json=alert,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending alert: {e}")
            return False
    
    def send_heartbeat(self) -> bool:
        """Send heartbeat to backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/monitoring/heartbeat",
                headers=self.headers,
                json={'timestamp': datetime.now().isoformat()},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending heartbeat: {e}")
            return False
```

---

## 8. MONITORING SERVICE

### 8.1 Main Monitoring Service

```python
import time
import threading
from datetime import datetime
from process_monitor import ProcessMonitor
from resource_monitor import ResourceMonitor
from network_monitor import NetworkMonitor
from file_monitor import FileMonitor
from browser_monitor import BrowserMonitor
from data_transmitter import DataTransmitter

class MonitoringService:
    """Main monitoring service"""
    
    def __init__(self, backend_url: str, api_key: str):
        self.process_monitor = ProcessMonitor()
        self.resource_monitor = ResourceMonitor()
        self.network_monitor = NetworkMonitor()
        self.file_monitor = FileMonitor()
        self.browser_monitor = BrowserMonitor()
        self.transmitter = DataTransmitter(backend_url, api_key)
        
        self.is_running = False
        self.monitoring_threads = []
        
        # Monitoring intervals
        self.process_interval = 5
        self.resource_interval = 2
        self.network_interval = 5
        self.browser_interval = 10
    
    def start(self):
        """Start monitoring service"""
        print("Starting monitoring service...")
        
        self.is_running = True
        
        # Start file monitoring
        self.file_monitor.add_watch_path(os.path.expanduser('~/Downloads'))
        self.file_monitor.add_watch_path(os.path.expanduser('~/Desktop'))
        self.file_monitor.start_monitoring()
        
        # Start monitoring threads
        self.monitoring_threads = [
            threading.Thread(target=self._monitor_processes, daemon=True),
            threading.Thread(target=self._monitor_resources, daemon=True),
            threading.Thread(target=self._monitor_network, daemon=True),
            threading.Thread(target=self._monitor_browser, daemon=True),
            threading.Thread(target=self._send_heartbeat, daemon=True)
        ]
        
        for thread in self.monitoring_threads:
            thread.start()
        
        print("Monitoring service started")
    
    def stop(self):
        """Stop monitoring service"""
        print("Stopping monitoring service...")
        
        self.is_running = False
        self.file_monitor.stop_monitoring()
        
        for thread in self.monitoring_threads:
            thread.join(timeout=5)
        
        print("Monitoring service stopped")
    
    def _monitor_processes(self):
        """Monitor processes"""
        while self.is_running:
            processes = self.process_monitor.get_processes()
            suspicious = [p for p in processes if p['is_suspicious']]
            
            # Send data to backend
            data = {
                'type': 'process',
                'timestamp': datetime.now().isoformat(),
                'data': processes,
                'suspicious_count': len(suspicious)
            }
            self.transmitter.send_monitoring_data(data)
            
            # Send alerts for suspicious processes
            for proc in suspicious:
                alert = {
                    'type': 'suspicious_process',
                    'severity': 'high',
                    'message': f"Suspicious process detected: {proc['name']} (PID: {proc['pid']})",
                    'data': proc,
                    'timestamp': datetime.now().isoformat()
                }
                self.transmitter.send_alert(alert)
            
            time.sleep(self.process_interval)
    
    def _monitor_resources(self):
        """Monitor system resources"""
        while self.is_running:
            resources = self.resource_monitor.get_all_resources()
            
            # Send data to backend
            data = {
                'type': 'resource',
                'timestamp': datetime.now().isoformat(),
                'data': resources
            }
            self.transmitter.send_monitoring_data(data)
            
            # Send alerts for high resource usage
            if resources['cpu']['is_high_usage']:
                alert = {
                    'type': 'high_cpu',
                    'severity': 'medium',
                    'message': f"High CPU usage: {resources['cpu']['cpu_percent']}%",
                    'data': resources['cpu'],
                    'timestamp': datetime.now().isoformat()
                }
                self.transmitter.send_alert(alert)
            
            if resources['memory']['is_high_usage']:
                alert = {
                    'type': 'high_memory',
                    'severity': 'medium',
                    'message': f"High memory usage: {resources['memory']['percent']}%",
                    'data': resources['memory'],
                    'timestamp': datetime.now().isoformat()
                }
                self.transmitter.send_alert(alert)
            
            time.sleep(self.resource_interval)
    
    def _monitor_network(self):
        """Monitor network"""
        while self.is_running:
            connections = self.network_monitor.get_connections()
            stats = self.network_monitor.get_network_stats()
            
            suspicious = [c for c in connections if c['is_suspicious']]
            
            # Send data to backend
            data = {
                'type': 'network',
                'timestamp': datetime.now().isoformat(),
                'connections': connections,
                'stats': stats,
                'suspicious_count': len(suspicious)
            }
            self.transmitter.send_monitoring_data(data)
            
            # Send alerts for suspicious connections
            for conn in suspicious:
                alert = {
                    'type': 'suspicious_connection',
                    'severity': 'high',
                    'message': f"Suspicious network connection: {conn['remote_address']}:{conn['remote_port']}",
                    'data': conn,
                    'timestamp': datetime.now().isoformat()
                }
                self.transmitter.send_alert(alert)
            
            time.sleep(self.network_interval)
    
    def _monitor_browser(self):
        """Monitor browser activity"""
        while self.is_running:
            history = self.browser_monitor.get_all_history(limit=50)
            suspicious = [h for h in history if h['is_suspicious']]
            
            # Send data to backend
            data = {
                'type': 'browser',
                'timestamp': datetime.now().isoformat(),
                'history': history,
                'suspicious_count': len(suspicious)
            }
            self.transmitter.send_monitoring_data(data)
            
            # Send alerts for suspicious URLs
            for item in suspicious:
                alert = {
                    'type': 'suspicious_url',
                    'severity': 'medium',
                    'message': f"Suspicious URL visited: {item['url']}",
                    'data': item,
                    'timestamp': datetime.now().isoformat()
                }
                self.transmitter.send_alert(alert)
            
            time.sleep(self.browser_interval)
    
    def _send_heartbeat(self):
        """Send heartbeat to backend"""
        while self.is_running:
            self.transmitter.send_heartbeat()
            time.sleep(30)  # Every 30 seconds
    
    def get_status(self) -> Dict:
        """Get monitoring service status"""
        return {
            'is_running': self.is_running,
            'monitored_paths': self.file_monitor.monitored_paths,
            'process_interval': self.process_interval,
            'resource_interval': self.resource_interval,
            'network_interval': self.network_interval,
            'browser_interval': self.browser_interval
        }
```

---

## 9. DESKTOP AGENT

### 9.1 Desktop Agent Application

```python
# desktop_agent.py
import sys
import os
import signal
import argparse
from monitoring_service import MonitoringService

def main():
    parser = argparse.ArgumentParser(description='AI Digital Bodyguard Desktop Agent')
    parser.add_argument('--backend-url', required=True, help='Backend API URL')
    parser.add_argument('--api-key', required=True, help='API key for authentication')
    parser.add_argument('--monitor-downloads', action='store_true', help='Monitor downloads folder')
    parser.add_argument('--monitor-desktop', action='store_true', help='Monitor desktop folder')
    
    args = parser.parse_args()
    
    print("AI Digital Bodyguard - Desktop Agent")
    print("=" * 50)
    
    # Initialize monitoring service
    service = MonitoringService(args.backend_url, args.api_key)
    
    # Add monitoring paths
    if args.monitor_downloads:
        service.file_monitor.add_watch_path(os.path.expanduser('~/Downloads'))
    
    if args.monitor_desktop:
        service.file_monitor.add_watch_path(os.path.expanduser('~/Desktop'))
    
    # Handle shutdown gracefully
    def signal_handler(sig, frame):
        print("\nShutting down...")
        service.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start monitoring
    service.start()
    
    print("Desktop agent is running. Press Ctrl+C to stop.")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
```

### 9.2 Requirements File

```txt
# requirements_monitoring.txt
psutil>=5.9.0
watchdog>=3.0.0
requests>=2.31.0
pywin32>=306 (Windows only)
```

---

## 10. DEPLOYMENT

### 10.1 Windows Service

```python
# windows_service.py
import sys
import os
import win32service
import win32serviceutil
import win32event
import servicemanager
from desktop_agent import MonitoringService

class DigitalBodyguardService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DigitalBodyguard"
    _svc_display_name_ = "AI Digital Bodyguard"
    _svc_description_ = "AI-Powered Digital Bodyguard for Cyber Threat Detection"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.service = None
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.service:
            self.service.stop()
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, '')
        )
    
    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        # Get configuration from registry or config file
        backend_url = "http://localhost:8000"
        api_key = "your-api-key"
        
        self.service = MonitoringService(backend_url, api_key)
        self.service.start()
        
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DigitalBodyguardService)
```

### 10.2 Dockerfile (for Linux)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_monitoring.txt .
RUN pip install --no-cache-dir -r requirements_monitoring.txt

# Copy application code
COPY desktop_agent.py .
COPY process_monitor.py .
COPY resource_monitor.py .
COPY network_monitor.py .
COPY file_monitor.py .
COPY browser_monitor.py .
COPY data_transmitter.py .
COPY monitoring_service.py .

# Expose port for health checks
EXPOSE 8080

# Run application
CMD ["python", "desktop_agent.py", "--backend-url", "http://backend:8000", "--api-key", "${API_KEY}"]
```

### 10.3 Docker Compose

```yaml
version: '3.8'

services:
  desktop-agent:
    build: .
    environment:
      - BACKEND_URL=http://backend:8000
      - API_KEY=${API_KEY}
    volumes:
      - /home/user/Downloads:/downloads
      - /home/user/Desktop:/desktop
    restart: unless-stopped
```

---

## 11. CONCLUSION

This document provides complete implementation for the Real-Time Monitoring System including:

- **Process Monitoring**: Track running processes with suspicious detection
- **Resource Monitoring**: CPU, RAM, disk usage with threshold alerts
- **Network Monitoring**: Connection tracking with suspicious detection
- **File System Monitoring**: Real-time file change detection
- **Browser Monitoring**: History tracking with suspicious URL detection
- **Data Transmitter**: Send monitoring data to backend API
- **Monitoring Service**: Orchestrate all monitoring components
- **Desktop Agent**: Standalone application for deployment

**Next Steps:**
1. Install monitoring agent on target systems
2. Configure monitoring paths and thresholds
3. Deploy backend API to receive monitoring data
4. Set up alert processing and notification
5. Integrate with threat detection models

---

## APPENDICES

### Appendix A: Configuration File

```json
{
  "backend_url": "http://localhost:8000",
  "api_key": "your-api-key",
  "monitoring": {
    "process_interval": 5,
    "resource_interval": 2,
    "network_interval": 5,
    "browser_interval": 10
  },
  "thresholds": {
    "high_cpu": 90.0,
    "high_memory": 90.0,
    "high_disk": 90.0
  },
  "paths": {
    "monitor_downloads": true,
    "monitor_desktop": true,
    "custom_paths": []
  }
}
```

### Appendix B: Installation Script (Windows)

```batch
@echo off
echo Installing AI Digital Bodyguard Desktop Agent...

REM Create installation directory
mkdir "C:\Program Files\DigitalBodyguard"
cd /d "C:\Program Files\DigitalBodyguard"

REM Copy files
copy desktop_agent.py .
copy process_monitor.py .
copy resource_monitor.py .
copy network_monitor.py .
copy file_monitor.py .
copy browser_monitor.py .
copy data_transmitter.py .
copy monitoring_service.py .

REM Install Python dependencies
python -m pip install -r requirements_monitoring.txt

REM Install as Windows service
python windows_service.py install

REM Start service
python windows_service.py start

echo Installation complete!
```

### Appendix C: System Tray Application

```python
# system_tray.py
import sys
import tkinter as tk
from tkinter import messagebox
from monitoring_service import MonitoringService

class SystemTrayApp:
    def __init__(self, backend_url, api_key):
        self.service = MonitoringService(backend_url, api_key)
        self.service.start()
        
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        
        # Create system tray icon (requires pystray)
        # Implementation depends on OS
        
    def show_status(self):
        status = self.service.get_status()
        messagebox.showinfo("Status", f"Monitoring: {status['is_running']}")
    
    def stop_monitoring(self):
        self.service.stop()
        self.root.quit()
```
