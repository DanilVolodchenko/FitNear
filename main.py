import uvicorn

from core.config import config
from registrar import register_fastapi_app

app = register_fastapi_app(config.fastapi)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
