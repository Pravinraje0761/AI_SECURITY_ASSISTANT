# Database Design
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. DATABASE OVERVIEW

This document provides complete database schema design for the AI-Powered Digital Bodyguard system using PostgreSQL.

### 1.1 Database Purpose

Store and manage all system data including:
- User accounts and authentication
- Alerts and notifications
- Threat detection results
- Scan history
- Monitoring data
- User behavior baselines
- System logs

### 1.2 Database Technology

- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Connection Pooling**: SQLAlchemy connection pool
- **Backup**: pg_dump

### 1.3 Database Name

- **Production**: `digital_bodyguard`
- **Development**: `digital_bodyguard_dev`
- **Testing**: `digital_bodyguard_test`

---

## 2. ENTITY RELATIONSHIP DIAGRAM

```
┌─────────────────┐       ┌─────────────────┐
│     users       │       │     alerts       │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────│ user_id (FK)    │
│ email           │       │ id (PK)         │
│ password_hash   │       │ type            │
│ first_name      │       │ severity        │
│ last_name       │       │ title           │
│ role            │       │ message         │
│ is_active       │       │ status          │
│ created_at      │       │ acknowledged_at │
│ last_login      │       │ dismissed_at    │
└─────────────────┘       │ created_at      │
                          └─────────────────┘
                                   │
                                   │
┌─────────────────┐       ┌─────────────────┐
│     scans       │       │    threats      │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ user_id (FK)    │◄──────│ user_id (FK)    │
│ type            │       │ type            │
│ target          │       │ source          │
│ result          │       │ threat_score    │
│ score           │       │ attack_type     │
│ details         │       │ status          │
│ created_at      │       │ details         │
└─────────────────┘       │ created_at      │
                          │ updated_at      │
                          └─────────────────┘
                                   │
                                   │
┌─────────────────┐       ┌─────────────────┐
│ monitoring_data │       │ behavior_data   │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ user_id (FK)    │◄──────│ user_id (FK)    │
│ type            │       │ timestamp       │
│ data            │       │ login_hour      │
│ created_at      │       │ file_access_cnt │
└─────────────────┘       │ network_activity│
                          │ session_duration│
                          │ is_anomalous    │
                          └─────────────────┘
                                   │
                                   │
                          ┌─────────────────┐
                          │   baselines     │
                          ├─────────────────┤
                          │ id (PK)         │
                          │ user_id (FK)    │◄──────
                          │ feature_name    │
                          │ mean            │
                          │ std             │
                          │ created_at      │
                          │ updated_at      │
                          └─────────────────┘
```

---

## 3. TABLE SCHEMAS

### 3.1 Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Comments
COMMENT ON TABLE users IS 'User accounts and authentication information';
COMMENT ON COLUMN users.role IS 'User role: user or admin';
COMMENT ON COLUMN users.is_active IS 'Account active status';
```

### 3.2 Alerts Table

```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('phishing', 'malware', 'behavior', 'network', 'system')),
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    title VARCHAR(255) NOT NULL,
    message TEXT,
    data JSONB,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'acknowledged', 'dismissed')),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    dismissed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_status_transition CHECK (
        (status = 'new' AND acknowledged_at IS NULL AND dismissed_at IS NULL) OR
        (status = 'acknowledged' AND acknowledged_at IS NOT NULL AND dismissed_at IS NULL) OR
        (status = 'dismissed' AND dismissed_at IS NOT NULL)
    )
);

-- Indexes
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_alerts_type ON alerts(type);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_created_at ON alerts(created_at DESC);
CREATE INDEX idx_alerts_user_status ON alerts(user_id, status);

-- Comments
COMMENT ON TABLE alerts IS 'Security alerts and notifications';
COMMENT ON COLUMN alerts.type IS 'Alert type classification';
COMMENT ON COLUMN alerts.severity IS 'Alert severity level';
COMMENT ON COLUMN alerts.data IS 'Additional alert data in JSON format';
```

### 3.3 Threats Table

```sql
CREATE TABLE threats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('phishing', 'malware', 'behavior', 'network', 'ransomware')),
    source VARCHAR(255),
    threat_score DECIMAL(5,2) CHECK (threat_score BETWEEN 0 AND 100),
    attack_type VARCHAR(100),
    status VARCHAR(20) DEFAULT 'detected' CHECK (status IN ('detected', 'investigating', 'resolved', 'false_positive')),
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_threats_user_id ON threats(user_id);
CREATE INDEX idx_threats_type ON threats(type);
CREATE INDEX idx_threats_status ON threats(status);
CREATE INDEX idx_threats_threat_score ON threats(threat_score DESC);
CREATE INDEX idx_threats_created_at ON threats(created_at DESC);

