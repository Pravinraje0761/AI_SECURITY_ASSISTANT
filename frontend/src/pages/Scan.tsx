import React, { useState } from 'react'
import axios from 'axios'

const Scan: React.FC = () => {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleScan = async () => {
    if (!url) {
      setError('Please enter a URL')
      return
    }
    setError('')
    setLoading(true)
    setResult(null)

    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        '/api/v1/scan/url',
        { type: 'phishing', target: url },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Scan failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>URL Scanner</h1>
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Enter URL to scan:</label>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          style={{ width: '100%', maxWidth: '500px', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}
        />
        <button
          onClick={handleScan}
          disabled={loading}
          style={{ marginTop: '10px', padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: loading ? 'not-allowed' : 'pointer' }}
        >
          {loading ? 'Scanning...' : 'Scan'}
        </button>
      </div>
      {error && <div style={{ color: 'red', marginBottom: '20px' }}>{error}</div>}
      {result && (
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', maxWidth: '500px' }}>
          <h3>Scan Result</h3>
          <p><strong>Result:</strong> <span style={{ color: result.result === 'benign' ? 'green' : 'red' }}>{result.result.toUpperCase()}</span></p>
          <p><strong>Score:</strong> {(result.score * 100).toFixed(2)}%</p>
          <p><strong>URL:</strong> {result.target}</p>
          {result.details?.indicators && result.details.indicators.length > 0 && (
            <div>
              <p><strong>Indicators:</strong></p>
              <ul>
                {result.details.indicators.map((indicator: string, index: number) => (
                  <li key={index}>{indicator}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Scan
