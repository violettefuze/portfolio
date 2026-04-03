from __future__ import annotations

import base64
import html
import json
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "portfolio_content.json"
PDF_PATH = ROOT / "Bewerbung_Tim_Heid_Babelsberg.pdf"


def load_content() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def image_data_uri(path: Path) -> str | None:
    if not path.exists():
        return None
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/{path.suffix.lstrip('.').lower()};base64,{encoded}"


def render_html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def inject_css() -> None:
    render_html(
        """
        <style>
        :root {
            --bg: #161211;
            --bg-elevated: #1d1817;
            --panel: rgba(255, 255, 255, 0.028);
            --panel-strong: rgba(255, 255, 255, 0.045);
            --line: rgba(198, 178, 142, 0.16);
            --line-strong: rgba(198, 178, 142, 0.32);
            --text: #f1ebe2;
            --muted: rgba(241, 235, 226, 0.70);
            --gold: #c9b089;
            --gold-soft: rgba(201, 176, 137, 0.16);
            --shadow: 0 32px 72px rgba(0, 0, 0, 0.34);
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(201, 176, 137, 0.08), transparent 22%),
                linear-gradient(180deg, #151110 0%, #120f0f 100%);
            color: var(--text);
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }

        #MainMenu, footer, header[data-testid="stHeader"] {
            visibility: hidden;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        .block-container {
            max-width: 1220px;
            padding-top: 1.4rem;
            padding-bottom: 5rem;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stButton > button,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stDownloadButton > button,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stLinkButton > a {
            width: 100%;
            min-height: 3.1rem;
            border-radius: 999px;
            border: 1px solid var(--line-strong);
            background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.018));
            color: var(--text);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-size: 0.72rem;
            text-decoration: none;
            transition: 0.18s ease;
            box-shadow: none;
        }

        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stButton > button:hover,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stDownloadButton > button:hover,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stLinkButton > a:hover {
            border-color: rgba(201, 176, 137, 0.45);
            background: linear-gradient(180deg, rgba(201,176,137,0.18), rgba(255,255,255,0.03));
            color: var(--text);
        }

        .site-shell {
            display: flex;
            flex-direction: column;
            gap: 4.2rem;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1.5rem;
            padding: 0.4rem 0 0.2rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            gap: 0.85rem;
        }

        .brand-logo {
            width: 42px;
            height: 42px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 auto;
        }

        .brand-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }

        .brand-square {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            background: linear-gradient(135deg, var(--gold), #f4ecdf);
            box-shadow: 0 0 0 1px rgba(255,255,255,0.06);
        }

        .brand-copy {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .brand-title {
            margin: 0;
            font-size: 0.94rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--text);
        }

        .brand-subtitle {
            margin: 0;
            font-size: 0.75rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--muted);
        }

        .nav-copy {
            display: flex;
            gap: 1.3rem;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero {
            position: relative;
            border-radius: 34px;
            overflow: hidden;
            min-height: 36rem;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.015));
            box-shadow: var(--shadow);
        }

        .hero-media {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center center;
            transform: scale(1.01);
        }

        .hero-scrim {
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(11,10,10,0.82) 0%, rgba(11,10,10,0.64) 38%, rgba(11,10,10,0.24) 100%),
                linear-gradient(180deg, rgba(11,10,10,0.10) 0%, rgba(11,10,10,0.40) 100%);
        }

        .hero-content {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            justify-content: end;
            min-height: 36rem;
            padding: 3rem;
            max-width: 42rem;
        }

        .eyebrow {
            margin: 0 0 1rem 0;
            font-size: 0.76rem;
            letter-spacing: 0.28em;
            text-transform: uppercase;
            color: var(--gold);
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(3.4rem, 8vw, 6.2rem);
            line-height: 0.92;
            letter-spacing: -0.04em;
            color: #fbf6ef;
        }

        .hero-role {
            margin-top: 1rem;
            font-size: 1.05rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: rgba(251, 246, 239, 0.86);
        }

        .hero-copy {
            margin-top: 1.3rem;
            max-width: 34rem;
            font-size: 1.06rem;
            line-height: 1.8;
            color: rgba(251, 246, 239, 0.78);
        }

        .hero-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
        }

        .strip-card,
        .process-card,
        .background-card,
        .skill-card {
            border-radius: 24px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, var(--panel-strong), var(--panel));
            padding: 1.35rem 1.4rem;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.16);
        }

        .strip-title,
        .process-title,
        .background-title,
        .skill-title {
            margin: 0 0 0.5rem 0;
            font-size: 0.86rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--gold);
        }

        .strip-text,
        .process-text,
        .background-text,
        .skill-text {
            margin: 0;
            color: var(--text);
            line-height: 1.7;
            font-size: 0.98rem;
        }

        .section-label {
            margin-bottom: 0.8rem;
            font-size: 0.74rem;
            letter-spacing: 0.26em;
            text-transform: uppercase;
            color: var(--gold);
        }

        .section-heading {
            margin: 0;
            font-size: clamp(2rem, 4vw, 3.3rem);
            line-height: 1.02;
            letter-spacing: -0.03em;
            color: #faf5ed;
        }

        .section-copy {
            margin-top: 1rem;
            max-width: 42rem;
            color: var(--muted);
            line-height: 1.85;
            font-size: 1rem;
        }

        .project-wrap {
            margin-top: 1.25rem;
            padding: 1.2rem;
            border-radius: 30px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
        }

        .project-title {
            margin: 0;
            font-size: 1.8rem;
            color: #faf5ed;
        }

        .project-meta {
            margin-top: 0.45rem;
            color: var(--muted);
            line-height: 1.7;
            font-size: 0.96rem;
        }

        .project-summary {
            margin-top: 1rem;
            color: var(--text);
            line-height: 1.85;
            font-size: 1rem;
        }

        .tag-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }

        .tag {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            border: 1px solid rgba(201, 176, 137, 0.18);
            background: rgba(201, 176, 137, 0.08);
            padding: 0.42rem 0.72rem;
            color: rgba(251, 246, 239, 0.86);
            font-size: 0.82rem;
        }

        .project-image {
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 0.85rem;
        }

        .project-caption {
            padding: 0.9rem 1rem;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
            color: var(--muted);
            font-size: 0.94rem;
            line-height: 1.7;
            margin-bottom: 0.85rem;
        }

        .statement {
            padding: 4.5rem 2rem;
            border-radius: 34px;
            border: 1px solid var(--line);
            background:
                radial-gradient(circle at top center, rgba(201,176,137,0.09), transparent 38%),
                linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
            text-align: center;
            box-shadow: var(--shadow);
        }

        .statement-text {
            max-width: 46rem;
            margin: 0 auto;
            color: #faf5ed;
            font-size: clamp(1.6rem, 3vw, 2.6rem);
            line-height: 1.5;
        }

        .contact-panel {
            border-radius: 30px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.018));
            padding: 2rem;
        }

        .contact-label {
            margin-bottom: 0.25rem;
            font-size: 0.72rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--gold);
        }

        .contact-value {
            margin-bottom: 1rem;
            color: var(--text);
            font-size: 1rem;
            line-height: 1.7;
        }

        .helper-note {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.7;
        }

        .site-link {
            color: var(--gold) !important;
            text-decoration: none;
        }

        .site-link:hover {
            text-decoration: underline;
        }

        @media (max-width: 900px) {
            .hero-strip {
                grid-template-columns: 1fr;
            }

            .topbar {
                flex-direction: column;
                align-items: flex-start;
            }

            .hero {
                min-height: 30rem;
            }

            .hero-content {
                min-height: 30rem;
                padding: 2rem;
            }
        }
        </style>
        """
    )


