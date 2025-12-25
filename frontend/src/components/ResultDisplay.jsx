import { useEffect, useState } from "react";

export default function ResultDisplay() {
    const [imageUrl, setImageUrl] = useState(null);

    useEffect(() => {
        function handler(event) {
            setImageUrl(event.detail);
        }

        window.addEventListener("imageProcessed", handler);
        return () => window.removeEventListener("imageProcessed", handler);
    }, []);

    return (
        <section style={{ flex: 1 }}>
            <h2>Result</h2>

            {imageUrl ? (
                <img
                    src={imageUrl}
                    alt="Processed"
                    style={{ maxWidth: "100%", borderRadius: "8px" }}
                />
            ) : (
                <p>No image processed yet.</p>
            )}
        </section>
    );
}
