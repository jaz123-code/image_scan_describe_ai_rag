import { useEffect, useMemo, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import apiClient from "../config/api"

type ScanDetailsResponse = {
  image_id: string
  user_id: string
  data: unknown
}

export default function ScanDetail() {
  const { image_id } = useParams<{ image_id: string }>()
  const navigate = useNavigate()

  const [manualId, setManualId] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [details, setDetails] = useState<ScanDetailsResponse | null>(null)
  const [decisionLoading, setDecisionLoading] = useState<"approve" | "reject" | null>(null)

  const resolvedId = useMemo(() => image_id ?? null, [image_id])

  useEffect(() => {
    if (!resolvedId) {
      setDetails(null)
      return
    }

    setLoading(true)
    setError(null)

    apiClient
      .get<ScanDetailsResponse>(`/api-v1/scan-details/${encodeURIComponent(resolvedId)}`)
      .then((res) => setDetails(res.data))
      .catch((err: unknown) => {
        const status =
          err && typeof err === "object" && "response" in err
            ? (err as { response?: { status?: number } }).response?.status
            : null
        if (status === 401) {
          localStorage.removeItem("token")
          navigate("/login", { replace: true })
          return
        }
        setError(err instanceof Error ? err.message : "Failed to fetch scan details.")
      })
      .finally(() => setLoading(false))
  }, [navigate, resolvedId])

  const status =
    details && details.data && typeof details.data === "object" && "status" in details.data
      ? String((details.data as { status?: unknown }).status ?? "")
      : ""

  async function submitHumanDecision(approve: boolean) {
    if (!resolvedId) return
    setError(null)
    setDecisionLoading(approve ? "approve" : "reject")
    try {
      const form = new FormData()
      form.append("scan_id", resolvedId)
      form.append("approve", String(approve))

      await apiClient.post("/api-v1/human-approval/", form)
      const refreshed = await apiClient.get<ScanDetailsResponse>(
        `/api-v1/scan-details/${encodeURIComponent(resolvedId)}`
      )
      setDetails(refreshed.data)
    } catch (err: unknown) {
      const status =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { status?: number } }).response?.status
          : null
      if (status === 401) {
        localStorage.removeItem("token")
        navigate("/login", { replace: true })
        return
      }
      setError(err instanceof Error ? err.message : "Failed to submit human decision.")
    } finally {
      setDecisionLoading(null)
    }
  }

  return (
    <div style={{ maxWidth: 900 }}>
      <h2 style={{ marginTop: 0 }}>Scan Details</h2>

      {!resolvedId && (
        <div style={{ display: "grid", gap: 8, maxWidth: 520 }}>
          <p style={{ margin: 0, color: "#374151" }}>
            Enter a scan id to view details.
          </p>
          <input
            value={manualId}
            onChange={(e) => setManualId(e.target.value)}
            placeholder="e.g. 25f0b978-..."
          />
          <button
            onClick={() => {
              const id = manualId.trim()
              if (!id) return
              navigate(`/scan/${encodeURIComponent(id)}`)
            }}
          >
            View details
          </button>
        </div>
      )}

      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {details && (
        <div style={{ display: "grid", gap: 8 }}>
          <div>
            <b>Image ID:</b> {details.image_id}
          </div>
          <div>
            <b>User ID:</b> {details.user_id}
          </div>
          <div>
            <b>Data:</b>
            <pre style={{ overflow: "auto", padding: 12, background: "#0b1020", color: "#e5e7eb" }}>
              {JSON.stringify(details.data, null, 2)}
            </pre>
          </div>

          {status === "PENDING_REVIEW" && (
            <div style={{ display: "flex", gap: 8, alignItems: "center", marginTop: 8 }}>
              <button
                onClick={() => submitHumanDecision(true)}
                disabled={decisionLoading !== null}
              >
                {decisionLoading === "approve" ? "Approving…" : "Approve"}
              </button>
              <button
                onClick={() => submitHumanDecision(false)}
                disabled={decisionLoading !== null}
              >
                {decisionLoading === "reject" ? "Rejecting…" : "Reject"}
              </button>
              <span style={{ color: "#6b7280", fontSize: 12 }}>
                Current status: <b>{status}</b>
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}