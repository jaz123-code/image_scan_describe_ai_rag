import { useEffect, useState } from "react"
import apiClient from "../config/api"
import AlertsPanel from "../components/AlertsPanel";

interface AdminStats {
  total_scans: number;
  auto_approved: number;
  pending_review: number;
  avg_confidence: number;
}

export default function AdminDashboard() {

  const [data, setData] = useState<AdminStats | null>(null)

  useEffect(() => {
    apiClient.get("/api-v1/admin/dashboard")
      .then(res => setData(res.data))
      .catch(err => console.error("Failed to fetch admin stats:", err))
  }, [])

  if (!data) return <div>Loading dashboard...</div>

  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin Dashboard</h1>

      <div>
        <h3>Total Scans</h3>
        <p>{data.total_scans}</p>
      </div>

      <div>
        <h3>Auto Approved</h3>
        <p>{data.auto_approved}</p>
      </div>

      <div>
        <h3>Pending Review</h3>
        <p>{data.pending_review}</p>
      </div>

      <div>
        <h3>Average Confidence</h3>
        <p>{data.avg_confidence}</p>
      </div>

      <AlertsPanel />
    </div>
  )
}