-- Comments
COMMENT ON TABLE threats IS 'Detected threats and their details';
COMMENT ON COLUMN threats.threat_score IS 'Threat score between 0 and 100';
COMMENT ON COLUMN threats.status IS 'Threat investigation status';
```

### 3.4 Scans Table

```sql
CREATE TABLE scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('phishing', 'malware')),
    target VARCHAR(2048) NOT NULL,
    result VARCHAR(20) NOT NULL CHECK (result IN ('malicious', 'benign', 'suspicious', 'error')),
    score DECIMAL(5,2) CHECK (score BETWEEN 0 AND 1),
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_scans_user_id ON scans(user_id);
CREATE INDEX idx_scans_type ON scans(type);
CREATE INDEX idx_scans_result ON scans(result);
CREATE INDEX idx_scans_created_at ON scans(created_at DESC);
CREATE INDEX idx_scans_user_created ON scans(user_id, created_at DESC);

-- Comments
COMMENT ON TABLE scans IS 'Scan history for URLs and files';
COMMENT ON COLUMN scans.target IS 'URL or file path that was scanned';
COMMENT ON COLUMN scans.score IS 'Malware/phishing probability score';
```

### 3.5 Monitoring Data Table

```sql
CREATE TABLE monitoring_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('process', 'resource', 'network', 'file', 'browser')),
    data JSONB NOT NULL,
    suspicious_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_monitoring_user_id ON monitoring_data(user_id);
CREATE INDEX idx_monitoring_type ON monitoring_data(type);
CREATE INDEX idx_monitoring_created_at ON monitoring_data(created_at DESC);
CREATE INDEX idx_monitoring_user_type ON monitoring_data(user_id, type);

-- Partition by date for large datasets
-- CREATE TABLE monitoring_data_y2026m07 PARTITION OF monitoring_data
-- FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

-- Comments
COMMENT ON TABLE monitoring_data IS 'Real-time monitoring data from desktop agents';
COMMENT ON COLUMN monitoring_data.type IS 'Type of monitoring data';
COMMENT ON COLUMN monitoring_data.data IS 'Monitoring data in JSON format';
```

### 3.6 Behavior Data Table

```sql
CREATE TABLE behavior_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    login_hour INTEGER CHECK (login_hour BETWEEN 0 AND 23),
    login_day_of_week INTEGER CHECK (login_day_of_week BETWEEN 0 AND 6),
    is_weekend BOOLEAN DEFAULT false,
    is_night BOOLEAN DEFAULT false,
    login_attempts INTEGER DEFAULT 1,
    failed_login_attempts INTEGER DEFAULT 0,
    login_location_changed BOOLEAN DEFAULT false,
    login_device_changed BOOLEAN DEFAULT false,
    login_ip_changed BOOLEAN DEFAULT false,
    file_access_count INTEGER DEFAULT 0,
    files_per_hour DECIMAL(10,2),
    suspicious_files_accessed INTEGER DEFAULT 0,
    suspicious_file_ratio DECIMAL(5,2),
    sensitive_dir_access INTEGER DEFAULT 0,
    sites_visited INTEGER DEFAULT 0,
    sites_per_hour DECIMAL(10,2),
    suspicious_sites_visited INTEGER DEFAULT 0,
    downloads INTEGER DEFAULT 0,
    network_activity_mb DECIMAL(10,2),
    network_per_hour DECIMAL(10,2),
    unique_endpoints INTEGER DEFAULT 0,
    suspicious_endpoints INTEGER DEFAULT 0,
    session_duration DECIMAL(10,2),
    is_long_session BOOLEAN DEFAULT false,
    is_short_session BOOLEAN DEFAULT false,
    is_anomalous BOOLEAN DEFAULT false,
    anomaly_score DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_behavior_user_id ON behavior_data(user_id);
CREATE INDEX idx_behavior_timestamp ON behavior_data(timestamp DESC);
CREATE INDEX idx_behavior_is_anomalous ON behavior_data(is_anomalous);
CREATE INDEX idx_behavior_user_timestamp ON behavior_data(user_id, timestamp DESC);

