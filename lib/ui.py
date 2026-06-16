"""
Shared UI helpers and Inkverse visual identity.

The visual direction is a magical-library / grimoire interface: mostly dark,
gold, and arcane, with a softer playful glow so the app still feels welcoming
for novice writers.
"""

from __future__ import annotations

import base64
import html
import os

import streamlit as st

GOLD = "#F6C85F"
EMBER = "#FF6B6B"
VIOLET = "#8B5CF6"
AETHER = "#4DD0E1"
INK = "#120B1F"
PARCHMENT = "#FFF7E6"

GENRES = [
    "Fantasy", "Science Fiction", "Mystery", "Romance", "Horror",
    "Adventure", "Drama", "Fan Fiction", "Poetry", "Historical",
]


def esc(value: object) -> str:
    """HTML-escape dynamic content used inside custom Streamlit markup."""
    return html.escape(str(value or ""), quote=True)


def asset_exists(path: str | None) -> bool:
    return bool(path and os.path.exists(path))


def image_data_uri(path: str | None) -> str:
    """Return a base64 data URI so images also work inside custom HTML cards."""
    if not asset_exists(path):
        return ""
    ext = os.path.splitext(path or "")[1].lower().replace(".", "") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    with open(path, "rb") as fh:
        return f"data:image/{mime};base64," + base64.b64encode(fh.read()).decode("ascii")