def render_topbar(content: dict[str, Any]) -> None:
    site = content["site"]
    brand_mark_path = ROOT / site["brand_mark"] if site.get("brand_mark") else None
    brand_mark_uri = image_data_uri(brand_mark_path) if brand_mark_path else None
    brand_visual = '<div class="brand-square"></div>'
    if brand_mark_uri:
        brand_visual = (
            f'<div class="brand-logo"><img src="{brand_mark_uri}" '
            f'alt="{html.escape(site["title"])} pictogram"></div>'
        )
    render_html(
        f"""
        <div class="topbar">
            <div class="brand-mark">
                {brand_visual}
                <div class="brand-copy">
                    <p class="brand-title">{html.escape(site["title"])}</p>
                    <p class="brand-subtitle">{html.escape(site["subtitle"])}</p>
                </div>
            </div>
            <div class="nav-copy">
                <span>Selected Work</span>
                <span>Production Background</span>
                <span>Direct Video Playback</span>
            </div>
        </div>
        """
    )


def render_hero(content: dict[str, Any]) -> None:
    site = content["site"]
    hero_image = image_data_uri(ROOT / site["hero_image"])
    background_style = (
        f"background-image: url('{hero_image}');" if hero_image else "background: linear-gradient(180deg, #1b1716, #141110);"
    )
    render_html(
        f"""
        <section class="hero">
            <div class="hero-media" style="{background_style}"></div>
            <div class="hero-scrim"></div>
            <div class="hero-content">
                <div class="eyebrow">{html.escape(site["hero_kicker"])}</div>
                <h1>{html.escape(site["title"])}</h1>
                <div class="hero-role">{html.escape(site["subtitle"])}</div>
                <div class="hero-copy">{html.escape(site["intro"])}</div>
            </div>
        </section>
        """
    )

    c1, c2, c3 = st.columns([1.05, 1, 1], gap="small")
    with c1:
        if PDF_PATH.exists():
            st.download_button(
                "Bewerbungs-PDF",
                PDF_PATH.read_bytes(),
                file_name=PDF_PATH.name,
                mime="application/pdf",
                width="stretch",
            )
    with c2:
        st.link_button("FrameArt Media", "https://frameart.lu", width="stretch")
    with c3:
        st.link_button("Website", content["contact"]["website"], width="stretch")