-- Comments
COMMENT ON TABLE behavior_data IS 'User behavior data for anomaly detection';
COMMENT ON COLUMN behavior_data.is_anomalous IS 'Flag indicating anomalous behavior';
COMMENT ON COLUMN behavior_data.anomaly_score IS 'Anomaly detection score';
```

### 3.7 Baselines Table

```sql
CREATE TABLE baselines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feature_name VARCHAR(100) NOT NULL,
    mean DECIMAL(15,4),
    std DECIMAL(15,4),
    min_value DECIMAL(15,4),
    max_value DECIMAL(15,4),
    median DECIMAL(15,4),
    q25 DECIMAL(15,4),
    q75 DECIMAL(15,4),
    sample_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, feature_name)
);

-- Indexes
CREATE INDEX idx_baselines_user_id ON baselines(user_id);
CREATE INDEX idx_baselines_feature_name ON baselines(feature_name);
CREATE INDEX idx_baselines_updated_at ON baselines(updated_at DESC);

-- Comments
COMMENT ON TABLE baselines IS 'User behavior baseline statistics';
COMMENT ON COLUMN baselines.feature_name IS 'Name of the behavioral feature';
COMMENT ON COLUMN baselines.mean IS 'Mean value for the feature';
```

### 3.8 System Logs Table

```sql
CREATE TABLE system_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    level VARCHAR(20) NOT NULL CHECK (level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    component VARCHAR(100),
    message TEXT NOT NULL,
    details JSONB,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_logs_level ON system_logs(level);
CREATE INDEX idx_logs_component ON system_logs(component);
CREATE INDEX idx_logs_created_at ON system_logs(created_at DESC);
CREATE INDEX idx_logs_user_id ON system_logs(user_id);

-- Comments
COMMENT ON TABLE system_logs IS 'System application logs';
COMMENT ON COLUMN system_logs.level IS 'Log level severity';
```

---

## 4. STORED PROCEDURES

### 4.1 Get User Statistics

```sql
CREATE OR REPLACE FUNCTION get_user_statistics(p_user_id UUID)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT jsonb_build_object(
        'total_alerts', (SELECT COUNT(*) FROM alerts WHERE user_id = p_user_id),
        'unread_alerts', (SELECT COUNT(*) FROM alerts WHERE user_id = p_user_id AND status = 'new'),
        'total_scans', (SELECT COUNT(*) FROM scans WHERE user_id = p_user_id),
        'total_threats', (SELECT COUNT(*) FROM threats WHERE user_id = p_user_id),
        'high_severity_alerts', (SELECT COUNT(*) FROM alerts WHERE user_id = p_user_id AND severity IN ('high', 'critical')),
        'last_scan', (SELECT created_at FROM scans WHERE user_id = p_user_id ORDER BY created_at DESC LIMIT 1)
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### 4.2 Get Security Score

```sql
CREATE OR REPLACE FUNCTION calculate_security_score(p_user_id UUID)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    alert_score DECIMAL(5,2);
    threat_score DECIMAL(5,2);
    scan_score DECIMAL(5,2);
    final_score DECIMAL(5,2);
BEGIN
    -- Calculate alert score (inverse of high severity alerts)
    SELECT COALESCE(
        100 - (COUNT(*) FILTER (WHERE severity IN ('high', 'critical'))::DECIMAL * 10),
        100
    ) INTO alert_score
    FROM alerts
    WHERE user_id = p_user_id
    AND created_at > CURRENT_TIMESTAMP - INTERVAL '30 days';
    
    -- Calculate threat score (inverse of recent threats)
    SELECT COALESCE(
        100 - (COUNT(*) FILTER (WHERE threat_score > 70)::DECIMAL * 5),
        100
    ) INTO threat_score
    FROM threats
    WHERE user_id = p_user_id
    AND created_at > CURRENT_TIMESTAMP - INTERVAL '30 days';
    
    -- Calculate scan score (based on benign scan results)
    SELECT COALESCE(
        (COUNT(*) FILTER (WHERE result = 'benign')::DECIMAL / NULLIF(COUNT(*), 0) * 100),
        100
    ) INTO scan_score
    FROM scans
    WHERE user_id = p_user_id
    AND created_at > CURRENT_TIMESTAMP - INTERVAL '30 days';
    
    -- Calculate weighted average
    final_score = (alert_score * 0.4) + (threat_score * 0.3) + (scan_score * 0.3);
    
    RETURN final_score;
END;
$$ LANGUAGE plpgsql;
```

### 4.3 Cleanup Old Data

```sql
CREATE OR REPLACE FUNCTION cleanup_old_data(days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- Delete old monitoring data
    DELETE FROM monitoring_data
    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '1 day' * days_to_keep;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Delete old behavior data
    DELETE FROM behavior_data
    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '1 day' * days_to_keep;
    
    -- Delete old system logs
    DELETE FROM system_logs
    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '1 day' * days_to_keep;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;
```

---

## 5. TRIGGERS

### 5.1 Update Timestamp Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to threats table
CREATE TRIGGER update_threats_updated_at
    BEFORE UPDATE ON threats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply to baselines table
CREATE TRIGGER update_baselines_updated_at
    BEFORE UPDATE ON baselines
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 5.2 Alert Creation Trigger

```sql
CREATE OR REPLACE FUNCTION on_alert_created()
RETURNS TRIGGER AS $$
BEGIN
    -- Send notification (would call external service)
    -- This is a placeholder for notification logic
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_alert_notification
    AFTER INSERT ON alerts
    FOR EACH ROW
    EXECUTE FUNCTION on_alert_created();
```

---

## 6. VIEWS

### 6.1 User Dashboard View

```sql
CREATE OR REPLACE VIEW user_dashboard AS
SELECT 
    u.id AS user_id,
    u.email,
    u.first_name,
    u.last_name,
    (SELECT COUNT(*) FROM alerts a WHERE a.user_id = u.id AND a.status = 'new') AS unread_alerts,
    (SELECT COUNT(*) FROM alerts a WHERE a.user_id = u.id AND a.severity IN ('high', 'critical')) AS high_severity_alerts,
    (SELECT COUNT(*) FROM threats t WHERE t.user_id = u.id AND t.status = 'detected') AS active_threats,
    (SELECT COUNT(*) FROM scans s WHERE s.user_id = u.id AND s.created_at > CURRENT_TIMESTAMP - INTERVAL '7 days') AS recent_scans,
    calculate_security_score(u.id) AS security_score,
    u.last_login
FROM users u
WHERE u.is_active = true;
```

### 6.2 Alert Summary View

```sql
CREATE OR REPLACE VIEW alert_summary AS
SELECT 
    DATE_TRUNC('day', created_at) AS date,
    type,
    severity,
    status,
    COUNT(*) AS count
FROM alerts
GROUP BY DATE_TRUNC('day', created_at), type, severity, status
ORDER BY date DESC, count DESC;
```

### 6.3 Threat Statistics View

```sql
CREATE OR REPLACE VIEW threat_statistics AS
SELECT 
    DATE_TRUNC('day', created_at) AS date,
    type,
    attack_type,
    AVG(threat_score) AS avg_score,
    COUNT(*) AS count,
    COUNT(*) FILTER (WHERE threat_score > 70) AS high_risk_count
FROM threats
GROUP BY DATE_TRUNC('day', created_at), type, attack_type
ORDER BY date DESC;
```

---

## 7. MIGRATIONS

### 7.1 Initial Migration

```python
# alembic/versions/001_initial_schema.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100)),
        sa.Column('last_name', sa.String(100)),
        sa.Column('role', sa.String(50), server_default='user'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.TIMESTAMP(timezone=True)),
        sa.CheckConstraint("role IN ('user', 'admin')", name='check_role'),
        sa.CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'", name='check_email_format'),
        sa.UniqueConstraint('email', name='uq_users_email')
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_role', 'users', ['role'])
    
    # Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text()),
        sa.Column('data', postgresql.JSONB()),
        sa.Column('status', sa.String(20), server_default='new'),
        sa.Column('acknowledged_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('dismissed_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("type IN ('phishing', 'malware', 'behavior', 'network', 'system')", name='check_alert_type'),
        sa.CheckConstraint("severity IN ('low', 'medium', 'high', 'critical')", name='check_alert_severity'),
        sa.CheckConstraint("status IN ('new', 'acknowledged', 'dismissed')", name='check_alert_status')
    )
    op.create_index('idx_alerts_user_id', 'alerts', ['user_id'])
    op.create_index('idx_alerts_type', 'alerts', ['type'])
    op.create_index('idx_alerts_severity', 'alerts', ['severity'])
    op.create_index('idx_alerts_status', 'alerts', ['status'])
    op.create_index('idx_alerts_created_at', 'alerts', ['created_at'])
    
    # Create threats table
    op.create_table(
        'threats',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('source', sa.String(255)),
        sa.Column('threat_score', sa.Numeric(5, 2)),
        sa.Column('attack_type', sa.String(100)),
        sa.Column('status', sa.String(20), server_default='detected'),
        sa.Column('details', postgresql.JSONB()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("type IN ('phishing', 'malware', 'behavior', 'network', 'ransomware')", name='check_threat_type'),
        sa.CheckConstraint("status IN ('detected', 'investigating', 'resolved', 'false_positive')", name='check_threat_status')
    )
    op.create_index('idx_threats_user_id', 'threats', ['user_id'])
    op.create_index('idx_threats_type', 'threats', ['type'])
    op.create_index('idx_threats_status', 'threats', ['status'])
    
    # Create scans table
    op.create_table(
        'scans',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('target', sa.String(2048), nullable=False),
        sa.Column('result', sa.String(20), nullable=False),
        sa.Column('score', sa.Numeric(5, 2)),
        sa.Column('details', postgresql.JSONB()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("type IN ('phishing', 'malware')", name='check_scan_type'),
        sa.CheckConstraint("result IN ('malicious', 'benign', 'suspicious', 'error')", name='check_scan_result')
    )
    op.create_index('idx_scans_user_id', 'scans', ['user_id'])
    op.create_index('idx_scans_type', 'scans', ['type'])
    op.create_index('idx_scans_result', 'scans', ['result'])
    
    # Create monitoring_data table
    op.create_table(
        'monitoring_data',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('data', postgresql.JSONB(), nullable=False),
        sa.Column('suspicious_count', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("type IN ('process', 'resource', 'network', 'file', 'browser')", name='check_monitoring_type')
    )
    op.create_index('idx_monitoring_user_id', 'monitoring_data', ['user_id'])
    op.create_index('idx_monitoring_type', 'monitoring_data', ['type'])
    
    # Create behavior_data table
    op.create_table(
        'behavior_data',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('login_hour', sa.Integer()),
        sa.Column('login_day_of_week', sa.Integer()),
        sa.Column('is_weekend', sa.Boolean(), server_default='false'),
        sa.Column('is_night', sa.Boolean(), server_default='false'),
        sa.Column('login_attempts', sa.Integer(), server_default='1'),
        sa.Column('failed_login_attempts', sa.Integer(), server_default='0'),
        sa.Column('login_location_changed', sa.Boolean(), server_default='false'),
        sa.Column('login_device_changed', sa.Boolean(), server_default='false'),
        sa.Column('login_ip_changed', sa.Boolean(), server_default='false'),
        sa.Column('file_access_count', sa.Integer(), server_default='0'),
        sa.Column('files_per_hour', sa.Numeric(10, 2)),
        sa.Column('suspicious_files_accessed', sa.Integer(), server_default='0'),
        sa.Column('suspicious_file_ratio', sa.Numeric(5, 2)),
        sa.Column('sensitive_dir_access', sa.Integer(), server_default='0'),
        sa.Column('sites_visited', sa.Integer(), server_default='0'),
        sa.Column('sites_per_hour', sa.Numeric(10, 2)),
        sa.Column('suspicious_sites_visited', sa.Integer(), server_default='0'),
        sa.Column('downloads', sa.Integer(), server_default='0'),
        sa.Column('network_activity_mb', sa.Numeric(10, 2)),
        sa.Column('network_per_hour', sa.Numeric(10, 2)),
        sa.Column('unique_endpoints', sa.Integer(), server_default='0'),
        sa.Column('suspicious_endpoints', sa.Integer(), server_default='0'),
        sa.Column('session_duration', sa.Numeric(10, 2)),
        sa.Column('is_long_session', sa.Boolean(), server_default='false'),
        sa.Column('is_short_session', sa.Boolean(), server_default='false'),
        sa.Column('is_anomalous', sa.Boolean(), server_default='false'),
        sa.Column('anomaly_score', sa.Numeric(5, 2)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_behavior_user_id', 'behavior_data', ['user_id'])
    op.create_index('idx_behavior_timestamp', 'behavior_data', ['timestamp'])
    op.create_index('idx_behavior_is_anomalous', 'behavior_data', ['is_anomalous'])
    
    # Create baselines table
    op.create_table(
        'baselines',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('feature_name', sa.String(100), nullable=False),
        sa.Column('mean', sa.Numeric(15, 4)),
        sa.Column('std', sa.Numeric(15, 4)),
        sa.Column('min_value', sa.Numeric(15, 4)),
        sa.Column('max_value', sa.Numeric(15, 4)),
        sa.Column('median', sa.Numeric(15, 4)),
        sa.Column('q25', sa.Numeric(15, 4)),
        sa.Column('q75', sa.Numeric(15, 4)),
        sa.Column('sample_count', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'feature_name', name='uq_baselines_user_feature')
    )
    op.create_index('idx_baselines_user_id', 'baselines', ['user_id'])
    op.create_index('idx_baselines_feature_name', 'baselines', ['feature_name'])
    
    # Create system_logs table
    op.create_table(
        'system_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('level', sa.String(20), nullable=False),
        sa.Column('component', sa.String(100)),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('details', postgresql.JSONB()),
        sa.Column('user_id', postgresql.UUID(as_uuid=True)),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.CheckConstraint("level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')", name='check_log_level')
    )
    op.create_index('idx_logs_level', 'system_logs', ['level'])
    op.create_index('idx_logs_component', 'system_logs', ['component'])
    op.create_index('idx_logs_created_at', 'system_logs', ['created_at'])

def downgrade():
    op.drop_table('system_logs')
    op.drop_table('baselines')
    op.drop_table('behavior_data')
    op.drop_table('monitoring_data')
    op.drop_table('scans')
    op.drop_table('threats')
    op.drop_table('alerts')
    op.drop_table('users')
```

---

## 8. SEED DATA

### 8.1 Admin User

```sql
-- Insert default admin user (password: Admin123!)
INSERT INTO users (email, password_hash, first_name, last_name, role, is_active)
VALUES (
    'admin@digitalbodyguard.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJq9qYqY2i',
    'Admin',
    'User',
    'admin',
    true
);
```

### 8.2 Sample Data

```sql
-- Insert sample alerts
INSERT INTO alerts (user_id, type, severity, title, message, status)
VALUES 
    ((SELECT id FROM users WHERE email = 'admin@digitalbodyguard.com'), 'phishing', 'high', 'Phishing URL Detected', 'Suspicious URL detected in browser history', 'new'),
    ((SELECT id FROM users WHERE email = 'admin@digitalbodyguard.com'), 'malware', 'critical', 'Malware Detected', 'Malicious file detected in Downloads folder', 'new');

-- Insert sample scans
INSERT INTO scans (user_id, type, target, result, score)
VALUES 
    ((SELECT id FROM users WHERE email = 'admin@digitalbodyguard.com'), 'phishing', 'http://example.com', 'benign', 0.15),
    ((SELECT id FROM users WHERE email = 'admin@digitalbodyguard.com'), 'malware', 'suspicious.exe', 'malicious', 0.92);
```

---

## 9. BACKUP AND RESTORE

### 9.1 Backup Script

```bash
#!/bin/bash
# backup_database.sh

DB_NAME="digital_bodyguard"
DB_USER="postgres"
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Perform backup
pg_dump -U $DB_USER -d $DB_NAME > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

echo "Backup completed: ${BACKUP_FILE}.gz"
```

### 9.2 Restore Script

```bash
#!/bin/bash
# restore_database.sh

DB_NAME="digital_bodyguard"
DB_USER="postgres"
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Decompress if needed
if [[ $BACKUP_FILE == *.gz ]]; then
    gunzip -c $BACKUP_FILE | psql -U $DB_USER -d $DB_NAME
else
    psql -U $DB_USER -d $DB_NAME < $BACKUP_FILE
fi

echo "Restore completed"
```

---

## 10. PERFORMANCE OPTIMIZATION

### 10.1 Connection Pooling

```python
# database.py with connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

### 10.2 Index Optimization

```sql
-- Composite indexes for common queries
CREATE INDEX idx_alerts_user_status_created ON alerts(user_id, status, created_at DESC);
CREATE INDEX idx_threats_user_status_score ON threats(user_id, status, threat_score DESC);
CREATE INDEX idx_scans_user_type_created ON scans(user_id, type, created_at DESC);

-- Partial indexes for filtered queries
CREATE INDEX idx_alerts_high_severity ON alerts(user_id, created_at DESC) 
WHERE severity IN ('high', 'critical');

CREATE INDEX idx_behavior_anomalous ON behavior_data(user_id, timestamp DESC) 
WHERE is_anomalous = true;
```

### 10.3 Partitioning Strategy

```sql
-- Partition monitoring_data by month
CREATE TABLE monitoring_data (
    id UUID DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    suspicious_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE monitoring_data_y2026m07 PARTITION OF monitoring_data
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

CREATE TABLE monitoring_data_y2026m08 PARTITION OF monitoring_data
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');

-- Create future partitions
CREATE TABLE monitoring_data_y2026m09 PARTITION OF monitoring_data
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
```

---

## 11. SECURITY CONSIDERATIONS

### 11.1 Row Level Security

```sql
-- Enable row level security
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- Create policy for users to see only their own alerts
CREATE POLICY user_alerts_policy ON alerts
    FOR SELECT
    USING (user_id = current_setting('app.current_user_id')::UUID);

-- Create policy for admins to see all alerts
CREATE POLICY admin_alerts_policy ON alerts
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = current_setting('app.current_user_id')::UUID 
            AND role = 'admin'
        )
    );
```

### 11.2 Data Encryption

```sql
-- Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Function to encrypt sensitive data
CREATE OR REPLACE FUNCTION encrypt_data(data TEXT, key TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN encode(encrypt(data::bytea, key::bytea, 'aes'), 'base64');
END;
$$ LANGUAGE plpgsql;

-- Function to decrypt sensitive data
CREATE OR REPLACE FUNCTION decrypt_data(encrypted_data TEXT, key TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN convert_from(decrypt(decode(encrypted_data, 'base64'), key::bytea, 'aes'), 'SQL_ASCII');
END;
$$ LANGUAGE plpgsql;
```

---

## 12. CONCLUSION

This document provides complete database design for the AI-Powered Digital Bodyguard system including:

- **8 Tables**: users, alerts, threats, scans, monitoring_data, behavior_data, baselines, system_logs
- **ER Diagram**: Complete entity relationships
- **Stored Procedures**: User statistics, security score calculation, data cleanup
- **Triggers**: Auto-update timestamps, alert notifications
- **Views**: Dashboard, alert summary, threat statistics
- **Migrations**: Alembic migration scripts
- **Performance**: Connection pooling, indexing, partitioning
- **Security**: Row level security, data encryption
- **Backup**: Backup and restore scripts

**Next Steps:**
1. Set up PostgreSQL database
2. Run initial migration
3. Configure connection pooling
4. Set up automated backups
5. Implement row level security
6. Monitor database performance

---

## APPENDICES

### Appendix A: Database Connection String

```
# Production
postgresql://user:password@localhost:5432/digital_bodyguard

# Development
postgresql://user:password@localhost:5432/digital_bodyguard_dev

# Testing
postgresql://user:password@localhost:5432/digital_bodyguard_test
```

### Appendix B: Useful SQL Queries

```sql
-- Get top 10 users by threat count
SELECT u.email, COUNT(t.id) as threat_count
FROM users u
LEFT JOIN threats t ON u.id = t.user_id
GROUP BY u.id, u.email
ORDER BY threat_count DESC
LIMIT 10;

-- Get alerts by severity distribution
SELECT severity, COUNT(*) as count
FROM alerts
GROUP BY severity
ORDER BY 
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END;

-- Get recent monitoring activity
SELECT user_id, type, suspicious_count, created_at
FROM monitoring_data
WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '1 hour'
ORDER BY created_at DESC;
```

### Appendix C: Database Maintenance

```sql
-- Vacuum and analyze tables
VACUUM ANALYZE users;
VACUUM ANALYZE alerts;
VACUUM ANALYZE threats;
VACUUM ANALYZE scans;
VACUUM ANALYZE monitoring_data;
VACUUM ANALYZE behavior_data;

-- Reindex tables
REINDEX TABLE users;
REINDEX TABLE alerts;
REINDEX TABLE threats;
```
