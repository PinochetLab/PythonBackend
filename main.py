from fastapi import APIRouter, FastAPI
from pydantic import BaseModel


class d(BaseModel):
    def __init__(self, m: dict[str, float], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m = m;

class Expr:
    def evaluate(self, values):
        raise NotImplementedError("Please Implement this method")


class Param(Expr):
    def __init__(self, name):
        self.name = name

    def evaluate(self, values):
        return values[self.name]


class Value(Expr):
    def __init__(self, val):
        self.val = val

    def evaluate(self, values):
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
            return map(lambda x: Param(x).name, filter(lambda x: isinstance(x, Param), self.expressions))

        @self.myRouter.post("/add_val_{e}")
        async def add_val(e):
            self.expressions.append(Value(e))

        @self.myRouter.post("/add_par_{e}")
        async def add_val(e):
            self.expressions.append(Param(e))

        @self.myRouter.post("/eval")
        async def evaluate(m: d):
            return sum(map(lambda x: x.evaluate(m), self.expressions))


app = FastAPI()
app.include_router(MyMath().myRouter)
