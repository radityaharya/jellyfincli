class MediaItems:
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
        pass

    def refresh_item(self, item_id: str):
        """
        This function refreshes a single item by the item ID

        :param item_id: The item ID of the item to refresh
        :type item_id: str
        :return: None
        """
        self.jf_client.items.refresh_item(
            item_id=item_id,
        )
        return None
