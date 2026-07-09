import uvicorn

from core.config import config
from core.registrar import register_app

app = register_app(config.fastapi)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
