import {Navigate} from "react-router-dom"

export default function AdminProtectedRoute({children}: {children: React.ReactNode}){
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if(!token || token === "null" || token === "undefined") {
        return <Navigate to="/login"/>
    }

    if(role !== "admin") {
        return <Navigate to="/dashboard"/>
    }

    return children
}