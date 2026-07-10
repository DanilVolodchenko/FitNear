from dishka import Provider, Scope, provide

from application.interfaces.generator import IStringGenerator
from application.interfaces.localization import ITranslator
from application.interfaces.security import IHasher, IPwdHasher
from application.interfaces.template import IHTMLTemplate
from application.interfaces.repositories import (
    IUserReader,
    IUserRemover,
    IUserSaver,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    IRegistrationTokenUpdater,
)
from application.interfaces.transaction import ITransactionManager
from application.services.auth import RegisterUserService
from core.config import Config


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_register_user_service(
        self,
        config: Config,
        tranlator: ITranslator,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        reg_token_reader: IRegistrationTokenReader,
        reg_token_saver: IRegistrationTokenSaver,
        reg_token_updater: IRegistrationTokenUpdater,
        pwd_hasher: IPwdHasher,
        string_generator: IStringGenerator,
        hasher: IHasher,
        html_template: IHTMLTemplate,
        trx_manager: ITransactionManager,
    ) -> RegisterUserService:
        return RegisterUserService(
            config=config,
            translator=tranlator,
            user_reader = user_reader,
            user_saver = user_saver,
            user_remover = user_remover,
            reg_token_reader = reg_token_reader,
            reg_token_saver = reg_token_saver,
            reg_token_updater = reg_token_updater,
            pwd_hasher = pwd_hasher,
            string_generator = string_generator,
            hasher = hasher,
            html_template = html_template,
            trx_manager = trx_manager,
        )

    register_user_service = provide(
        RegisterUserService,
        scope=Scope.REQUEST,
    )
