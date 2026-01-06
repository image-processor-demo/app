const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:3000";

export async function processImage(file) {
    const formData = new FormData();
    formData.append("image", file);
    const response = await fetch(`${API_BASE_URL}/api/process`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Image processing failed" + ` (status: ${response.status})` + "API_BASE_URL: " + API_BASE_URL);
    }

    // Check if response is base64-encoded text instead of binary
    const text = await response.text();

    // If it starts with base64 JPEG signature, decode it
    if (text.startsWith('/9j/')) {
        // Convert base64 to binary
        const binaryString = atob(text);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        return new Blob([bytes], { type: 'image/jpeg' });
    }

    // Otherwise, treat as blob (shouldn't happen, but fallback)
    return new Blob([text], { type: 'image/jpeg' });
}
