import apiClient from "../config/api";

export async function uploadImage(file: File, provider: string) {
  const formData = new FormData();
  formData.append("image_file", file);
  formData.append("provider", provider);

  const token = localStorage.getItem("token");
  const response = await apiClient.post("/api-v1/scan-image/", formData, {
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });

  return response.data;
}