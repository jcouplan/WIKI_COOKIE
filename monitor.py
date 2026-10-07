import os
import json
import requests
from pathlib import Path

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
COOKIE = os.environ.get("WIKI_COOKIE")
CACHE_FILE = Path("cache.json")

WATCHLIST = [
    "Franck Thilliez", "Jean-Marc Jancovici", "CNews", "Garonne",
    "Grand remplacement", "Haute-Garonne", "Ironman", "Paradoxe de Fermi",
    "Pascal Praud", "Philippe Poutou", "Article 49 alinéa 3 de la Constitution de la Cinquième République française",
    "Banoffee pie", "Coke en stock", "Garmin", "Islamo-gauchisme",
    "Journal d'un dégonflé", "L'Affaire Tournesol", "L'Étoile mystérieuse",
    "L'Île Noire", "L'Oreille cassée", "Le Crabe aux pinces d'or",
    "Le Lotus bleu", "Le Sceptre d'Ottokar", "Le Secret de La Licorne",
    "Le Temple du Soleil", "Le Trésor de Rackham le Rouge",
    "Les Bijoux de la Castafiore", "Les Cigares du pharaon",
    "Les Sept Boules de cristal", "Master Poulet", "Néolibéralisme",
    "Nujabes", "Objectif Lune", "Omar m'a tuer", "On a marché sur la Lune",
    "Playboi Carti", "Rilès", "Tintin au Congo", "Tintin au pays de l'or noir",
    "Tintin au pays des Soviets", "Tintin au Tibet", "Tintin en Amérique",
    "Tintin et l'Alph-Art", "Tintin et les Picaros", "Vol 714 pour Sydney",
    "Fédération internationale des échecs", "François Couplan",
    "Good Kid, M.A.A.D City", "Institut national des sciences appliquées de Toulouse",
    "Philippe Bihouix"
]

def load_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            return set()
    return set()

def save_cache(cache_data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(cache_data), f)

def alert_discord(card_name, auction_id):
    if not WEBHOOK_URL:
        return
    data = {
        "content": f"🚨 **{card_name}** est sur le marché !\nLien : https://www.wiki-masters.com/marketplace",
        "username": "WikiSniper"
    }
    requests.post(WEBHOOK_URL, json=data)

def main():
    url = "https://www.wiki-masters.com/api/marketplace?page=1&limit=50&sort=recent"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:156.0) Gecko/20100101 Firefox/156.0",
        "Accept": "application/json",
        "Cookie": COOKIE
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur de requête: {e}")
        return

    data = response.json()
    auctions = data.get("auctions", [])
    cache = load_cache()
    new_finds = 0

    for auction in auctions:
        auction_str = str(auction)
        auction_id = str(auction.get("id", hash(auction_str)))

        if auction_id in cache:
            continue

        for card in WATCHLIST:
            if card in auction_str:
                print(f"Match: {card}")
                alert_discord(card, auction_id)
                cache.add(auction_id)
                new_finds += 1
                break

    if new_finds > 0:
        save_cache(cache)

if __name__ == "__main__":
    main()