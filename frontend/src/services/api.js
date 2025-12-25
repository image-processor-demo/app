const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function processImage(file) {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch(`${API_BASE_URL}/process`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Image processing failed");
    }

    return response.blob();
}
