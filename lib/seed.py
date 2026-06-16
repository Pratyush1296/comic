"""
seed.py
=======
Seeds the JSON store with rich starter content the first time the app runs:
authors (with illustrated avatars), published stories (with cover art), shared
universes, short-film adaptations, and a worldbuilding wiki.

All art is bundled in /assets and referenced by relative path, so the demo looks
complete out of the box even with an empty (local) data store. Seeding is
idempotent: each collection is only populated if it is currently empty.
"""

from __future__ import annotations

from datetime import datetime, timezone

from lib import storage

# Illustrated avatars bundled with the app, used to give new accounts a face.
AVATAR_POOL = [
    "assets/avatars/avatar-aria.png",
    "assets/avatars/avatar-finn.png",
    "assets/avatars/avatar-mira.png",
    "assets/avatars/avatar-jasper.png",
]


def _ts(day: int) -> str:
    return datetime(2024, 6, day, 12, 0, tzinfo=timezone.utc).isoformat()


# --------------------------------------------------------------------------- #
# Authors
# --------------------------------------------------------------------------- #
AUTHORS = [
    {
        "id": "seed-author-aria",
        "username": "ariavale",
        "display_name": "Aria Vale",
        "bio": "Maps imaginary coastlines for a living. Founder of the Aetheria universe.",
        "avatar": "assets/avatars/avatar-aria.png",
    },
    {
        "id": "seed-author-finn",
        "username": "finnmarsh",
        "display_name": "Finn Marsh",
        "bio": "Writes quiet stories about the sea and the people who keep its lights on.",
        "avatar": "assets/avatars/avatar-finn.png",
    },
    {
        "id": "seed-author-mira",
        "username": "miraokonkwo",
        "display_name": "Mira Okonkwo",
        "bio": "Astronomer by day, science-fiction poet by night.",
        "avatar": "assets/avatars/avatar-mira.png",
    },
    {
        "id": "seed-author-jasper",
        "username": "jasperlin",
        "display_name": "Jasper Lin",
        "bio": "Brews mysteries and the occasional potion. Steward of the Verdance world.",
        "avatar": "assets/avatars/avatar-jasper.png",
    },
]


