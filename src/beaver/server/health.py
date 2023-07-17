from beaver import app


@app.get("/health", tags=["monitoring"])
async def health():
    return {"status": "ok"}
