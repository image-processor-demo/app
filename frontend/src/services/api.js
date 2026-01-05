const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:3000";

export async function processImage(file) {
    const formData = new FormData();
    formData.append("image", file);
    const response = await fetch(`${API_BASE_URL}/process`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Image processing failed" + ` (status: ${response.status})` + "API_BASE_URL: " + API_BASE_URL);

    }

    const blob = await response.blob();
    return new Blob([blob], { type: "image/jpeg" }); // <-- wrap here
}
