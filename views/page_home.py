"""Home / landing page."""

from __future__ import annotations

import streamlit as st

from lib import storage, ui


def _stat(label: str, value) -> None:
    st.markdown(
        f"""<div class="magic-card stat-card" style="text-align:center;">
        <h4>{ui.esc(value)}</h4>
        <p>{ui.esc(label)}</p></div>""",
        unsafe_allow_html=True,
    )


def _nav_button(label: str, page: str, primary: bool = False) -> None:
    if st.button(label, type="primary" if primary else "secondary", use_container_width=True, key=f"home_{page}_{label}"):
        st.session_state["page"] = page
        st.rerun()


def _nav_card(icon: str, title: str, body: str, page: str) -> None:
    st.markdown(
        f"""<div class="magic-card nav-card">
        <div class="nav-icon">{ui.esc(icon)}</div>
        <h4>{ui.esc(title)}</h4>
        <p>{ui.esc(body)}</p>
        </div>""",
        unsafe_allow_html=True,
    )
    _nav_button(f"Open {title}", page)


def render() -> None:
    st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
    col_text, col_img = st.columns([1.15, .85], vertical_alignment="center")
    with col_text:
        st.markdown('<span class="hero-kicker">✨ Grimoire-inspired storytelling platform</span>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Every story is a spell.</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="hero-subtitle">Inkverse gives writers a cinematic home for original fiction, fan fiction, shared universes, short-film showcases, demo profiles, and offline originality checks — a little Black Clover grandeur, softened with Iruma-kun mischief.</p>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            _nav_button("✍️ Start writing", "Write & publish", True)
        with c2:
            _nav_button("📖 Explore stories", "Explore stories")
        with c3:
            _nav_button("🎬 Watch films", "Short films")
    with col_img:
        if ui.asset_exists("assets/hero.png"):
            st.image("assets/hero.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    stories = storage.read_collection("stories")
    films = storage.read_collection("films")
    universes = storage.read_collection("universes")
    users = storage.read_collection("users")

    st.write("")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        _stat("Published stories", len([s for s in stories if s.get("status") == "published"]))
    with s2:
        _stat("Shared universes", len(universes))
    with s3:
        _stat("Short films", len(films))
    with s4:
        _stat("Demo writers", len(users))

    ui.section("Choose your portal")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        _nav_card("📖", "Story Archive", "Browse published tales and fan fiction.", "Explore stories")
    with p2:
        _nav_card("✍️", "Writer Desk", "Draft, check, and publish new work.", "Write & publish")
    with p3:
        _nav_card("🌌", "World Atlas", "Explore shared universes and canon rules.", "Shared universes")
    with p4:
        _nav_card("🎬", "Film Hall", "Watch short-film adaptations.", "Short films")

    ui.section("Featured seed stories")
    featured = [s for s in stories if s.get("status") == "published"][:3]
    cols = st.columns(3)
    for col, story in zip(cols, featured):
        with col:
            if ui.asset_exists(story.get("cover")):
                st.image(story.get("cover"), use_container_width=True)
            st.markdown(
                f"""<div class="magic-card">
                <h4>{ui.esc(story.get('title'))}</h4>
                <p>by <strong>{ui.esc(story.get('author_name'))}</strong></p>
                <p>{ui.esc((story.get('synopsis') or '')[:170])}...</p>
                </div>""",
                unsafe_allow_html=True,
            )

    ui.section("Why Inkverse exists")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            """<div class="magic-card">
            <h4>Problem 1 — Writers need a stage</h4>
            <p>Publishing routes are narrow and slow. Inkverse lets writers publish,
            build an audience, and retain creative control over their work.</p></div>""",
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            """<div class="magic-card">
            <h4>Problem 2 — Copyright anxiety is real</h4>
            <p>The checker uses local text recognition: TF-IDF similarity, n-gram phrase
            overlap, and fuzzy matching. It does not call OpenAI.</p></div>""",
            unsafe_allow_html=True,
        )

    ui.section("How it works")
    h1, h2, h3 = st.columns(3)
    steps = [
        ("1. Sign in", "Use a demo account or create your own. Avatars included."),
        ("2. Write or collaborate", "Publish solo, join universes, or add lore to the wiki."),
        ("3. Check & publish", "Run offline originality checks before sharing your work."),
    ]
    for col, (title, body) in zip([h1, h2, h3], steps):
        with col:
            st.markdown(f'<div class="magic-card"><h4>{ui.esc(title)}</h4><p>{ui.esc(body)}</p></div>', unsafe_allow_html=True)
