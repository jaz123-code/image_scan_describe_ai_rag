import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { uploadImage } from "../api/apiClient"
import '../App.css'

interface Props{
    onScanStarted: (scanId: string)=>void
}
export default function ImageUploader({ onScanStarted }: Props) {
    const [file, setFile] = useState<File | null>(null)
    const [provider, setProvider] = useState("local")
    const [error, setError] = useState<string | null>(null)
    const navigate = useNavigate()

    const handleUpload = async () => {
        if (!file) return
        setError(null)
        try {
            const result = await uploadImage(file, provider)
            onScanStarted(result.scan_id)
        } catch (err: unknown) {
            const status = err && typeof err === "object" && "response" in err
                ? (err as { response?: { status?: number } }).response?.status
                : null
            if (status === 401) {
                localStorage.removeItem("token")
                navigate("/login", { replace: true })
                return
            }
            setError(err instanceof Error ? err.message : "Upload failed. Please try again.")
        }
    }
    return (
        <div>
            <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
            <input type="text" value={provider} onChange={(e) => setProvider(e.target.value)} />
            <button onClick={handleUpload}>Upload & Scan</button>
            {error && <p className="error">{error}</p>}
        </div>
    )
    
}