def render_intro_strip(content: dict[str, Any]) -> None:
    cards = [
        {
            "title": "Grundlage",
            "text": "Professionelle Werbefilmproduktion als Fundament statt rein theoretischer Einstieg.",
        },
        {
            "title": "Fokus",
            "text": content["site"]["tagline"],
        },
        {
            "title": "Ort",
            "text": content["site"]["location"],
        },
    ]
    markup = ['<div class="hero-strip">']
    for card in cards:
        markup.append(
            f'<div class="strip-card"><p class="strip-title">{html.escape(card["title"])}</p>'
            f'<p class="strip-text">{html.escape(card["text"])}</p></div>'
        )
    markup.append("</div>")
    render_html("".join(markup))


def render_about(content: dict[str, Any]) -> None:
    about = content["about"]
    render_html('<div class="section-label">Profil</div>')
    render_html(f'<h2 class="section-heading">{html.escape(about["headline"])}</h2>')
    cols = st.columns([1.18, 0.82], gap="large")
    with cols[0]:
        for paragraph in about["paragraphs"]:
            render_html(f'<p class="section-copy">{html.escape(paragraph)}</p>')
    with cols[1]:
        facts_markup = ['<div class="skill-card">', '<p class="skill-title">Kurzprofil</p>']
        for fact in about["facts"]:
            facts_markup.append(f'<p class="skill-text">• {html.escape(fact)}</p>')
        facts_markup.append("</div>")
        render_html("".join(facts_markup))


def render_process(content: dict[str, Any]) -> None:
    render_html('<div class="section-label">Arbeitsweise</div>')
    render_html('<h2 class="section-heading">Produktionslogik statt reines Selbstmarketing.</h2>')
    render_html(
        '<p class="section-copy">Die Struktur ist von einer Produktionswebsite inspiriert: klar, reduziert und auf echte Arbeit ausgerichtet. Nicht als Kopie von FrameArt, sondern als persönliche Übersetzung auf dein Profil.</p>'
    )
    cols = st.columns(3, gap="large")
    for col, item in zip(cols, content["process"]):
        with col:
            render_html(
                f"""
                <div class="process-card">
                    <p class="process-title">{html.escape(item["title"])}</p>
                    <p class="process-text">{html.escape(item["text"])}</p>
                </div>
                """
            )


def render_project_media(project: dict[str, Any]) -> None:
    hero_image = project.get("hero_image")
    if hero_image:
        render_html('<div class="project-image">')
        st.image(str(ROOT / hero_image), width="stretch")
        render_html("</div>")

    if project.get("stills"):
        gallery = st.columns(len(project["stills"]), gap="small")
        for col, still in zip(gallery, project["stills"]):
            with col:
                st.image(str(ROOT / still), width="stretch")
        st.write("")

    if not hero_image and not project.get("stills"):
        render_html(
            f'<div class="project-caption">{html.escape(project["category"])} · {html.escape(project["role"])}</div>'
        )

    st.video(project["video_url"])


def render_project_details(project: dict[str, Any]) -> None:
    render_html(f'<h3 class="project-title">{html.escape(project["title"])}</h3>')
    render_html(
        f'<div class="project-meta">{html.escape(project["category"])} · {html.escape(project["role"])}</div>'
    )
    render_html(f'<div class="project-summary">{html.escape(project["summary"])}</div>')

    tags = "".join(f'<span class="tag">{html.escape(note)}</span>' for note in project.get("notes", []))
    render_html(f'<div class="tag-row">{tags}</div>')
    st.write("")
    st.link_button("Original öffnen", project["video_url"], width="stretch")


