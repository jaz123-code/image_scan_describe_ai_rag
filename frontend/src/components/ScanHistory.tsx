import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import apiClient from "../config/api"

interface Scan {
  image_id: string;
  filename: string;
  status: string;
}

export default function ScanHistory() {

  const [scans, setScans] = useState<Scan[]>([])

  useEffect(() => {
    apiClient.get("/api-v1/scans")
      .then(res => setScans(res.data.scans))
      .catch(err => console.error("Failed to fetch scans:", err))
  }, [])

  return (
    <div>
      <h2>Scan History</h2>

      {scans.map((scan) => (
        <div key={scan.image_id}>
          <b>{scan.filename}</b>
          <p>Status: {scan.status}</p>
          <Link to={`/scan/${encodeURIComponent(scan.image_id)}`}>View details</Link>
        </div>
      ))}
      {scans.length === 0 && <p>No scans found.</p>}
    </div>
  )
}