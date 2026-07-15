import uvicorn

from config import Config
from registrar import register_fastapi_app

config = Config()

app = register_fastapi_app(config.fastapi)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
