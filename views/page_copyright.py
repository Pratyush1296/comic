"""Standalone local text-recognition copyright / originality checker (Problem 2)."""

from __future__ import annotations

import streamlit as st

from lib import ui
from lib.copyright_checker import check_draft, engine_name, reference_works


def render() -> None:
    ui.section("Copyright & originality check")
    st.caption(
        "Paste a draft to scan it against a database of known works and community "
        "stories. Local text recognition flags overlapping phrases, verbatim "
        "passages, and lexical similarity so you can avoid accidental infringement "
        "before you publish."
    )

    st.success(f"Originality engine ready and runs fully offline — {engine_name()}.")
    st.info("This checker does **not** use OpenAI. It recognizes text overlap using TF-IDF, shared n-grams, and fuzzy matching against the seeded reference database plus community stories.")

    draft = st.text_area(
        "Your draft or synopsis",
        height=280,
        placeholder="Paste the text you want to check...",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        top_k = st.slider("How many top matches to analyze", 1, 5, 3)
    with c2:
        threshold = st.slider("Similarity sensitivity", 0.05, 0.60, 0.10, 0.05)

    if st.button("Run originality check", type="primary", disabled=not draft):
        with st.spinner("Recognizing shared text against the reference database..."):
            result = check_draft(draft, top_k=top_k, threshold=threshold)
        st.session_state["copyright_result"] = result

    result = st.session_state.get("copyright_result")
    if result:
        if result.get("message"):
            st.info(result["message"])

        st.markdown(
            "### Overall risk: " + ui.risk_chip(result.get("overall_risk", "none")),
            unsafe_allow_html=True,
        )

        for cand in result.get("candidates", []):
            analysis = cand.get("analysis", {})
            scores = analysis.get("scores", {})
            st.markdown(
                f"""<div class="ink-card">
                <h4>{cand.get('title')} <span style="font-size:0.8rem;color:#6B7280;">
                by {cand.get('author')}</span></h4>
                <p>Lexical similarity: <strong>{cand.get('similarity')}</strong> ·
                Source: {cand.get('source', 'reference')}</p>
                </div>""",
                unsafe_allow_html=True,
            )
            st.markdown(ui.risk_chip(analysis.get("risk_level", "low")), unsafe_allow_html=True)
            st.write(analysis.get("similarity_explanation", ""))

            if scores:
                m1, m2, m3 = st.columns(3)
                m1.metric("TF-IDF cosine", scores.get("tfidf_cosine", 0))
                m2.metric("Phrase overlap", scores.get("ngram_overlap", 0))
                m3.metric("Verbatim block", scores.get("fuzzy_block", 0))

            if analysis.get("overlaps"):
                st.markdown("**Recognized overlaps to review**")
                for o in analysis["overlaps"]:
                    st.markdown(f"- {o}")
            if analysis.get("common_tropes"):
                st.markdown("**Common tropes (not infringement)**")
                for t in analysis["common_tropes"]:
                    st.markdown(f"- {t}")
            if analysis.get("recommendation"):
                st.success(analysis["recommendation"])
            st.divider()

        st.caption(
            "This tool offers automated guidance and is not legal advice. For "
            "high-risk findings, consult a qualified IP attorney."
        )

    with st.expander("What's in the reference database?"):
        works = reference_works()
        st.write(
            f"Comparing against **{len(works)}** works "
            "(public-domain seeds + community stories)."
        )
        for w in works:
            st.markdown(f"- **{w.get('title')}** — {w.get('author')} ({w.get('source', '')})")
