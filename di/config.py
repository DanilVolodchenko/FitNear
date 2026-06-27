from dishka import Provider, Scope, provide

from core.config import Config, SecurityConfig


class ConfigProvider(Provider):
    config = provide(Config, scope=Scope.APP)
    security_config = provide(SecurityConfig, scope=Scope.APP)
