import { useState } from "react";
import { processImage } from "../services/api";

export default function ImageUploader() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleProcess() {
        if (!file) return;

        setLoading(true);
        setError("");

        try {
            const result = await processImage(file);
            const url = URL.createObjectURL(result);
            window.dispatchEvent(
                new CustomEvent("imageProcessed", { detail: url })
            );
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <section style={{ flex: 1 }}>
            <h2>Upload Image</h2>

            <input
                type="file"
                accept="image/*"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <div style={{ marginTop: "1rem" }}>
                <button onClick={handleProcess} disabled={loading}>
                    {loading ? "Processing..." : "Process Image"}
                </button>
            </div>

            {error && <p style={{ color: "tomato" }}>{error}</p>}
        </section>
    );
}
