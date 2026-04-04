import {useEffect, useState } from "react";
import apiClient  from "../config/api";

interface Alert {
    id: string;
    message: string;
    severity: string;
}

export default function AlertsPanel(){
    const [alerts, setAlerts]=useState<Alert[]>([])

    useEffect(()=>{
        apiClient.get("/api-v1/alerts")
         .then(res=> setAlerts(res.data.alerts))

    },[])
    return (
        <div>
            <h2>System Alerts</h2>

            {alerts.map((alert) => (
                <div key={alert.id} style={{ border: "1px solid #ccc", margin: "8px 0", padding: "8px" }}>
                    <p><strong>[{alert.severity}]</strong> {alert.message}</p>
                </div>
            ))}
            
            {alerts.length === 0 && <p>No active alerts.</p>}
        </div>
    )
}