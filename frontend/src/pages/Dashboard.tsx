import { useState } from "react";
import ImageUploader from "../components/ImageUploader";
import ScanStatus from "../components/scanStatus";
import '../App.css'

export default function Dashboard() {
    const [scanId, setScanId] = useState<string | null>(null);

    return (
        <div className="container">
            <h1>AI Image Scanner</h1>
            <ImageUploader onScanStarted={setScanId} />
            {scanId && <ScanStatus scanId={scanId} />}
        </div>
    );
}
