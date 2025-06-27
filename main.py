from fastapi import FastAPI, Request, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx

import os # Added import for os module

app = FastAPI()

# Serve static files (for favicon)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
async def root():
    return {"message": "Welcome to the Manyara Backend! Visit /docs for API documentation."}


# GET endpoint: fetches from a public sample JSON endpoint
@app.get("/posts")
async def get_posts():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts")
        return response.json()

# POST endpoint: create a new item
@app.post("/items")
async def create_item(item: dict):
    return {"message": "Item created", "item": item}

# PUT endpoint: update an item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: dict):
    return {"message": f"Item {item_id} updated", "item": item}

# PATCH endpoint: partially update an item
@app.patch("/items/{item_id}")
async def patch_item(item_id: int, item: dict):
    return {"message": f"Item {item_id} patched", "item": item}

# DELETE endpoint: delete an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}

# OPTIONS endpoint: return allowed methods
@app.options("/items")
async def options_items():
    return Response(headers={"Allow": "GET,POST,PUT,PATCH,DELETE,OPTIONS,HEAD"})

# HEAD endpoint: return headers only
@app.head("/items")
async def head_items():
    return Response(status_code=status.HTTP_200_OK)




@app.get("/favicon.ico")
async def favicon(): # Updated path to favicon.ico
    return FileResponse(os.path.join("assets", "favicon.ico"))

# MISCELLANEOUS ENDPOINTS
# HEAD endpoint for root
@app.head("/")
async def head_root():
    return Response(status_code=status.HTTP_200_OK)

@app.head("/health")
async def head_health():
    return Response(status_code=status.HTTP_200_OK)

# Health check endpoint for Render
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}
