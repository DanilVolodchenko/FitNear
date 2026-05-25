from dishka import make_async_container

from di.application import ApplicationProvider
from di.infrastructure import InfrastructureProvider
from di.config import ConfigProvider
from core.config import Config, config

ioc = make_async_container(
    ApplicationProvider(),
    InfrastructureProvider(),
    context={Config: config},
)
