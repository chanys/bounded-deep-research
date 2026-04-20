from fastapi import FastAPI

app = FastAPI(title="bounded-deep-research")  # creates app instance

@app.get("/health")  # registers function below as HTTP handler: GET request to /health
def health():
    return {"status": "ok"}