from typing import Annotated, Union
from fastapi import Body, FastAPI, Form, Path, Cookie
from pydantic import BaseModel, Field

app = FastAPI()

# 假資料放最上面供使用
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

@app.post("/login")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    return {"username": username}


# Pydantic Model
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default = None, title = "The description of the value", max_length=300
    )
    price: float = Field(gt=0, description = "The price must be greater then zero")
    tax: Union[float , None] = None
    tags: list[str] = []

# 根目錄
@app.get("/")
async def root():
    return {"message": "Hello world"}

# 根據 item_id 取得項目
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

'''
# 支援跳過與限制筆數的查詢參數
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
'''

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()]):
    return {"ads_id": ads_id}

'''
# 建立新的項目
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()#dict() 將.jason存成py好處理的格式
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax":price_with_tax})
    return item_dict  # 回傳接收到的 item 資料
'''

@app.post("/items/")
async def create_item(item:Item) -> list[Item]:
    return item

'''
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    item: Item | None = None,
    q : str | None = None,
):
    results = {"item_id":item_id}
    if q:
        results.update({"q":q})
    if item:
        results.update({"item":item})
    return results
'''

@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item" : item}
    return results