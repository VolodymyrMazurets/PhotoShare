from fastapi import FastAPI
import uvicorn
from api.routes import auth
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8000"
]

app = FastAPI()
app.include_router(auth.router, prefix='/api')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
