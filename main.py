from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def index():
    return {"hai":{'hai':"fawaz"}}