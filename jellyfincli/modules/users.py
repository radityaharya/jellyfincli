class Users:
    def __init__(self, jf_client, console, admin_user_id):
        self.jf_client = jf_client
        self.console = console
        self.admin_user_id = admin_user_id

    def get_users(self) -> None:
        """
        This function prints out the name, ID, and Last Activity of each user in the Jellyfin server
        :return: None
        """
        users = self.jf_client.user.get_users()
        self.console.print(
            f"[bold green]{'Name':<30} {'ID':<40} {'Last Activity':<40}[/bold green]"
        )
        for user in users:
            last_activity_str = user.last_activity_date.datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            self.console.print(f"{user.name:<30} {user.id:<40} {last_activity_str:<40}")
        return None

    def _get_user_id_by_name(self, name: str) -> str | None:
        users = self.jf_client.users.get_users()
        for user in users.items:
            if user.name == name:
                return user.id
        return None
