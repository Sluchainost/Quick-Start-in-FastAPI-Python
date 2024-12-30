"""A module that provides a server for efficient operation of applications."""

import uvicorn

from fastapi import FastAPI


app = FastAPI()


@app.post('/calculate')
async def calculate(num1: int, num2: int):
    """ returns json with the sum of two numbers """

    return {f'sum of numbers {num1} and {num2} is ': f'{num1+num2}'}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