# --------------------------------------------------------------------------- #
# Stories
# --------------------------------------------------------------------------- #
STORIES = [
    {
        "id": "seed-story-cartographer",
        "title": "The Cartographer of Forgotten Seas",
        "author_id": "seed-author-aria",
        "author_name": "Aria Vale",
        "author_avatar": "assets/avatars/avatar-aria.png",
        "cover": "assets/covers/cover-cartographer.png",
        "genres": ["Fantasy", "Adventure"],
        "universe_name": "Aetheria",
        "synopsis": (
            "When every map of the floating isles burns in a single night, a young "
            "cartographer must redraw the world from memory and starlight before the "
            "sky-routes are lost forever."
        ),
        "body": (
            "Elowen had drawn the floating isles a thousand times, but never from memory. "
            "The night the Great Archive burned, she stood on the harbor bridge and watched "
            "centuries of charts curl into embers that rose like reluctant fireflies.\n\n"
            "By morning, the airships had no routes. Captains who had crossed the cloud-sea "
            "for decades suddenly feared the gaps between islands, where the wind turned "
            "treacherous and the mist swallowed sound. The Cartographers' Guild called it the "
            "end of safe passage. Elowen called it a problem worth solving.\n\n"
            "She began with the constellations, because stars do not burn the way paper does. "
            "Each night she rowed her little skiff to the edge of the world and matched the "
            "reflections on the calm water to the shapes she remembered. Slowly, island by "
            "island, the map returned, not as it had been, but truer, drawn by someone who had "
            "finally learned to trust her own hands."
        ),
        "status": "published",
        "created_at": _ts(2),
    },
    {
        "id": "seed-story-lighthouse",
        "title": "Tea for the Lighthouse Keeper",
        "author_id": "seed-author-finn",
        "author_name": "Finn Marsh",
        "author_avatar": "assets/avatars/avatar-finn.png",
        "cover": "assets/covers/cover-lighthouse.png",
        "genres": ["Drama"],
        "universe_name": None,
        "synopsis": (
            "Every evening at dusk, the keeper sets a second cup on the rocks for a friend who "
            "has not come in years. A gentle story about grief, routine, and the slow return "
            "of hope."
        ),
        "body": (
            "The kettle whistled at six, the way it had for thirty-one years. Aldous poured two "
            "cups, carried them down the worn stone steps, and set one on the flat rock where "
            "Margery used to sit.\n\n"
            "\"Calm tonight,\" he told the empty seat. The sea agreed, lapping politely at the "
            "base of the lighthouse. He drank his tea slowly and let the other go cold, as he "
            "always did, then climbed back up to light the lamp.\n\n"
            "It was a girl from the village who broke the habit. She rowed out one evening, "
            "uninvited, and sat on Margery's rock as though it had been waiting for her. \"Is "
            "this seat taken?\" she asked. Aldous looked at the cooling cup, then at the living "
            "face in front of it, and decided that keeping a light meant more than warning ships "
            "away. Sometimes it meant guiding someone in."
        ),
        "status": "published",
        "created_at": _ts(4),
    },
    {
        "id": "seed-story-signal",
        "title": "Signal in the Static",
        "author_id": "seed-author-mira",
        "author_name": "Mira Okonkwo",
        "author_avatar": "assets/avatars/avatar-mira.png",
        "cover": "assets/covers/cover-signal.png",
        "genres": ["Science Fiction"],
        "universe_name": None,
        "synopsis": (
            "A lonely radio astronomer finally hears the signal she has waited her whole career "
            "for, only to realize it is a message she sent herself, long ago and not yet."
        ),
        "body": (
            "The dish had listened to empty sky for forty years. Dr. Ada Boakye had listened to "
            "the dish for twelve of them, long enough to know the difference between noise and "
            "nothing.\n\n"
            "At 3:14 in the morning, the static folded. A pattern surfaced, prime numbers, then "
            "a waveform that resolved into something almost like speech. Ada's hands shook as she "
            "logged it. First contact, alone, on a Tuesday.\n\n"
            "It took her three weeks to decode the message and one terrible second to recognize "
            "the voice. It was hers, older and calmer, transmitting coordinates and a single "
            "instruction: keep listening. The signal had not come from across the galaxy. It had "
            "come from across time, and it was counting on her to answer."
        ),
        "status": "published",
        "created_at": _ts(6),
    },
    {
        "id": "seed-story-apothecary",
        "title": "The Midnight Apothecary",
        "author_id": "seed-author-jasper",
        "author_name": "Jasper Lin",
        "author_avatar": "assets/avatars/avatar-jasper.png",
        "cover": "assets/covers/cover-apothecary.png",
        "genres": ["Mystery", "Fantasy"],
        "universe_name": "Verdance",
        "synopsis": (
            "In the living tree-city of Verdance, a shop that only opens at midnight sells cures "
            "for ailments no doctor can name, until a customer asks for a remedy that does not "
            "exist."
        ),
        "body": (
            "The Midnight Apothecary had no sign, because the people who needed it always found "
            "it anyway. Its shelves climbed the inside of a hollow tree, lined with bottles that "
            "glowed faintly in colors that had no names.\n\n"
            "Wren had inherited the shop from her grandmother along with a single rule: never "
            "promise a cure you cannot brew. For years that had been easy. Then a hooded stranger "
            "set a coin on the counter and asked for a remedy to forget a face.\n\n"
            "Wren searched every drawer and ledger and found nothing, because forgetting, her "
            "grandmother had written in the margin, is not a sickness but a choice. So instead of "
            "a potion, Wren brewed a pot of tea, and asked the stranger to tell her the story they "
            "were so desperate to lose. By dawn, the face they feared had become one they could "
            "finally carry."
        ),
        "status": "published",
        "created_at": _ts(8),
    },
    {
        "id": "seed-story-comet",
        "title": "Letters to a Comet",
        "author_id": "seed-author-mira",
        "author_name": "Mira Okonkwo",
        "author_avatar": "assets/avatars/avatar-mira.png",
        "cover": "assets/covers/cover-comet.png",
        "genres": ["Romance", "Poetry"],
        "universe_name": None,
        "synopsis": (
            "A collection of letters written to a comet that returns once every eighty years, "
            "and to the person the writer hopes will read them when it does."
        ),
        "body": (
            "Dear traveler of the long dark,\n\n"
            "They say you will not pass this way again for eighty years. I am writing anyway, "
            "because some things are worth saying even to a light that cannot answer.\n\n"
            "I climbed the hill again tonight. The grass remembered me. I told the sky the things "
            "I could not tell anyone with a face, and the comet listened the way only distant "
            "things can, patiently, without flinching.\n\n"
            "If you are reading this, then eighty years have passed and the comet has come round "
            "again, and someone, maybe you, is standing on my hill. Leave a letter of your own. "
            "Tell it everything. I promise the sky keeps every word."
        ),
        "status": "published",
        "created_at": _ts(10),
    },
]


