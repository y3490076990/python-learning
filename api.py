from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

db = {}

@app.get("/items")
def list_items():
    return list(db.values())

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in db:
        return {"error": "not found"}
    return db[item_id]

@app.post("/items")
def create_item(item: Item):
    db[len(db) + 1] = item.model_dump()
    return {"id": len(db), "item": item.model_dump()}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in db:
        return {"error": "not found"}
    del db[item_id]
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
