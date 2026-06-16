"""Short-film adaptations — upload (link) & showcase."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import streamlit as st

from lib import auth, storage, ui


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_video_url(url: str) -> bool:
    parsed = urlparse(url or "")
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _normalise_video_url(url: str) -> str:
    """Return a Streamlit-friendly YouTube/Vimeo URL when possible."""
    url = (url or "").strip()
    if not url:
        return url
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")

    if host == "youtu.be":
        video_id = parsed.path.strip("/")
        return f"https://www.youtube.com/watch?v={video_id}" if video_id else url

    if host in {"youtube.com", "m.youtube.com"}:
        if parsed.path.startswith("/embed/") or parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/")[2] if len(parsed.path.split("/")) > 2 else ""
            return f"https://www.youtube.com/watch?v={video_id}" if video_id else url
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        return f"https://www.youtube.com/watch?v={video_id}" if video_id else url

    return url


def render() -> None:
    ui.section("Short films")
    st.caption(
        "A cinematic hall for adaptations, proof-of-concepts, trailers, and visual sparks. "
        "Paste a YouTube or Vimeo link and connect it to the original work."
    )

    user = auth.current_user()
    stories = [s for s in storage.read_collection("stories") if s.get("status") == "published"]
    story_map = {f"{s.get('title')} — {s.get('author_name')}": s.get("id") for s in stories}

    with st.expander("Add a short film", expanded=False):
        if not user:
            st.info("Sign in to add a film.")
        elif not stories:
            st.info("Publish a story first — films are linked to a published work.")
        else:
            f_title = st.text_input("Film title")
            f_story = st.selectbox("Based on which story?", list(story_map.keys()))
            f_director = st.text_input("Director / creator")
            f_url = st.text_input("Video link (YouTube, Vimeo, etc.)")
            f_desc = st.text_area("Description", height=80)
            clean_url = _normalise_video_url(f_url)
            valid = bool(f_title and _is_video_url(clean_url))
            if f_url and not _is_video_url(clean_url):
                st.warning("Please enter a valid http(s) video URL.")
            if f_url and clean_url != f_url.strip():
                st.caption(f"This will be saved as: {clean_url}")
            if st.button("Add film", type="primary", disabled=not valid):
                storage.append_document(
                    "films",
                    {
                        "id": uuid.uuid4().hex,
                        "title": f_title.strip(),
                        "story_id": story_map[f_story],
                        "story_title": f_story.split(" — ")[0],
                        "director": f_director.strip(),
                        "url": clean_url,
                        "description": f_desc.strip(),
                        "uploader_id": user["id"],
                        "uploader_name": user["display_name"],
                        "created_at": _now(),
                    },
                )
                st.success("Film added to the showcase.")
                st.rerun()

    films = storage.read_collection("films")
    if not films:
        st.info("No short films yet. Add the first adaptation above!")
        return

    st.markdown(
        f"""<div class="magic-card">
        <h4>🎬 Film Hall</h4>
        <p><strong>{len(films)}</strong> short films in the showcase. Broken/stale seed links are repaired automatically when the app starts.</p>
        </div>""",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, film in enumerate(sorted(films, key=lambda f: f.get("created_at", ""), reverse=True)):
        with cols[i % 2]:
            url = _normalise_video_url(film.get("url", ""))
            st.markdown(
                f"""<div class="magic-card">
                <h4>{ui.esc(film.get('title'))}</h4>
                <p>Adapted from <strong>{ui.esc(film.get('story_title'))}</strong></p>
                <p>Directed by {ui.esc(film.get('director') or 'Unknown')} · added by {ui.esc(film.get('uploader_name'))}</p>
                <p>{ui.esc(film.get('description'))}</p>
                </div>""",
                unsafe_allow_html=True,
            )
            if _is_video_url(url):
                try:
                    st.video(url)
                except Exception:
                    st.warning("This video could not be embedded. Open it directly instead.")
                    st.link_button("Watch the film", url, use_container_width=True)
            else:
                st.error("This film has an invalid video URL.")
