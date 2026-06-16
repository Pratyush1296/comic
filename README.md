# Inkverse

A colorful Streamlit storytelling app for publishing fiction, collaborating on shared universes, showcasing short-film adaptations, and checking originality with an offline text-recognition engine.

## What is included

- Working homepage buttons that navigate to the correct Streamlit pages.
- Reliable image rendering for hero art, covers, banners, and profile avatars.
- Seed stories, universes, films, wiki/lore entries, and demo author accounts.
- Offline copyright/originality checking using TF-IDF, n-gram phrase overlap, and fuzzy matching.
- No OpenAI dependency or API key required.
- Local JSON storage by default, with optional GitHub-backed persistence.

## Demo login accounts

All demo accounts use this password:

```text
inkverse-demo
```

Usernames:

```text
ariavale
finnmarsh
miraokonkwo
jasperlin
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The first app run automatically seeds local demo data in `local_data/` if the store is empty.

## Optional GitHub persistence

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your GitHub token/repo settings. If you do not configure GitHub, the app will use local JSON files.

## Project structure

```text
streamlit_app.py          # Main app + multipage navigation
lib/auth.py               # Demo/signup/login logic with bcrypt
lib/copyright_checker.py  # Offline text-recognition originality checker
lib/seed.py               # Seed data: users, stories, universes, films, wiki
lib/storage.py            # Local/GitHub JSON storage
lib/ui.py                 # Shared CSS, cards, badges, image helpers
views/                    # Page modules
assets/                   # Avatars, covers, hero, world images
```

## Notes

The copyright checker is an educational early-warning tool, not legal advice. For serious IP decisions, consult a qualified attorney.
