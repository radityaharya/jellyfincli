class System:
    def __init__(self, jf_client, console, admin_user_id) -> None:
        self.jf_client = jf_client
        self.console = console
        self.admin_user_id = admin_user_id
        
    def system_restart(self) -> None:
        """
        Restarts jellyfin instance (non docker instalation)
        """
        self.jf_client.system.restart()
        self.console.print("[bold green]Jellyfin Restarted[/bold green]")
    
    def get_system_info(self) -> dict:
        """
        Returns system info
        """
        pass