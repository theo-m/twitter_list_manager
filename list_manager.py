#!/usr/bin/env python

import twitter
import dotenv

import os
from typing import List, NamedTuple

TwitterList = NamedTuple(
    "TwitterList", (("props", twitter.List), ("members", List[twitter.User]))
)


def loop_start_screen(idx: int, u: twitter.User, lists: List[TwitterList]):
    print("\033c", end="")  # Clears the screen
    print(
        f"[{idx:4d}] @{u.screen_name} '{u.name}' - https://twitter.com/{u.screen_name}\n{u.description}\n---\n"
    )
    for i, (list_props, list_members) in enumerate(lists):
        inlist = (
            "*" if u.screen_name in [u_.screen_name for u_ in list_members] else " "
        )
        print(f"[{i:3d}]: {inlist} {list_props.name}")
    print("\n---\n[r]: refresh lists")
    print("[c]: create a new list")
    print("[u]: unfollow")
    print("[n|⏎]: next")
    print("[p]: previous")
    print("[g]: go to index")
    print("[q]: quit")

    inp = _get_input()
    return inp


def _get_input():
    while True:
        inp = input("\nEnter a command or a list number: ").strip()
        if inp not in ["r", "c", "n", "p", "u", "q", "g", ""]:
            try:
                int(inp)
            except ValueError:
                continue
        break
    return inp


def get_api() -> twitter.Api:
    dotenv.load_dotenv()
    api = twitter.Api(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET_KEY"),
        access_token_key=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )
    return api


def get_lists(api: twitter.Api) -> List[TwitterList]:
    _lists = api.GetListsList()
    lists = [
        TwitterList(lst, api.GetListMembers(lst.id)) for i, lst in enumerate(_lists)
    ]
    return sorted(lists, key=lambda lst: lst.props.full_name)


def loop():
    api = get_api()
    lists = get_lists(api)
    following = api.GetFriends()

    idx = 0
    while idx < len(following):
        u = following[idx]
        inp = loop_start_screen(idx, u, lists)

        # --- Refresh
        if inp == "r":
            lists = get_lists(api)
            continue

        # --- Create list
        if inp == "c":
            n = input("list name: ")
            api.CreateList(n, "private", description=None)
            lists = get_lists(api)
            continue

        # --- Quit
        if inp == "q":
            break

        # --- Next user
        if inp == "n" or inp == "":
            idx += 1
            continue

        # --- Previous user
        if inp == "p":
            idx -= 1
            continue

        # --- Go to index
        if inp == "g":
            while True:
                inp = input("idx: ").strip()
                try:
                    int(inp)
                except ValueError:
                    continue
                break
            idx = int(inp)
            continue

        # --- Unfollow
        if inp == "u":
            api.DestroyFriendship(user_id=u.id)
            following.remove(u)
            idx += 1
            continue

        try:
            list_props, list_members = lists[int(inp)]
        except IndexError:
            print(f"{int(inp)} but values: 0...{len(lists) - 1}")
            continue

        print(f"Adding '{u.name}' to '{list_props.full_name}'")
        api.CreateListsMember(list_id=list_props.id, user_id=u.id)
        lists[int(inp)].members.append(u)


if __name__ == "__main__":
    loop()