def avatar(path: str | None, size: int = 72) -> None:
    if asset_exists(path):
        st.image(path, width=size)
    else:
        st.markdown(
            f'<div class="avatar-fallback" style="width:{size}px;height:{size}px;">✦</div>',
            unsafe_allow_html=True,
        )


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --gold: {GOLD}; --ember: {EMBER}; --violet: {VIOLET}; --aether: {AETHER};
            --ink: {INK}; --parchment: {PARCHMENT};
        }}
        .stApp {{
            background:
                radial-gradient(900px 540px at 12% -8%, rgba(139,92,246,.30), transparent 60%),
                radial-gradient(820px 520px at 102% 2%, rgba(246,200,95,.24), transparent 58%),
                radial-gradient(700px 440px at 50% 110%, rgba(77,208,225,.12), transparent 58%),
                linear-gradient(180deg, #0b0713 0%, #130d24 46%, #201437 100%);
            color: #F8EED7;
        }}
        .block-container {{ padding-top: 1.7rem; padding-bottom: 3rem; max-width: 1220px; }}
        section[data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(14,9,26,.96), rgba(30,19,52,.96)),
                radial-gradient(420px 300px at 0% 0%, rgba(246,200,95,.18), transparent);
            border-right: 1px solid rgba(246,200,95,.25);
        }}
        section[data-testid="stSidebar"] * {{ color: #F8EED7; }}
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color: rgba(248,238,215,.78); }}
        h1, h2, h3, h4 {{ color: #FFF7E6; }}
        p, li, label, .stMarkdown {{ color: rgba(248,238,215,.88); }}
        .ink-brand {{
            font-size: 2.35rem; font-weight: 950; letter-spacing: -1.5px; margin: 0;
            background: linear-gradient(90deg, #FFF3B0, var(--gold), var(--aether), #E9D5FF);
            -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
            filter: drop-shadow(0 0 16px rgba(246,200,95,.28));
        }}
        .ink-tag {{ color: rgba(248,238,215,.72); margin-top:-6px; font-size:.94rem; }}
        .hero-shell {{
            position: relative; overflow: hidden; padding: clamp(26px, 5vw, 54px);
            border: 1px solid rgba(246,200,95,.32); border-radius: 34px;
            background:
                radial-gradient(700px 360px at 88% 18%, rgba(246,200,95,.22), transparent 58%),
                radial-gradient(520px 300px at 12% 20%, rgba(139,92,246,.24), transparent 58%),
                linear-gradient(135deg, rgba(255,247,230,.09), rgba(255,255,255,.035));
            box-shadow: 0 30px 90px rgba(0,0,0,.32), inset 0 0 0 1px rgba(255,255,255,.05);
        }}
        .hero-shell:before {{
            content: "✦ ✧ ✦ ✧ ✦"; position:absolute; right:28px; top:18px; color:rgba(246,200,95,.40);
            letter-spacing: 16px; font-size: 1.25rem;
        }}
        .hero-title {{
            font-size: clamp(2.55rem, 6vw, 5.6rem); line-height:.92; font-weight: 950;
            letter-spacing:-3px; color: #FFF7E6; margin:0 0 14px;
            text-shadow: 0 0 28px rgba(246,200,95,.18);
        }}
        .hero-kicker {{
            display:inline-block; padding:7px 14px; border-radius:999px; margin-bottom:14px;
            background:rgba(246,200,95,.13); border:1px solid rgba(246,200,95,.42);
            font-weight:900; color:#FFE9A6;
        }}
        .hero-subtitle {{ max-width: 740px; color:rgba(248,238,215,.86); font-size:1.04rem; }}
        .ink-h2 {{
            font-size:1.55rem; font-weight:950; color:#FFF7E6; margin: 26px 0 14px;
            border-left:7px solid var(--gold); padding-left:13px; letter-spacing:-.5px;
        }}
        .ink-card, .magic-card {{
            background: linear-gradient(180deg, rgba(255,247,230,.105), rgba(255,255,255,.045));
            border:1px solid rgba(246,200,95,.22); border-radius:24px; padding:18px 20px;
            box-shadow:0 18px 48px rgba(0,0,0,.22), inset 0 0 0 1px rgba(255,255,255,.04);
            margin-bottom:16px; backdrop-filter: blur(10px);
        }}
        .ink-card:hover, .magic-card:hover {{
            transform: translateY(-2px); transition: .18s ease;
            border-color: rgba(246,200,95,.46); box-shadow:0 24px 58px rgba(0,0,0,.30), 0 0 28px rgba(246,200,95,.10);
        }}
        .ink-card h4, .magic-card h4 {{ margin:0 0 7px; color:#FFF7E6; font-size:1.18rem; }}
        .ink-card p, .magic-card p {{ margin:0; color:rgba(248,238,215,.78); }}
        .stat-card h4 {{ font-size:2rem; color:#FFE9A6; margin:0; }}
        .nav-card {{ min-height: 150px; }}
        .nav-icon {{ font-size:2rem; margin-bottom:8px; }}
        .story-card {{ display:grid; grid-template-columns:140px 1fr; gap:16px; align-items:start; }}
        .story-cover {{ width:140px; height:190px; object-fit:cover; border-radius:18px; box-shadow:0 12px 30px rgba(0,0,0,.35); border:1px solid rgba(246,200,95,.25); }}
        .avatar-img {{ width:38px; height:38px; object-fit:cover; border-radius:999px; border:2px solid rgba(255,247,230,.9); box-shadow:0 4px 12px rgba(0,0,0,.35); vertical-align:middle; margin-right:8px; }}
        .avatar-fallback {{ display:flex; align-items:center; justify-content:center; border-radius:999px; background:linear-gradient(135deg,var(--gold),var(--violet)); color:#160E26; font-weight:900; }}
        .ink-badge {{ display:inline-block; padding:4px 12px; border-radius:999px; font-size:.78rem; font-weight:900; margin:2px 6px 2px 0; color:#170F24; }}
        .b-coral {{ background:#FF9F8C; }} .b-teal {{ background:#8BE9E0; }} .b-sun {{ background:var(--gold); }} .b-ink {{ background:#D8B4FE; }}
        .risk {{ padding:4px 14px; border-radius:999px; font-weight:900; color:#170F24; }}
        .risk-none {{ background:#8BE9E0; }} .risk-low {{ background:#B5F7A5; }} .risk-medium {{ background:var(--gold); }} .risk-high {{ background:#FF9F8C; }}
        .stButton > button {{
            border-radius:15px; font-weight:900; min-height:2.75rem;
            border:1px solid rgba(246,200,95,.25); background:rgba(255,247,230,.08); color:#FFF7E6;
        }}
        .stButton > button:hover {{ border-color:rgba(246,200,95,.65); color:#FFE9A6; }}
        .stButton > button[kind="primary"] {{
            background:linear-gradient(90deg, #F6C85F, #FF8A65); color:#170F24; border:0;
            box-shadow:0 12px 30px rgba(246,200,95,.18);
        }}
        div[data-testid="stRadio"] label {{ color:#FFF7E6; }}
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
            background-color:rgba(255,247,230,.08); color:#FFF7E6; border-color:rgba(246,200,95,.22);
        }}
        .stTabs [data-baseweb="tab"] {{ font-weight:900; color:#F8EED7; }}
        div[data-testid="stExpander"] {{ border:1px solid rgba(246,200,95,.20); border-radius:18px; background:rgba(255,247,230,.04); }}
        @media(max-width:700px) {{ .story-card {{ grid-template-columns:1fr; }} .story-cover {{ width:100%; height:260px; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def brand_header() -> None:
    st.markdown('<p class="ink-brand">Inkverse</p>', unsafe_allow_html=True)
    st.markdown('<p class="ink-tag">A magical library for stories, universes, and short-film sparks.</p>', unsafe_allow_html=True)


def section(title: str) -> None:
    st.markdown(f'<div class="ink-h2">{esc(title)}</div>', unsafe_allow_html=True)


def genre_badge(genre: str) -> str:
    colors = {0: "b-coral", 1: "b-teal", 2: "b-sun", 3: "b-ink"}
    cls = colors[sum(ord(c) for c in genre) % 4]
    return f'<span class="ink-badge {cls}">{esc(genre)}</span>'


def risk_chip(level: str) -> str:
    level = (level or "none").lower()
    label = {"none": "No risk", "low": "Low risk", "medium": "Medium risk", "high": "High risk"}.get(level, "Unknown")
    return f'<span class="risk risk-{esc(level)}">{esc(label)}</span>'
