from jellyfinapi.models.user_dto import UserDto
from jellyfinapi.models.user_policy import UserPolicy
from jellyfinapi.models.update_user_password import UpdateUserPassword
from jellyfinapi.models.user_configuration import UserConfiguration
from jellyfinapi.models.create_user_by_name import CreateUserByName
from jellyfinapi.exceptions.api_exception import APIException

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
            try:
                last_activity_str = user.last_activity_date.datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except AttributeError:
                last_activity_str = "None"
            self.console.print(f"{user.name:<30} {user.id:<40} {last_activity_str:<40}")
        return None

    def _get_user_id_by_name(self, name: str) -> str:
        try:
            users = self.jf_client.user.get_users()
            for user in users:
                if user.name == name:
                    return user.id
            raise ValueError(f"User {name} not found")
        except Exception as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")
            return None
    
    def create_user(self, username:str = None, password:str = None) -> UserDto:
        """
        Creates a user in the Jellyfin server
        """
        try:
            if username is None:
                raise ValueError("--username is required")
            if password is None:
                raise ValueError("please specify --password")
            new_user = self.jf_client.user.create_user_by_name(CreateUserByName(name=username, password=password))
            self.console.print(f"[bold green]User {new_user.name} Created Successfuly[/bold green]")
        except Exception as api_exception:
            self.console.print(f"[bold red]Error creating user: {api_exception}[/bold red]")
        
    def delete_user(self, username:str = None, user_id:str = None) -> None:
        """
        Deletes a user in the Jellyfin server
        """
        try:
            if not user_id:
                user_id = self._get_user_id_by_name(username)
            if not username:
                username = self.jf_client.user.get_user(user_id).name
            self.jf_client.user.delete_user(user_id)
            self.console.print(f"[bold green]User {username} Deleted Successfuly[/bold green]")
        except Exception as api_exception:
            self.console.print(f"[bold red]Error deleting user: {api_exception}[/bold red]")
        return None
    
    def edit_user(
        self,
        id:str = None,
        name:str = None,
        new_name = None,
        password:str = None,
        new_password:str = None,
    )-> None:
        """
        edit a user.
        """
        if not id:
            id = self._get_user_id_by_name(name)
        if not name:
            name = self.jf_client.user.get_user(id).name
        if new_name:
            try:
                self.jf_client.user.update_user(
                    body = UserDto(
                        name=name,
                    )
                )
            except APIException as api_exception:
                self.console.print(f"[bold red] Unable to edit user {id}: {api_exception}")
        if password and new_password:
            try:
                self.jf_client.user.update_user_password(
                    user_id = id,
                    body = UpdateUserPassword(
                        current_pw = password,
                        new_pw = new_password,
                    )
                )
            except APIException as api_exception:
                self.console.print(f"[bold red] Unable to edit user {id}: {api_exception}")
    def edit_user_advance(
      self,
      user_id  
    ):
        pass