# --------------------------------------------------------------------------- #
# Shared universes
# --------------------------------------------------------------------------- #
UNIVERSES = [
    {
        "id": "seed-universe-aetheria",
        "name": "Aetheria",
        "tagline": "A sky-sea of floating isles connected by wind-routes and starlight.",
        "rules": (
            "Setting: a world of islands suspended in an endless cloud-sea, traveled by airship "
            "and sky-current. Canon: gravity is gentle, the stars are navigational law, and the "
            "Great Archive (recently burned) once held every map. Contributors may add new isles "
            "and crews but may not alter the laws of flight or resurrect the Archive intact."
        ),
        "creator_id": "seed-author-aria",
        "creator_name": "Aria Vale",
        "banner": "assets/wiki/world-aetheria.png",
        "created_at": _ts(1),
    },
    {
        "id": "seed-universe-archive",
        "name": "The Sunken Archive",
        "tagline": "A drowned library where every book ever lost eventually washes up.",
        "rules": (
            "Setting: a vast flooded library beneath the waves, lit by bioluminescent lanterns. "
            "Canon: knowledge is currency, water preserves rather than destroys, and the Archive "
            "rearranges itself nightly. Contributors may invent recovered texts and librarian "
            "guilds but must respect that nothing here is ever truly permanent."
        ),
        "creator_id": "seed-author-finn",
        "creator_name": "Finn Marsh",
        "banner": "assets/wiki/world-archive.png",
        "created_at": _ts(3),
    },
    {
        "id": "seed-universe-verdance",
        "name": "Verdance",
        "tagline": "A city grown, not built, from ancient living trees.",
        "rules": (
            "Setting: a metropolis cultivated within colossal sentient trees, lit by lantern-fruit. "
            "Canon: the trees remember everything that happens in their branches, magic is grown "
            "rather than cast, and the seasons govern law. Contributors may add districts, guilds, "
            "and growers but may not cut a living tree without consequence."
        ),
        "creator_id": "seed-author-jasper",
        "creator_name": "Jasper Lin",
        "banner": "assets/wiki/world-verdance.png",
        "created_at": _ts(5),
    },
]


# --------------------------------------------------------------------------- #
# Short films
# --------------------------------------------------------------------------- #
FILMS = [
    {
        "id": "seed-film-cartographer",
        "title": "The Cartographer — A Short Film",
        "story_id": "seed-story-cartographer",
        "story_title": "The Cartographer of Forgotten Seas",
        "director": "Aria Vale & the Aetheria Collective",
        "url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ",
        "description": "A wordless animated adaptation of the burning of the Great Archive.",
        "uploader_id": "seed-author-aria",
        "uploader_name": "Aria Vale",
        "created_at": _ts(11),
    },
    {
        "id": "seed-film-signal",
        "title": "Signal — Proof of Concept",
        "story_id": "seed-story-signal",
        "story_title": "Signal in the Static",
        "director": "Mira Okonkwo",
        "url": "https://www.youtube.com/watch?v=eRsGyueVLvQ",
        "description": "A three-minute teaser shot in a real radio observatory at night.",
        "uploader_id": "seed-author-mira",
        "uploader_name": "Mira Okonkwo",
        "created_at": _ts(12),
    },
]


# Replace stale/broken seed video links in already-created data stores.
# Important: _seed_collection() is idempotent, so changing FILMS above will not
# update an existing local_data/films.json or GitHub data/films.json by itself.
VIDEO_URL_FIXES = {
    "https://www.youtube.com/watch?v=BHACKCNDMW8": "https://www.youtube.com/watch?v=eRsGyueVLvQ",
}


def _repair_seed_video_urls() -> None:
    films = storage.read_collection("films")
    changed = False
    for film in films:
        url = film.get("url")
        if url in VIDEO_URL_FIXES:
            film["url"] = VIDEO_URL_FIXES[url]
            changed = True
    if changed:
        storage.write_collection("films", films)


