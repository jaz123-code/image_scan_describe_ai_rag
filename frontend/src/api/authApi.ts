import apiClient from "../config/api";

export async function login(email: string, password: string){
    const res=await apiClient.post("/auth/login", {email, password})
    return res.data;
}

export async function register(email: string, password: string){
    const res=await apiClient.post("/auth/signup", {email, password})
    return res.data;
}