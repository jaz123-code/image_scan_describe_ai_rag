import {useState} from "react";
import {register} from  "../api/authApi";

export default function SignupPage(){
    const[email, setEmail]=useState("")
    const[password, setPassword]=useState("")

    const handleSignup=async()=>{
        try{
            await register(email, password)
            alert("Account created successfully")
            window.location.href="/login"
                }catch{
            alert('Sign up  Failed')
        }
        }
    
    return (
        <div className="login-box">
            <h2>Sign Up</h2>
            <input placeholder="email" onChange={(e)=> setEmail(e.target.value)}/>
            <input placeholder="password" type="password" onChange={(e)=> setPassword(e.target.value)}/>
            <button onClick={handleSignup}>Sign up</button>

        </div>
    )
    }

