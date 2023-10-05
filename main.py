from fastapi import APIRouter, FastAPI
from pydantic import BaseModel


class Expr:
    def evaluate(self, values):
        raise NotImplementedError("Please Implement this method")


class Param(Expr):
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, values: dict[str, float]):
        return values[self.name]


class Value(Expr):
    def __init__(self, val: float):
        self.val = val

    def evaluate(self, values: dict[str, float]):
        return self.val


class MyMath:
    def __init__(self):
        self.myRouter = APIRouter()
        self.setup_routes()
        self.expressions = []

    def setup_routes(self):
        @self.myRouter.get("/")
        async def root():
            return {"message": "Hello World"}

        @self.myRouter.get("/items/{item_id}")
        async def read_item(item_id: int, q: str = None):
            return {"item_id": item_id, "q": q}

        @self.myRouter.get("/params")
        async def params():
            return list(map(lambda x: x.name, filter(lambda x: isinstance(x, Param), self.expressions)))

        @self.myRouter.post("/add_val_{e}")
        async def add_val(e):
            self.expressions.append(Value(e))

        @self.myRouter.post("/add_par_{e}")
        async def add_par(e):
            self.expressions.append(Param(e))

        @self.myRouter.post("/eval")
        async def evaluate(d: dict[str, float]):
            return sum(map(lambda x: x.evaluate(d), self.expressions))


app = FastAPI()
app.include_router(MyMath().myRouter)
