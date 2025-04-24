from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory data store
data_store: Dict[int, str] = {}

# Request model
class Item(BaseModel):
    id: int
    value: str

@app.get("/items")
def get_items():
    return data_store

@app.post("/items")
def create_item(item: Item):
    if item.id in data_store:
        raise HTTPException(status_code=400, detail="Item already exists.")
    data_store[item.id] = item.value
    return {"message": "Item created", "item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id != item.id:
        raise HTTPException(status_code=400, detail="ID mismatch.")
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found.")
    data_store[item_id] = item.value
    return {"message": "Item updated", "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found.")
    del data_store[item_id]
    return {"message": "Item deleted"}
