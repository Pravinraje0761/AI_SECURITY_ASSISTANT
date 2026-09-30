import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

interface DashboardProps {
  onLogout: () => void
}

const Dashboard: React.FC<DashboardProps> = ({ onLogout }) => {
  const [history, setHistory] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.get('/api/v1/scan/history', { headers: { Authorization: `Bearer ${token}` } })
        .then(res => setHistory(res.data))
        .catch(() => {})
    }
  }, [])

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>AI Digital Bodyguard Dashboard</h1>
        <button onClick={onLogout}
          style={{ padding: '8px 16px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Logout
        </button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>Security Score</h3>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#28a745' }}>85</div>
          <p>Your system is secure</p>
        </div>
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>Recent Alerts</h3>
          <p>No recent alerts</p>
        </div>
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>Quick Actions</h3>
          <button style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            onClick={() => navigate('/scan')}>Scan URL</button>
        </div>
      </div>
      <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
        <h3>Scan History</h3>
        {history.length === 0 ? (
          <p>No scans yet. Go to <a href="/scan">Scan URL</a> to get started.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                <th style={{ padding: '8px' }}>Target</th>
                <th style={{ padding: '8px' }}>Result</th>
                <th style={{ padding: '8px' }}>Score</th>
                <th style={{ padding: '8px' }}>Date</th>
              </tr>
            </thead>
            <tbody>
              {history.map((scan) => (
                <tr key={scan.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '8px' }}>{scan.target}</td>
                  <td style={{ padding: '8px', color: scan.result === 'benign' ? 'green' : 'red', fontWeight: 'bold' }}>
                    {scan.result.toUpperCase()}
                  </td>
                  <td style={{ padding: '8px' }}>{(scan.score * 100).toFixed(1)}%</td>
                  <td style={{ padding: '8px' }}>{new Date(scan.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default Dashboard
