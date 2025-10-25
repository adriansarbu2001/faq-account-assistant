from fastapi import FastAPI

app = FastAPI(title="FAQ Account Assistant", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check."""
    return {"status": "ok"}
