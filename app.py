from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "portfolio_content.json"
PDF_PATH = ROOT / "Bewerbung_Tim_Heid_Babelsberg.pdf"


def load_content() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #0b0b0c;
            color: #f0ebe2;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        [data-testid="stSidebar"] {
            background: #111112;
            border-right: 1px solid rgba(198, 178, 142, 0.18);
        }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }
        [data-testid="stToolbar"] {
            right: 1rem;
        }
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 4rem;
            max-width: 1180px;
        }
        h1, h2, h3 {
            color: #f6f0e8;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        .hero-kicker {
            letter-spacing: 0.28em;
            text-transform: uppercase;
            color: #c6b28e;
            font-size: 0.82rem;
            margin-bottom: 0.8rem;
        }
        .hero-title {
            font-size: clamp(2.8rem, 6vw, 5.4rem);
            font-weight: 700;
            line-height: 0.95;
            margin: 0;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            color: rgba(240, 235, 226, 0.78);
            line-height: 1.7;
            max-width: 38rem;
            margin-top: 1.2rem;
        }
        .section-label {
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: #c6b28e;
            font-size: 0.76rem;
            margin-bottom: 0.8rem;
        }
        .surface {
            background: linear-gradient(180deg, rgba(255,255,255,0.025), rgba(255,255,255,0.015));
            border: 1px solid rgba(198, 178, 142, 0.15);
            border-radius: 24px;
            padding: 1.4rem 1.5rem;
        }
        .project-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(198, 178, 142, 0.18);
            border-radius: 24px;
            padding: 1.4rem;
            margin-bottom: 1.2rem;
        }
        .project-title {
            font-size: 1.45rem;
            font-weight: 600;
            margin: 0 0 0.35rem 0;
        }
        .project-meta {
            color: rgba(240, 235, 226, 0.62);
            font-size: 0.92rem;
            margin-bottom: 1rem;
        }
        .project-summary {
            color: rgba(240, 235, 226, 0.86);
            font-size: 1rem;
            line-height: 1.7;
            margin-bottom: 0.9rem;
        }
        .tag {
            display: inline-block;
            padding: 0.36rem 0.7rem;
            border-radius: 999px;
            margin: 0 0.45rem 0.45rem 0;
            background: rgba(198, 178, 142, 0.12);
            border: 1px solid rgba(198, 178, 142, 0.14);
            color: #f0ebe2;
            font-size: 0.82rem;
        }
        .placeholder-visual {
            min-height: 250px;
            border-radius: 24px;
            border: 1px solid rgba(198, 178, 142, 0.18);
            background:
                radial-gradient(circle at top right, rgba(198,178,142,0.24), transparent 30%),
                linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01)),
                #111112;
            display: flex;
            align-items: end;
            padding: 1.2rem;
            color: rgba(240, 235, 226, 0.92);
            font-size: 1.1rem;
        }
        .quote-panel {
            padding: 4rem 2rem;
            border-radius: 28px;
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            border: 1px solid rgba(198, 178, 142, 0.18);
            text-align: center;
        }
        .quote-text {
            font-size: clamp(1.6rem, 3.4vw, 2.4rem);
            line-height: 1.4;
            max-width: 40rem;
            margin: 0 auto;
            color: #f5efe5;
        }
        .muted {
            color: rgba(240, 235, 226, 0.66);
        }
        .contact-label {
            letter-spacing: 0.18em;
            text-transform: uppercase;
            font-size: 0.72rem;
            color: #c6b28e;
            margin-bottom: 0.35rem;
        }
        .contact-value {
            font-size: 1rem;
            color: #f0ebe2;
            line-height: 1.6;
        }
        .small-gap {
            height: 0.6rem;
        }
        a {
            color: #d5c3a1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(content: dict[str, Any]) -> None:
    site = content["site"]
    st.sidebar.markdown(f"### {site['title']}")
    st.sidebar.caption(site["subtitle"])
    st.sidebar.markdown(site["tagline"])
    st.sidebar.divider()
    st.sidebar.markdown("**Inhalt**")
    st.sidebar.markdown("- Hero\n- About\n- Selected Work\n- Skills\n- Statement\n- Contact")
    st.sidebar.divider()
    st.sidebar.markdown("**Readiness**")
    st.sidebar.success("Streamlit stack installed")
    st.sidebar.success("PDF content extracted")
    st.sidebar.success("GitHub remote attached")
    st.sidebar.warning("Email / Instagram still missing")
    st.sidebar.warning("PDF itself contains no embedded project URLs")


def render_hero(content: dict[str, Any]) -> None:
    site = content["site"]
    image_path = ROOT / "assets" / "images" / "cover_still.png"
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        st.markdown('<div class="hero-kicker">Interactive portfolio</div>', unsafe_allow_html=True)
        st.markdown(f'<h1 class="hero-title">{site["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hero-subtitle">{site["subtitle"]}<br><span class="muted">{site["tagline"]}</span></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if PDF_PATH.exists():
                st.download_button(
                    "Download source PDF",
                    PDF_PATH.read_bytes(),
                    file_name=PDF_PATH.name,
                    mime="application/pdf",
                    width="stretch",
                )
        with c2:
            st.link_button("GitHub repo", "https://github.com/violettefuze/portfolio", width="stretch")
    with right:
        st.image(str(image_path), width="stretch")


def render_about(content: dict[str, Any]) -> None:
    about = content["about"]
    st.markdown('<div class="section-label">About</div>', unsafe_allow_html=True)
    cols = st.columns([1.15, 0.85], gap="large")
    with cols[0]:
        st.markdown(f"## {about['headline']}")
        for paragraph in about["paragraphs"]:
            st.write(paragraph)
    with cols[1]:
        st.markdown('<div class="surface">', unsafe_allow_html=True)
        st.markdown("### Kurzprofil")
        for fact in about["facts"]:
            st.markdown(f"- {fact}")
        st.markdown("</div>", unsafe_allow_html=True)


def render_project_media(project: dict[str, Any]) -> None:
    hero_image = project.get("hero_image")
    stills = project.get("stills", [])
    if hero_image:
        st.image(str(ROOT / hero_image), width="stretch")
    else:
        st.markdown(
            f'<div class="placeholder-visual"><div>{project["category"]}<br><span class="muted">{project["role"]}</span></div></div>',
            unsafe_allow_html=True,
        )

    if stills:
        gallery_cols = st.columns(len(stills), gap="small")
        for col, still in zip(gallery_cols, stills):
            with col:
                st.image(str(ROOT / still), width="stretch")


def render_project(project: dict[str, Any]) -> None:
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    cols = st.columns([1.05, 0.95], gap="large")
    with cols[0]:
        render_project_media(project)
    with cols[1]:
        st.markdown(f'<div class="project-title">{project["title"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="project-meta">{project["category"]} · {project["role"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="project-summary">{project["summary"]}</div>', unsafe_allow_html=True)
        for note in project.get("notes", []):
            st.markdown(f'<span class="tag">{note}</span>', unsafe_allow_html=True)
        st.write("")
        st.video(project["video_url"])
        st.link_button("Open original link", project["video_url"], width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)


def render_projects(content: dict[str, Any]) -> None:
    st.markdown('<div class="section-label">Selected work</div>', unsafe_allow_html=True)
    st.markdown("## Projekte mit direkter Wiedergabe")
    st.caption("Die Videos spielen direkt in der Seite. Weitere Projekte lassen sich spaeter einfach ueber die JSON-Daten erweitern.")
    for project in content["projects"]:
        render_project(project)


def render_skills(content: dict[str, Any]) -> None:
    skills = content["skills"]
    st.markdown('<div class="section-label">Skills</div>', unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("### Kamera")
        for item in skills["camera"]:
            st.markdown(f"- {item}")
    with right:
        st.markdown("### Postproduktion")
        for item in skills["postproduction"]:
            st.markdown(f"- {item}")
    st.markdown(f"> {skills['focus']}")


def render_statement() -> None:
    st.markdown('<div class="section-label">Statement</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="quote-panel">
            <div class="quote-text">
                Viele Filme sind technisch sauber,<br>
                aber austauschbar.<br><br>
                Genau das interessiert mich nicht.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_contact(content: dict[str, Any]) -> None:
    contact = content["contact"]
    site = content["site"]
    st.markdown('<div class="section-label">Contact</div>', unsafe_allow_html=True)
    cols = st.columns([1, 1], gap="large")
    with cols[0]:
        st.markdown(f"## {site['title']}")
        st.write(site["subtitle"])
        st.caption(site["location"])
    with cols[1]:
        st.markdown('<div class="contact-label">Mail</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="contact-value">{contact["email"] or "to be provided"}</div>', unsafe_allow_html=True)
        st.markdown('<div class="small-gap"></div>', unsafe_allow_html=True)
        st.markdown('<div class="contact-label">Instagram</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="contact-value">{contact["instagram"] or "to be provided"}</div>', unsafe_allow_html=True)
        if contact.get("website"):
            st.markdown('<div class="small-gap"></div>', unsafe_allow_html=True)
            st.markdown('<div class="contact-label">Website</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="contact-value">{contact["website"]}</div>', unsafe_allow_html=True)
    if contact.get("note"):
        st.info(contact["note"])


def main() -> None:
    st.set_page_config(
        page_title="Tim Heid | Portfolio",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    content = load_content()
    inject_css()
    render_sidebar(content)
    render_hero(content)
    st.divider()
    render_about(content)
    st.divider()
    render_projects(content)
    st.divider()
    render_skills(content)
    st.divider()
    render_statement()
    st.divider()
    render_contact(content)


if __name__ == "__main__":
    main()
