import { useState } from "react";
import { processImage } from "../services/api";

export default function ImageUploader() {
    const [file, setFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    function handleFileChange(e) {
        const selected = e.target.files[0];
        setFile(selected);
        if (selected) {
            setPreviewUrl(URL.createObjectURL(selected)); // <-- preview URL
        } else {
            setPreviewUrl(null);
        }
    }

    async function handleProcess() {
        if (!file) return;

        setLoading(true);
        setError("");

        try {
            const result = await processImage(file);
            const url = URL.createObjectURL(result);
            window.dispatchEvent(new CustomEvent("imageProcessed", { detail: url }));
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <section style={{ flex: 1 }}>
            <h2>Upload Image</h2>

            <input type="file" accept="image/*" onChange={handleFileChange} />

            {previewUrl && (
                <div style={{ marginTop: "1rem" }}>
                    <img
                        src={previewUrl}
                        alt="Uploaded preview"
                        style={{ maxWidth: "100%", borderRadius: "8px" }}
                    />
                </div>
            )}

            <div style={{ marginTop: "1rem" }}>
                <button onClick={handleProcess} disabled={loading}>
                    {loading ? "Processing..." : "Process Image"}
                </button>
            </div>

            {error && <p style={{ color: "tomato" }}>{error}</p>}
        </section>
    );
}
