import { NavLink, Outlet, useNavigate } from "react-router-dom"
import { useState } from "react"

function linkClassName({ isActive }: { isActive: boolean }) {
  return `nav-link${isActive ? " active" : ""}`
}

export default function ProtectedLayout({ children }: { children?: React.ReactNode }) {
  const [scanId, setScanId] = useState("")
  const navigate = useNavigate()
  const role = localStorage.getItem("role")

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside
        style={{
          width: 240,
          padding: 16,
          borderRight: "1px solid #e5e7eb",
          background: "#fafafa",
        }}
      >
        <h3 style={{ marginTop: 0 }}>Options</h3>

        <nav style={{ display: "grid", gap: 8, marginBottom: 16 }}>
          <NavLink to="/dashboard" className={linkClassName}>
            Dashboard
          </NavLink>
          <NavLink to="/history" className={linkClassName}>
            Scan History
          </NavLink>
          <NavLink to="/scan" className={linkClassName}>
            Scan Details
          </NavLink>
          {role === null &&(
            <NavLink to="/admin" className={linkClassName}>
              Admin
            </NavLink>
          )}
        </nav>

        <div style={{ display: "grid", gap: 8 }}>
          <label style={{ fontSize: 12, color: "#374151" }}>Jump to scan id</label>
          <input
            value={scanId}
            onChange={(e) => setScanId(e.target.value)}
            placeholder="e.g. 25f0b978-..."
          />
          <button
            onClick={() => {
              if (!scanId.trim()) return
              navigate(`/scan/${encodeURIComponent(scanId.trim())}`)
            }}
          >
            View
          </button>
        </div>
      </aside>

      <main style={{ flex: 1, padding: 16 }}>
        {children || <Outlet />}
      </main>
    </div>
  )
}
