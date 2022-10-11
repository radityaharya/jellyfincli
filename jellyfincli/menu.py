import sys


class Menu:
    def __init__(self, jf):
        self.jf = jf

    def _get_server_info(self):
        """
        Gets the server info
        """
        return self.jf.jf_client.system.get_system_info().__dict__

    def _print_server_info(self):
        """
        Prints the server info
        """
        server_info = self._get_server_info()
        self.jf.console.print(
            f"""Server Name: {server_info['server_name']}
Public URL: {self.jf.server_url}
Jellyfin Version: {server_info['version']}
Operating System: {server_info['operating_system']}
"""
        )
        if server_info["has_update_available"] == True:
            self.jf.console.print("[bold red]Update Available[/bold red]")
        if server_info["has_pending_restart"] == True:
            self.jf.console.print("[bold red]Restart Required[/bold red]")
        return ""

    def _welcome(self):
        """
        Prints the welcome message
        """
        self.jf.console.print(
            f"[bold purple]JellyfinCLI - v{self.jf.version}[/bold purple]"
        )

    def interactive(self):
        """
        It prints out a list of available menus, then prompts the user to select one
        """
        self._welcome()
        self._print_server_info()
        methods = [
            method
            for method in dir(self.jf)
            if not method.startswith("_") and callable(getattr(self.jf, method))
        ]
        menus = {
            "libraries": [
                method
                for method in methods
                if "library" in method or "libraries" in method
            ],
            "users": [
                method for method in methods if "user" in method or "users" in method
            ],
        }

        self.jf.console.print("[bold green]Available Actions[/bold green]")
        count = 1
        for menu in menus:
            self.jf.console.print(f"[bold]{menu}[/bold]")
            for method in menus[menu]:
                help_string = getattr(self.jf, method).__doc__
                help_string = help_string.split(":")[0].strip()

                self.jf.console.print(
                    f"    {count}. {method.replace('_', ' ')}: {help_string}"
                )
                count += 1

        selection = 0
        try:
            while selection not in range(1, count):
                selection = self.jf.console.input("[bold]Select an action:[/bold] ")
                try:
                    selection = int(selection)
                except ValueError:
                    selection = 0
                    self.jf.console.print("[bold red]Invalid selection[/bold red]")
        except KeyboardInterrupt:
            self.jf.console.print("[bold red]\nExiting[/bold red]")
            sys.exit()

        method_indexes = {}
        index_count = 1
        for menu in menus:
            for method in menus[menu]:
                method_indexes[index_count] = method
                index_count += 1

        if int(selection) in method_indexes:
            # checks if the method requires arguments
            method = getattr(self.jf, method_indexes[int(selection)])
            if method.__code__.co_argcount > 1:
                self.jf.console.print(
                    f"[bold]\n{method.__name__} requires arguments[/bold]"
                )
                args = []
                for arg in method.__code__.co_varnames[1:]:
                    arg_type = method.__annotations__[arg].__name__
                    default = method.__defaults__[
                        method.__code__.co_varnames.index(arg)
                        - method.__code__.co_argcount
                    ]
                    arg_input = self.jf.console.input(
                        f"[bold]{arg}\[type: {arg_type}] \[{default}]:[/bold] "
                    )
                    # change arg_input to the correct type
                    if arg_type == "str":
                        arg_input = str(arg_input)
                    elif arg_type == "int":
                        arg_input = int(arg_input)
                    elif arg_type == "bool":
                        arg_input = bool(arg_input)
                    args.append(arg_input)
                method(*args)
            else:
                method()
