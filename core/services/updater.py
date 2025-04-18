import requests
from ..models import Pokemon
from django.db import transaction

API_BASE_URL = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=1500"

def update_pokemon_list():
    response = requests.get(API_BASE_URL)
    data = response.json()
    remote_list = data.get("results", [])

    if Pokemon.objects.count() == len(remote_list):
        return {"status": "Up to Date"}

    with transaction.atomic():
        for result in remote_list:
            try:
                poke_id = int(''.join(filter(str.isdigit, result["url"][-10:])))
                pokemon_data = build_pokemon_object(result["name"], result["url"], poke_id)
                obj, created = Pokemon.objects.update_or_create(
                    id=poke_id,
                    defaults=pokemon_data
                )
                print(f"{obj.name} fue {'creado' if created else 'actualizado'} satisfactoriamente")
            except Exception as e:
                print(f"Error procesando {result['name']}: {e}")
    return {"status": "Updated", "count": len(remote_list)}

def build_pokemon_object(name, url, poke_id):
    pokemon = {
        "name": name,
        "baseUrl": url,
        "listimg": "",
        "detimg": "",
        "types": "",
        "evolvesFrom": "",
        "evolvesTo": "",
        "flavor": "",
        "strongAgainst": "",
        "weakAgainst": "",
        "noDamageTo": "",
        "noDamageFrom": "",
    }

    response = requests.get(url).json()
    sprites = response.get("sprites", {})
    pokemon["listimg"] = sprites.get("front_default", "")
    pokemon["detimg"] = sprites.get("other", {}).get("official-artwork", {}).get("front_default", "")
    
    types_data = response.get("types", [])
    fill_types(types_data, pokemon)

    species_url = response.get("species", {}).get("url")
    if species_url:
        fill_species(species_url, pokemon)

    return pokemon

def fill_types(types_data, pokemon):
    types = []
    no_damage_to = []
    no_damage_from = []
    strong_against = []
    weak_against = []

    for type_entry in types_data:
        type_info = type_entry["type"]
        type_name = type_info["name"]
        types.append(type_name)

        type_response = requests.get(type_info["url"]).json()
        damage_rel = type_response.get("damage_relations", {})

        strong_against.extend([t["name"] for t in damage_rel.get("double_damage_to", [])])
        weak_against.extend([t["name"] for t in damage_rel.get("double_damage_from", [])])
        no_damage_to.extend([t["name"] for t in damage_rel.get("no_damage_to", [])])
        no_damage_from.extend([t["name"] for t in damage_rel.get("no_damage_from", [])])

    # Join everything with ;
    pokemon["types"] = ";".join(types)
    pokemon["strongAgainst"] = ";".join(strong_against)
    pokemon["weakAgainst"] = ";".join(weak_against)
    pokemon["noDamageTo"] = ";".join(no_damage_to)
    pokemon["noDamageFrom"] = ";".join(no_damage_from)

def fill_species(url, pokemon):
    response = requests.get(url).json()
    pokemon["evolvesFrom"] = (response.get("evolves_from_species") or {}).get("name", "")

    flavor_entries = response.get("flavor_text_entries", [])
    flavor_texts = [entry["flavor_text"] for entry in flavor_entries if entry["language"]["name"] == "es"]
    pokemon["flavor"] = ";".join(set(flavor_texts))  # sin duplicados

    evo_chain_url = response.get("evolution_chain", {}).get("url")
    if evo_chain_url:
        fill_evolution(evo_chain_url, pokemon, pokemon["name"])

def fill_evolution(url, pokemon, current_name):
    try:
        response = requests.get(url).json()
        chain = response.get("chain", {})
        evo1 = chain.get("evolves_to", [])
        if evo1:
            second = evo1[0]["species"]["name"]
            evo2 = evo1[0].get("evolves_to", [])
            third = evo2[0]["species"]["name"] if evo2 else None
        else:
            second = None
            third = None

        # Validación similar a la que hacías en Kotlin
        pokemon["evolvesTo"] = third if third and third != current_name else (second if second and second != current_name else "")
    except Exception as e:
        print(f"Error obteniendo evolución: {e}")
