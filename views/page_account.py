"""Account — sign up, sign in, profile."""

from __future__ import annotations

import streamlit as st

from lib import auth, storage, ui

DEMO_PASSWORD = "inkverse-demo"


def render() -> None:
    ui.section("Account")

    user = auth.current_user()
    if user:
        _profile(user)
        return

    st.markdown("#### Demo accounts")
    demo_users = [u for u in storage.read_collection("users") if u.get("username") in {"ariavale", "finnmarsh", "miraokonkwo", "jasperlin"}]
    cols = st.columns(4)
    for col, demo in zip(cols, demo_users):
        with col:
            ui.avatar(demo.get("avatar"), 74)
            st.markdown(f"**{demo.get('display_name')}**  \n`{demo.get('username')}`")
    st.info(f"All demo accounts use password: `{DEMO_PASSWORD}`")

    tab_login, tab_signup = st.tabs(["Sign in", "Create account"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="ariavale")
            password = st.text_input("Password", type="password", placeholder=DEMO_PASSWORD)
            submitted = st.form_submit_button("Sign in", type="primary")
        if submitted:
            ok, msg = auth.login(username, password)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()

    with tab_signup:
        with st.form("signup_form"):
            display_name = st.text_input("Display name")
            new_username = st.text_input("Username (3-24 chars: letters, numbers, _)")
            bio = st.text_area("Short bio (optional)", height=80)
            new_password = st.text_input("Password (min 6 chars)", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", type="primary")
        if submitted:
            if new_password != confirm:
                st.error("Passwords do not match.")
            else:
                ok, msg = auth.signup(new_username, new_password, display_name, bio)
                (st.success if ok else st.error)(msg)


def _profile(user: dict) -> None:
    c1, c2 = st.columns([.15, .85], vertical_alignment="center")
    with c1:
        ui.avatar(user.get("avatar"), 96)
    with c2:
        st.markdown(
            f"""<div class="ink-card">
            <h4>{user['display_name']}</h4>
            <p>@{user['username']}</p>
            <p>{user.get('bio') or 'No bio yet.'}</p>
            </div>""",
            unsafe_allow_html=True,
        )

    stories = storage.find_many("stories", author_id=user["id"])
    published = [s for s in stories if s.get("status") == "published"]
    films = storage.find_many("films", uploader_id=user["id"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Published stories", len(published))
    c2.metric("Drafts", len(stories) - len(published))
    c3.metric("Films added", len(films))

    if st.button("Sign out"):
        auth.logout()
        st.rerun()