def render_projects(content: dict[str, Any]) -> None:
    render_html('<div class="section-label">Selected Work</div>')
    render_html('<h2 class="section-heading">Projekte mit direkter Wiedergabe.</h2>')
    render_html(
        '<p class="section-copy">Die Videos lassen sich direkt in der Seite abspielen. Damit wirkt die Bewerbung weniger wie ein PDF-Anhang und mehr wie ein kontrolliertes Portfolio, das man sofort ansehen kann.</p>'
    )

    for index, project in enumerate(content["projects"]):
        render_html('<div class="project-wrap">')
        left, right = st.columns([1.06, 0.94], gap="large")
        if index % 2 == 0:
            media_col, detail_col = left, right
        else:
            media_col, detail_col = right, left
        with media_col:
            render_project_media(project)
        with detail_col:
            render_project_details(project)
        render_html("</div>")


def render_background(content: dict[str, Any]) -> None:
    render_html('<div class="section-label">Background</div>')
    render_html('<h2 class="section-heading">Woher die Arbeit kommt.</h2>')
    render_html(
        '<p class="section-copy">Die Stärke deiner Seite sollte nicht darin liegen, eine Agentur zu imitieren, sondern zu zeigen, aus welchem professionellen Umfeld dein Blick entstanden ist und wie du ihn heute eigenständig weiterführst.</p>'
    )

    cols = st.columns(3, gap="large")
    for col, item in zip(cols, content["background"]):
        with col:
            link_markup = ""
            if item.get("link_url"):
                link_markup = (
                    f'<p class="helper-note"><a class="site-link" href="{html.escape(item["link_url"])}" target="_blank">'
                    f'{html.escape(item["link_label"])}</a></p>'
                )
            render_html(
                f"""
                <div class="background-card">
                    <p class="background-title">{html.escape(item["title"])}</p>
                    <p class="background-text">{html.escape(item["text"])}</p>
                    {link_markup}
                </div>
                """
            )


def render_skills(content: dict[str, Any]) -> None:
    skills = content["skills"]
    render_html('<div class="section-label">Technik</div>')
    render_html('<h2 class="section-heading">Werkzeuge und Schwerpunkt.</h2>')
    left, right = st.columns(2, gap="large")
    with left:
        camera_markup = ['<div class="skill-card">', '<p class="skill-title">Kamera</p>']
        for item in skills["camera"]:
            camera_markup.append(f'<p class="skill-text">• {html.escape(item)}</p>')
        camera_markup.append("</div>")
        render_html("".join(camera_markup))
    with right:
        post_markup = ['<div class="skill-card">', '<p class="skill-title">Postproduktion</p>']
        for item in skills["postproduction"]:
            post_markup.append(f'<p class="skill-text">• {html.escape(item)}</p>')
        post_markup.append(f'<p class="helper-note">{html.escape(skills["focus"])}</p>')
        post_markup.append("</div>")
        render_html("".join(post_markup))


def render_statement() -> None:
    render_html('<div class="section-label">Statement</div>')
    render_html(
        """
        <div class="statement">
            <div class="statement-text">
                Viele Filme sind technisch sauber,<br>
                aber austauschbar.<br><br>
                Genau das interessiert mich nicht.
            </div>
        </div>
        """
    )


def render_contact(content: dict[str, Any]) -> None:
    site = content["site"]
    contact = content["contact"]
    render_html('<div class="section-label">Kontakt</div>')
    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        render_html(f'<h2 class="section-heading">{html.escape(site["title"])}</h2>')
        render_html(f'<p class="section-copy">{html.escape(site["subtitle"])}<br>{html.escape(site["location"])}</p>')
    with right:
        render_html('<div class="contact-panel">')
        render_html('<div class="contact-label">Mail</div>')
        render_html(f'<div class="contact-value">{html.escape(contact["email"])}</div>')
        render_html('<div class="contact-label">Telefon</div>')
        render_html(f'<div class="contact-value">{html.escape(contact["phone"])}</div>')
        render_html('<div class="contact-label">Website</div>')
        render_html(
            f'<div class="contact-value"><a class="site-link" href="{html.escape(contact["website"])}" target="_blank">{html.escape(contact["website"])}</a></div>'
        )
        if contact.get("instagram"):
            render_html('<div class="contact-label">Instagram</div>')
            render_html(f'<div class="contact-value">{html.escape(contact["instagram"])}</div>')
        render_html(f'<p class="helper-note">{html.escape(contact["note"])}</p>')
        render_html("</div>")


def main() -> None:
    st.set_page_config(
        page_title="Tim Heid | Portfolio",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    content = load_content()
    inject_css()
    render_html('<div class="site-shell">')
    render_topbar(content)
    render_hero(content)
    render_intro_strip(content)
    render_about(content)
    render_process(content)
    render_projects(content)
    render_background(content)
    render_skills(content)
    render_statement()
    render_contact(content)
    render_html("</div>")


if __name__ == "__main__":
    main()
