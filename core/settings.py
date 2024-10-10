from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    payments_token: str
    admin_id: int
    api_path: str
    site_path: str
    temporary_path: str
    ws_path: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("BOT_TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            api_path=env.str("API_PATH"),
            site_path=env.str("SITE_PATH"),
            payments_token=env.str("PAYMENTS_TOKEN"),
            temporary_path=env.str("TEMPORARY_PATH"),
            ws_path=env.str("WS_PATH"),
        )
    )


settings = get_settings('.env')
