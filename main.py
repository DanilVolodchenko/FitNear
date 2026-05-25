import uvicorn

from core.registrar import register_app
from core.config import config

if __name__ == '__main__':
    app = register_app(config.fastapi)

    uvicorn.run(app)
