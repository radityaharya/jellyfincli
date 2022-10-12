import argparse
import logging
import os

from dotenv import load_dotenv

from jellyfincli import JellyfinCLI
from menu import Menu

if __name__ == "__main__":
    load_dotenv(override=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="server url")
    parser.add_argument("--token", help="token")
    parser.add_argument("--admin_user_id", help="admin user id")
    parser.add_argument("--list", help="list")
    parser.add_argument(
        "--refresh", help="refresh library or item", choices=["library", "item"]
    )
    parser.add_argument("--create", help="creates new {option}", choices=["user", "library"])
    parser.add_argument("--library_name", help="library name")
    parser.add_argument("--library_id", help="library id")
    parser.add_argument("--username", help="username")
    parser.add_argument("--password", help="password")
    parser.add_argument("--item_id", help="item id")
    parser.add_argument(
        "--save",
        help="save auth info to .env file or erase existing config",
        choices=["erase", ""],
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="count", default=0
    )
    args = parser.parse_args()

    if args.server and args.token:
        if args.save:
            if args.save == "erase":
                os.remove(".env")
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"JELLYFIN_SERVER={args.server}")
                f.write(f"JELLYFIN_TOKEN={args.token}")
                f.write(f"JELLYFIN_ADMIN_USER_ID={args.admin_user_id}")

    else:
        load_dotenv(override=True)
        jf = JellyfinCLI(
            x_emby_token=os.environ.get("JELLYFIN_TOKEN"),
            server_url=os.environ.get("JELLYFIN_SERVER"),
            admin_user_id=os.environ.get("JELLYFIN_ADMIN_USER_ID"),
        )

    logging.getLogger("jellyfinapi").setLevel(logging.CRITICAL)

    if args.verbose:
        if args.verbose == 1:
            logging.getLogger("jellyfinapi").setLevel(logging.INFO)
        elif args.verbose >= 2:
            logging.getLogger("jellyfinapi").setLevel(logging.DEBUG)

    if args.list:
        if args.list == "users":
            jf.get_users()
        elif args.list == "libraries":
            jf.get_libraries()

    elif args.refresh:
        if args.refresh == "library":
            if args.library_id:
                jf.refresh_library(library_id=args.library_id)
            elif args.library_name:
                jf.refresh_library(library_name=args.library_name)
            else:
                print(
                    "Please specify [bold]--library_name[/bold] or [bold]--library_id[/bold]"
                )
        elif args.refresh == "item":
            if args.item_id:
                jf.refresh_item(item_id=args.item_id)
            else:
                print("Please specify [bold]--library_id[/bold]")
    elif args.create:
        if args.create=="user": 
            jf.create_user(args.username, args.password)
    # if no arguments are passed except for -v, run the menu
    if not any(vars(args).values()) or args.verbose > 0:
        Menu(jf).interactive()
