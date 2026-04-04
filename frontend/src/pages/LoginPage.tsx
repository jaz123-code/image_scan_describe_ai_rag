import {useState} from "react"
import {login} from "../api/authApi"


export default function Login(){
    const [email, setEmail]=useState("")
    const[password, setPassword]=useState("")
    
    const handleLogin=async()=>{
        try {
            const data = await login(email, password)
            localStorage.setItem("token", data.token)
            window.location.href="/dashboard"
        } catch (error) {
            alert("Login failed. Please check your credentials.");
            console.error("Login failed:", error);
        }
    }

    return (
        <div className="login-box">
            <h2>Login</h2>
            <input placeholder="email" onChange={(e)=>setEmail(e.target.value)}/>
            <input placeholder="password" type="password" onChange={(e)=>setPassword(e.target.value)}/>
            <button onClick={handleLogin}>Login</button>
            <p>Dont have an account? <a href="/signup">Sign up</a></p>
        </div>
    )
}
