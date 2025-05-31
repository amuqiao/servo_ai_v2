from fastapi import FastAPI

app = FastAPI(title="My FastAPI Service")


@app.get("/")
async def root():
    return "Hello world"


@app.get("/hello")
async def root():
    return "Hello luffy"


def hello():
    print("Hello world")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import os
    import sys
    import uvicorn

    print(f"当前工作目录: {os.getcwd()}")
    print("Python路径列表:")
    for path in sys.path:
        print(f"- {path}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
