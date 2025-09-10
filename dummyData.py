#!/usr/bin/env python3
import argparse
import requests
import random
import json

BASE_URL = "http://localhost:8000"  # change if your API runs elsewhere

POKEMON_NAMES = [
    "Pikachu", "Charizard", "Mewtwo", "Eevee", "Gyarados",
    "Snorlax", "Bulbasaur", "Squirtle", "Jigglypuff", "Dragonite"
]
CARD_SETS = [
    "Base Set", "Base Set Holo", "Jungle", "Fossil",
    "Team Rocket", "Gym Heroes"
]

# ---- POKEMON ----
def fetch_que():
    resp = requests.get(f"{BASE_URL}/pokemon/fetch-que")
    print(resp.status_code, resp.text)

def insert_into_que(n: int):
    cards = []
    for _ in range(n):
        cards.append({
            "name": random.choice(POKEMON_NAMES),
            "number": str(random.randint(1, 151)),
            "card_set": random.choice(CARD_SETS)
        })
    resp = requests.post(
        f"{BASE_URL}/pokemon/insert-into-que",
        headers={"Content-Type": "application/json"},
        data=json.dumps(cards)
    )
    print(resp.status_code, resp.text)

def insert_scraped_data(n: int):
    data = []
    for _ in range(n):
        data.append({
            "name": random.choice(POKEMON_NAMES),
            "number": str(random.randint(1, 151)),
            "card_set": random.choice(CARD_SETS),
            "price": random.randint(10, 2000),
            "shipping": random.randint(0, 20),
            "seller": f"Seller{random.randint(1, 999)}"
        })
    resp = requests.post(
        f"{BASE_URL}/pokemon/insert-auctions-ended",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    print(resp.status_code, resp.text)

# ---- PROXIES ----
def insert_proxies(file_path: str):
    with open(file_path, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    proxy_dicts = [{"proxy": p} for p in proxies]

    resp = requests.post(
        f"{BASE_URL}/proxies/insert-proxies",
        headers={"Content-Type": "application/json"},
        data=json.dumps(proxy_dicts)
    )
    print(resp.status_code, resp.text)

def fetch_proxies():
    resp = requests.get(f"{BASE_URL}/proxies/fetch-proxies")
    print(resp.status_code, resp.text)

# ---- MAIN ----
def main():
    parser = argparse.ArgumentParser(description="CLI tool for Pokémon & Proxies API")
    subparsers = parser.add_subparsers(dest="command")

    # Pokémon commands
    subparsers.add_parser("fetch-que", help="Fetch one item from the Pokémon queue")

    que_parser = subparsers.add_parser("insert-que", help="Insert dummy cards into Pokémon queue")
    que_parser.add_argument("-n", "--num", type=int, default=3, help="Number of dummy cards to insert")

    scraped_parser = subparsers.add_parser("insert-scraped", help="Insert dummy scraped Pokémon data")
    scraped_parser.add_argument("-n", "--num", type=int, default=3, help="Number of dummy scraped entries to insert")

    # Proxy commands
    proxy_insert = subparsers.add_parser("insert-proxies", help="Insert proxies from a file")
    proxy_insert.add_argument("file", help="Path to file containing proxies (one per line)")

    subparsers.add_parser("fetch-proxies", help="Fetch all proxies from DB")

    args = parser.parse_args()

    # Pokémon
    if args.command == "fetch-que":
        fetch_que()
    elif args.command == "insert-que":
        insert_into_que(args.num)
    elif args.command == "insert-scraped":
        insert_scraped_data(args.num)
    # Proxies
    elif args.command == "insert-proxies":
        insert_proxies(args.file)
    elif args.command == "fetch-proxies":
        fetch_proxies()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
