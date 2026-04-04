import { useEffect, useState } from "react"
import '../App.css'

interface Props {
  scanId: string
}

export default function ScanStatus({ scanId }: Props) {
  const [status, setStatus] = useState("processing")
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const token = localStorage.getItem("token");
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://localhost:8000/ws/scan/${scanId}?token=${token}`);

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setStatus(data.stage || "processing");
        setProgress(data.progress || 0);
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => socket.close()
  }, [scanId])

  return (
    <div className="status-box">
      <h3>Status: {status}</h3>
      <div className="progress-bar">
        <div style={{ width: `${progress}%` }} className="progress-fill" />
      </div>
    </div>
  )
}