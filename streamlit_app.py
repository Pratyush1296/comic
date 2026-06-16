"""
Inkverse — main Streamlit application.

A colorful, open-source collaborative storytelling platform where writers can
publish fiction, collaborate on universes, showcase short films, and run an
offline text-recognition originality check before publishing.
"""

from __future__ import annotations

import streamlit as st

from lib import seed, ui
from views import (
    page_account,
    page_copyright,
    page_explore,
    page_films,
    page_home,
    page_legal,
    page_universes,
    page_write,
)

st.set_page_config(
    page_title="Inkverse — stories, universes & short films",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

ui.inject_css()
seed.ensure_seeded()

PAGES = {
    "Home": page_home.render,
    "Explore stories": page_explore.render,
    "Write & publish": page_write.render,
    "Shared universes": page_universes.render,
    "Short films": page_films.render,
    "Copyright check": page_copyright.render,
    "Legal & IP": page_legal.render,
    "Account": page_account.render,
}

NAV_ICONS = {
    "Home": "🏰",
    "Explore stories": "📖",
    "Write & publish": "✍️",
    "Shared universes": "🌌",
    "Short films": "🎬",
    "Copyright check": "🛡️",
    "Legal & IP": "⚖️",
    "Account": "🪄",
}


def go_to(page_name: str) -> None:
    """Navigate to a page from buttons/cards."""
    if page_name in PAGES:
        st.session_state["page"] = page_name
        st.rerun()


def sidebar() -> str:
    with st.sidebar:
        ui.brand_header()
        st.divider()

        user = st.session_state.get("user")
        if user:
            ui.avatar(user.get("avatar"), size=64)
            st.success(f"Signed in as **{user['display_name']}**")
        else:
            st.info("Browsing as a guest. Sign in to publish.")

        if "page" not in st.session_state or st.session_state["page"] not in PAGES:
            st.session_state["page"] = "Home"

        st.caption("Navigate")
        for page_name in PAGES:
            active = page_name == st.session_state["page"]
            label = f"{NAV_ICONS.get(page_name, '✦')}  {page_name}"
            if st.button(label, key=f"nav_{page_name}", type="primary" if active else "secondary", use_container_width=True):
                go_to(page_name)

        st.divider()
        from lib import storage
        from lib.copyright_checker import engine_name

        st.caption("System status")
        st.write("Storage:", "GitHub" if storage.github_enabled() else "Local demo")
        st.write("Originality:", "Offline text recognition")
        st.caption(engine_name())
    return st.session_state["page"]


def main() -> None:
    choice = sidebar()
    PAGES[choice]()


if __name__ == "__main__":
    main()
