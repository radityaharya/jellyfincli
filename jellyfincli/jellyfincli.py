from modules.library import Library
from modules.users import Users
from jellyfinapi.jellyfinapi_client import JellyfinapiClient
from rich.console import Console
import logging


class JellyfinCLI(Library, Users):
    def __init__(self, x_emby_token, server_url, admin_user_id):
        self.jf_client = JellyfinapiClient(
            x_emby_token=x_emby_token,
            server_url=server_url,
        )
        self.logger = logging.getLogger("jellyfinapi")
        self.logger.setLevel(logging.CRITICAL)
        self.console = Console()
        self.admin_user_id = admin_user_id
        self.server_url = server_url
        self.version = "0.0.1-dev"