# --------------------------------------------------------------------------- #
# Worldbuilding wiki
# --------------------------------------------------------------------------- #
WIKI = [
    {
        "id": "seed-wiki-aetheria",
        "kind": "World",
        "title": "Aetheria",
        "universe": "Aetheria",
        "image": "assets/wiki/world-aetheria.png",
        "summary": "The floating sky-sea where the saga of the cartographers unfolds.",
        "body": (
            "Aetheria is a world without ground. Hundreds of islands drift in a luminous "
            "cloud-sea, held aloft by a gentle gravity no scholar has fully explained. Travel "
            "between isles depends on the wind-routes — invisible currents charted over "
            "generations and, until recently, recorded in the Great Archive. The burning of "
            "that Archive is the founding wound of the modern age, and the reason mapmakers are "
            "once again the most important people in the sky."
        ),
        "tags": ["floating isles", "airships", "wind-routes", "starlight navigation"],
        "created_at": _ts(1),
    },
    {
        "id": "seed-wiki-archive",
        "kind": "World",
        "title": "The Sunken Archive",
        "universe": "The Sunken Archive",
        "image": "assets/wiki/world-archive.png",
        "summary": "A drowned library that collects everything the surface world loses.",
        "body": (
            "Beneath the waves lies a library larger than any city, lit by lanterns that glow "
            "without flame. The Sunken Archive does not burn, rot, or forget — instead it "
            "rearranges itself each night, so that no two visits are ever the same. Lost letters, "
            "forbidden maps, and forgotten songs all eventually settle onto its shelves. The "
            "librarians who tend it trade in knowledge, the only currency that holds value this "
            "far below the light."
        ),
        "tags": ["underwater", "library", "lost texts", "bioluminescence"],
        "created_at": _ts(3),
    },
    {
        "id": "seed-wiki-verdance",
        "kind": "World",
        "title": "Verdance",
        "universe": "Verdance",
        "image": "assets/wiki/world-verdance.png",
        "summary": "A living tree-city that remembers everything beneath its branches.",
        "body": (
            "Verdance was never constructed; it was grown. Its streets are root and branch, its "
            "lamps are lantern-fruit, and its tallest towers are simply the oldest trees. The "
            "city is sentient in the slow way of forests — it remembers every promise made in its "
            "shade and every blade drawn against its bark. Magic here is cultivated like a crop, "
            "and the seasons carry the weight of law."
        ),
        "tags": ["living city", "ancient trees", "grown magic", "lantern-fruit"],
        "created_at": _ts(5),
    },
    {
        "id": "seed-wiki-elowen",
        "kind": "Character",
        "title": "Elowen, the Memory Cartographer",
        "universe": "Aetheria",
        "image": "assets/wiki/char-keeper.png",
        "summary": "The young mapmaker who redrew Aetheria from starlight after the fire.",
        "body": (
            "Elowen was an apprentice the night the Great Archive burned, too junior to be blamed "
            "and too stubborn to despair. Where the Guild saw the end of safe passage, she saw a "
            "blank page. By rowing to the edge of the world each night and matching the stars to "
            "the islands she remembered, she rebuilt the wind-routes one constellation at a time. "
            "Her charts are now considered more accurate than the originals, because they were "
            "drawn by someone who learned to trust her own hands."
        ),
        "tags": ["protagonist", "cartographer", "Aetheria", "starlight"],
        "created_at": _ts(2),
    },
    {
        "id": "seed-wiki-windroutes",
        "kind": "Lore",
        "title": "The Wind-Routes",
        "universe": "Aetheria",
        "image": "assets/wiki/world-aetheria.png",
        "summary": "The invisible currents that make travel between the floating isles possible.",
        "body": (
            "The wind-routes are not roads but rivers of air, shifting slowly with the seasons. A "
            "captain who strays from a route risks the dead-zones between isles, where the mist "
            "muffles sound and the gravity grows uncertain. For centuries the routes were canon "
            "law, recorded and updated in the Great Archive. Since the fire, they survive only in "
            "the memories of old captains and in Elowen's redrawn charts."
        ),
        "tags": ["lore", "navigation", "Aetheria", "canon"],
        "created_at": _ts(2),
    },
    {
        "id": "seed-wiki-lanternfruit",
        "kind": "Lore",
        "title": "Lantern-Fruit",
        "universe": "Verdance",
        "image": "assets/wiki/world-verdance.png",
        "summary": "The glowing fruit that lights the living city of Verdance.",
        "body": (
            "Lantern-fruit ripen only at dusk, swelling with a soft golden light that lasts until "
            "dawn. Verdance is illuminated entirely by them; lamplighters are really orchard-keepers, "
            "and a street's brightness is a measure of how well its trees are loved. The fruit cannot "
            "be picked without dimming — light, in Verdance, must be tended, never hoarded."
        ),
        "tags": ["lore", "Verdance", "light", "flora"],
        "created_at": _ts(5),
    },
]


# --------------------------------------------------------------------------- #
# Seeding
# --------------------------------------------------------------------------- #
def _seed_collection(name: str, rows: list[dict]) -> None:
    if not storage.read_collection(name):
        storage.write_collection(name, rows)


def _build_users() -> list[dict]:
    # Seed authors as real accounts (with a shared demo password) so their work
    # is owned by a logged-in-capable user. Password hashing is done lazily to
    # avoid importing bcrypt unless we actually seed.
    import bcrypt

    demo_hash = bcrypt.hashpw(b"inkverse-demo", bcrypt.gensalt()).decode("utf-8")
    users = []
    for a in AUTHORS:
        users.append(
            {
                **a,
                "password_hash": demo_hash,
                "created_at": _ts(1),
            }
        )
    return users


def ensure_seeded() -> None:
    """Populate every core collection on first run. Safe to call repeatedly."""
    _seed_collection("users", _build_users())
    _seed_collection("stories", STORIES)
    _seed_collection("universes", UNIVERSES)
    _seed_collection("films", FILMS)
    _repair_seed_video_urls()
    _seed_collection("wiki", WIKI)
