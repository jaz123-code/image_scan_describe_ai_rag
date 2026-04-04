import { useState } from "react"

export default function TrainModel() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleTrain = async () => {
    setLoading(true)

    const token = localStorage.getItem("token")

    const res = await fetch("http://localhost:8000/api/admin/train-model/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await res.json()
    setResult(data)
    setLoading(false)
  }

  return (
    <div className="train-box">
      <h2>Model Training</h2>

      <button onClick={handleTrain} disabled={loading}>
        {loading ? "Training..." : "Train Model"}
      </button>

      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  )
}