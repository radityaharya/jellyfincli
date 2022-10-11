class Library:
    """
    This function is used to get the item ID of a library by the name of the library.
    """

    def __init__(self, jf_client, console, admin_user_id):
        self.jf_client = jf_client
        self.console = console
        self.admin_user_id = admin_user_id

    def get_library_items(self, item_id: str):
        """
        This function gets all the items in a library by the item ID of the library

        :param item_id: The item ID of the library
        :type item_id: str
        :return: None
        """
        items = self.jf_client.items.get_items_by_user_id(
            user_id=self.admin_user_id,
            parent_id=item_id,
        )
        return items

    def get_libraries(self) -> None:
        """
        It prints out the name, item ID, and path of each library in the Jellyfin server
        :return: None
        """
        mediafolders = self.jf_client.library.get_media_folders()
        self.console.print(
            f"[bold green]{'Name':<20} {'Item ID':<35} {'Path':<45} {'Number of Items':<40}[/bold green]"
        )
        for library in mediafolders.items:
            try:
                number_of_items = len(self.get_library_items(library.id).items)
            except Exception as e:
                number_of_items = 0
            self.console.print(
                f"{library.name:<20} {library.id:<35} {library.path:<45} {number_of_items:<40}"
            )
        return None

    def _get_library_id_by_name(self, name: str) -> str | None:
        mediafolders = self.jf_client.library.get_media_folders()
        for library in mediafolders.items:
            if library.name.lower() == name.lower():
                return library.id
        return None

    def _get_library_name_by_id(self, item_id: str) -> str | None:
        mediafolders = self.jf_client.library.get_media_folders()
        for library in mediafolders.items:
            if library.id == item_id:
                return library.name
        return None

    def refresh_library(self, library_id: str = None, library_name: str = None):
        """
        This function refreshes a library by either the library_id or the library_name

        :param library_id: The ID of the library you want to refresh
        :type library_id: str
        :param library_name: The name of the library you want to refresh
        :type library_name: str
        :return: None
        """
        if library_id:
            self.console.print(f"Refreshing {self._get_library_name_by_id(library_id)}")
            self.jf_client.item_refresh.refresh_item(item_id=library_id)
        elif library_name:
            library_id = self._get_library_id_by_name(library_name)
            self.console.print(f"Refreshing {self._get_library_name_by_id(library_id)}")
            self.jf_client.item_refresh.refresh_item(item_id=library_id)
        else:
            self.console.print(
                "Please specify [bold]--library_name[/bold] or [bold]--library_id[/bold]"
            )
        return None
