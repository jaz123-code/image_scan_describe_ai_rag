import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/LoginPage";
import SignupPage from "./pages/signUppage";
import ProtectedRoute from "./components/protectedRoute";
import ScanHistory from "./components/ScanHistory";
import ScanDetail from "./components/ScanDetail";
import ProtectedLayout from "./components/ProtectedLayout";
import AdminDashboard from "./pages/AdminDashboard";
import AdminProtectedRoute from "./components/AdminProtectedRoute";
import TrainModel from "./components/TrainModel";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route
          element={
            <ProtectedRoute>
              <ProtectedLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/history" element={<ScanHistory />} />
          <Route path="/scan" element={<ScanDetail />} />
          <Route path="/scan/:image_id" element={<ScanDetail />} />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Route>
        <Route element={
          <AdminProtectedRoute>
            <ProtectedLayout />
          </AdminProtectedRoute>
        }>
          <Route path="/train" element={<TrainModel />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}
export default App;
