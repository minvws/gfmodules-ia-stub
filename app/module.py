from fastapi import FastAPI, APIRouter

def init_custom_module(app: FastAPI) -> None:

  router = APIRouter()

  @router.get("/hellomax")
  def hello_module():
    return {"message": "Hello max-core!"}

  app.include_router(router)