from fastapi import FASTAPI

app = fastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}