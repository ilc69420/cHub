#!/usr/bin/env python3
import argparse
import requests
import random
import json

BASE_URL = "http://localhost:8000/pokemon"  # change if your API runs elsewhere

POKEMON_NAMES = ["Pikachu", "Charizard", "Mewtwo", "Eevee", "Gyarados", "Snorlax", "Bulbasaur", "Squirtle"]
CARD_SETS = ["Base Set", "Base Set Holo", "Jungle", "Fossil", "Team Rocket", "Gym Heroes"]

def fetch_que():
    resp = requests.get(f"{BASE_URL}/fetch-que")
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
        f"{BASE_URL}/insert-into-que",
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
        f"{BASE_URL}/insert-scraped-data",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    print(resp.status_code, resp.text)

def main():
    parser = argparse.ArgumentParser(description="CLI tool for Pokémon API with dummy data")
    subparsers = parser.add_subparsers(dest="command")

    # fetch-que
    subparsers.add_parser("fetch-que", help="Fetch one item from the Pokémon queue")

    # insert-into-que
    que_parser = subparsers.add_parser("insert-que", help="Insert dummy cards into the Pokémon queue")
    que_parser.add_argument("-n", "--num", type=int, default=3, help="Number of dummy cards to insert")

    # insert-scraped-data
    scraped_parser = subparsers.add_parser("insert-scraped", help="Insert dummy scraped data into table")
    scraped_parser.add_argument("-n", "--num", type=int, default=3, help="Number of dummy scraped entries to insert")

    args = parser.parse_args()

    if args.command == "fetch-que":
        fetch_que()
    elif args.command == "insert-que":
        insert_into_que(args.num)
    elif args.command == "insert-scraped":
        insert_scraped_data(args.num)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
