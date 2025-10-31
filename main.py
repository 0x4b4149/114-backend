from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 假資料放最上面供使用
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# Pydantic Model
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# 根目錄
@app.get("/")
async def root():
    return {"message": "Hello world"}

# 根據 item_id 取得項目
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 支援跳過與限制筆數的查詢參數
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# 建立新的項目
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()#dict() 將.jason存成py好處理的格式
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax":price_with_tax})
    return item_dict  # 回傳接收到的 item 資料

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q : str | None = None):
    result = {"item_id":item_id, **item.model_dump()}
    if q:
        result.update({"q":q})
    return {"item_id":item_id, **item.model_dump()}