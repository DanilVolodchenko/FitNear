from dishka import make_async_container

from config import Config, config
from di.application import ApplicationProvider
from di.infrastructure import InfrastructureProvider

ioc = make_async_container(
    ApplicationProvider(),
    InfrastructureProvider(),
    context={Config: config},
)
