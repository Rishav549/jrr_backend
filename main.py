from fastapi import FastAPI
from routes.product import router as product_router
from routes.contact import router as contact_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(product_router)
app.include_router(contact_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="127.0.0.1")