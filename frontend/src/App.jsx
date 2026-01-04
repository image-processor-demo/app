import Header from "./components/Header";
import ImageUploader from "./components/ImageUploader";
import ResultDisplay from "./components/ResultDisplay";
// Main application component
export default function App() {
  return (
    <>
      <Header />
      <main style={{ display: "flex", gap: "2rem", padding: "2rem" }}>
        <ImageUploader />
        <ResultDisplay />
      </main>
    </>
  );
}
