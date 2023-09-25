"""This module for FastAPI."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root1():
    """Default GET request."""
    return {"message": "Hello World"}


@app.get("/123")
async def root2():
    """GET request returning [1, 2, 3]."""
    return [1, 2, 3]


@app.get("/123concat{s}")
async def root3(numbers: str):
    """GET request with query parameter returning "123" and s concatenation."""
    return "123" + numbers


@app.post("/123concat")
async def root4(item: list[int]):
    """Post request returning concatenation of [1, 2, 3] and list in request body."""
    return [1, 2, 3] + item


@app.post("/concat{s}")
async def root5(numbers: str, item: list[int]):
    """Post request returning concatenation of (list[int])s and list in request body."""
    return list(map(int, numbers)) + item
