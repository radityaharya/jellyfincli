import argparse
import logging
import os

from dotenv import load_dotenv
from jellyfinapi.jellyfinapi_client import JellyfinapiClient
from rich import print

if __name__ == "__main__":
    load_dotenv(override=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="server url")
    parser.add_argument("--token", help="token")
    parser.add_argument("--list", help="list")
    parser.add_argument("--refresh", help="refresh library or item", choices=["library", "item"])
    parser.add_argument("--library_name", help="library name")
    parser.add_argument("--library_id", help="library id")
    parser.add_argument("--item_id", help="item id")
    parser.add_argument("--save", help="save auth info to .env file")
    args = parser.parse_args()

    if args.server and args.token:
        client = JellyfinapiClient(
            x_emby_token=args.token,
            server_url=args.server,
        )

        if args.save:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"JELLYFIN_SERVER={args.server}")
                f.write(f"JELLYFIN_TOKEN={args.token}")
    else:
        client = JellyfinapiClient(
            x_emby_token=os.getenv("JELLYFIN_TOKEN"),
            server_url=os.getenv("JELLYFIN_SERVER"),
        )

    logging.getLogger("jellyfinapi").setLevel(logging.CRITICAL)

    if args.list:
        if args.list == "users":
            users = client.user.get_users()
            for user in users:
                print(
                    f"[bold]{'User Name':<15} {'User ID':<40} {'Last Activity':<15}[/bold]"
                )
                last_activity_string = user.last_activity_date.datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                print(f"{user.name:<15} {user.id:<40} {last_activity_string:<15}")
        elif args.list == "libraries":
            libraries = client.library_structure.get_virtual_folders()
            print(f"[bold]{'Library Name':<30} {'Item ID':<40} {'location':30}[/bold]")
            for library in libraries:
                print(f"{library.name:<30} {library.item_id:<40} {library.locations}")

    if args.refresh:
        if args.refresh == "library":
            if args.library_id:
                client.items.refresh_item(item_id=args.library_id)
            elif args.library_name:
                libraries = client.library.get_media_folders()
                for library in libraries.items:
                    if library.name == args.library_name:
                        client.item_refresh.refresh_item(item_id=library.id)
            else:
                print(
                    "Please specify [bold]--library_name[/bold] or [bold]--library_id[/bold]"
                )
        elif args.refresh == "item":
            if args.item_id:
                client.items.refresh_item(item_id=args.item_id)
            else:
                print("Please specify [bold]--library_id[/bold]")
                