from fastapi import FastAPI,Response
app = FastAPI()

# ============================================================================
# 200 status code endpoints
# ============================================================================

@app.get("/")
async def root():
    return Response(status_code=200)

@app.post("/200-only-post-method")
async def create_item():
    return Response(status_code=201)

@app.get("/200-only-get-method/{id}")
async def read_item(id: int):
    return Response(status_code=200)

@app.put("/200-only-put-method/{id}")
async def update_item(id: int):
    return Response(status_code=200)

@app.delete("/200-only-delete-method/{id}")
async def delete_item(id: int):
    return Response(status_code=204)