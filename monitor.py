import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
COOKIE = os.environ.get("WIKI_COOKIE")
CACHE_FILE = Path("cache.json")

WATCHLIST = {
    "52024fad-620f-462e-aee4-2856ae7092e9": "Franck Thilliez",
    "f544c0d2-40bc-4919-bbf7-0796a5d386ea": "Jean-Marc Jancovici",
    "94e5fa27-55c6-4dd3-b203-5ae1e30e7cea": "CNews",
    "9c82c287-ab8b-40f1-b0c4-25933c80dbf9": "Garonne",
    "94bfc70c-b3d0-46d8-9ef9-75f2c5bab102": "Grand remplacement",
    "1bd839db-ffda-4260-aade-adbed56da062": "Haute-Garonne",
    "ec2d28f7-aac3-4342-b88d-8eada9a3bd17": "Ironman",
    "2964c8a0-c3fa-45bc-9c51-67e6a99b67ae": "Paradoxe de Fermi",
    "bfea774a-34e8-442d-9d20-8e381580db3c": "Pascal Praud",
    "1ac1fb16-0878-41b6-b1d6-f5ec68b4a09b": "Philippe Poutou",
    "2ac49a52-0edb-472c-b113-6fa5027f7e3c": "Article 49 alinéa 3 de la Constitution de la Cinquième République française",
    "d4ef0914-df47-4949-bca8-ad2f68ffcf52": "Banoffee pie",
    "07a8b53f-dd4c-4271-a88a-35f04cd32036": "Coke en stock",
    "cf6fc71b-e9db-4b92-9fe7-51ea5c4cd9a7": "Garmin",
    "e560b424-dac2-4cec-a16e-651f12e951ae": "Islamo-gauchisme",
    "a0ec6fb4-8aca-4a4f-b738-c85f477ec00e": "Journal d'un dégonflé",
    "f3e2f2b4-ac92-406e-93d8-6cc8acb4100e": "L'Affaire Tournesol",
    "4008b663-bc83-40ad-915d-fd006bec26d1": "L'Étoile mystérieuse",
    "5c052377-29f2-4a55-aeff-bb9a5747bd7e": "L'Île Noire",
    "09db033a-c5da-4ac3-a95f-6ef37d363a25": "L'Oreille cassée",
    "00aebde5-49cf-4ad1-ba0e-4819e9a7d346": "Le Crabe aux pinces d'or",
    "ded893c3-2fc6-4f79-ac42-e9bc18c70084": "Le Sceptre d'Ottokar",
    "a925f6dd-1b59-49b9-87c8-a2fcb022d0dc": "Le Secret de La Licorne",
    "70694c0b-ceaa-42b6-af85-c206b2c7ce35": "Le Temple du Soleil",
    "ac498f4c-7441-4d2e-a501-c00fc82bffeb": "Le Trésor de Rackham le Rouge",
    "083b9f31-d5b4-415c-9f08-723c5317c514": "Les Bijoux de la Castafiore",
    "8fb675fd-ea46-46dd-baa9-5363b0dd144f": "Les Cigares du pharaon",
    "4a3b87f3-b0c3-4d60-9694-0d2c3e3c8fd9": "Les Sept Boules de cristal",
    "7b21b996-91a1-4891-b773-38be5c685ad5": "Master Poulet",
    "27e34332-151d-4893-96a7-247de99a240b": "Néolibéralisme",
    "a7f7a00e-0c9a-440d-9087-b6ccd4f0e290": "Nujabes",
    "f0b45c10-310f-4f9e-b2b6-7382ef49f1d5": "Objectif Lune",
    "12b0eec7-2f2a-4239-a503-ee3bf65ccf08": "Omar m'a tuer",
    "996fc086-a27d-4628-b9d9-7c708fa08c51": "On a marché sur la Lune",
    "2f3c4537-dc36-410a-8ae0-c0176041bab3": "Playboi Carti",
    "a216e252-8c65-47d9-b623-f26c446d7135": "Rilès",
    "66411b74-d0d2-4424-8826-c8da4b31270c": "Tintin au Congo",
    "d99bbf82-06ad-4cdd-b4e3-b2f9c0b09614": "Tintin au pays de l'or noir",
    "7b45794f-4103-4b8b-9500-81abfe391607": "Tintin au pays des Soviets",
    "96d2a5e4-642c-457c-93f4-511bdbd5fd93": "Tintin au Tibet",
    "83b7ef42-b314-4e84-94d3-97ed0eaee204": "Tintin en Amérique",
    "841b7e2d-42b3-4d35-8497-2e096893500e": "Tintin et l'Alph-Art",
    "6464b424-b409-4649-a51e-78ec502278f1": "Tintin et les Picaros",
    "f003c616-3ab8-41f6-b516-8bf59bb83348": "Vol 714 pour Sydney",
    "00958246-e8c8-4bbd-8b0c-97b6dc006c44": "Fédération internationale des échecs",
    "7951126c-f232-4238-a5df-ada2f7251be7": "François Couplan",
    "72f81a70-0e8a-410c-a84f-0d53843b0e9e": "Good Kid, M.A.A.D City",
    "76f0cf95-8d03-49bd-a947-b392de94d1f7": "Institut national des sciences appliquées de Toulouse",
    "4557681a-a957-490f-996c-725af218d917": "Philippe Bihouix",
    "0ab8685f-3018-49ef-bd8d-bf6ed2a5b98b": "ReMarkable"
}

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

def get_time_remaining(end_at_str):
    if not end_at_str:
        return "inconnue"
    try:
        end_time = datetime.fromisoformat(end_at_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = end_time - now
        total_seconds = int(diff.total_seconds())

        if total_seconds <= 0:
            return "terminée"

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            return f"{hours}h {minutes:02d}m"
        return f"{minutes}m"
    except Exception:
        return "inconnue"

def alert_discord(card_name, price, time_left):
    if not WEBHOOK_URL:
        return
    data = {
        "content": f"🚨 **{card_name}** est sur le marché !\n💰 Mise actuelle : **{price} W** | ⏳ Reste : **{time_left}**\nhttps://www.wiki-masters.com/marketplace",
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
        print(f"Erreur API : {e}")
        return

    data = response.json()
    auctions = data.get("auctions", [])
    cache = load_cache()
    new_finds = 0

    for auction in auctions:
        auction_id = auction.get("id")
        card_id = auction.get("card_id")

        if not auction_id or auction_id in cache:
            continue

        if card_id in WATCHLIST:
            card_name = WATCHLIST[card_id]
            price = auction.get("current_bid") or auction.get("base_amount") or "?"
            end_at = auction.get("end_at")
            time_left = get_time_remaining(end_at)

            print(f"Trouvé : {card_name} | {price} W | Reste : {time_left}")
            alert_discord(card_name, price, time_left)
            cache.add(auction_id)
            new_finds += 1

    print(f"Total alertes envoyées : {new_finds}")
    if new_finds > 0:
        save_cache(cache)

if __name__ == "__main__":
    main()
