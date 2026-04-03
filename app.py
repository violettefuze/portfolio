from __future__ import annotations

import base64
import html
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import streamlit as st
import streamlit.components.v1 as components


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


def video_embed_url(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if "youtu.be" in host:
        video_id = parsed.path.strip("/")
        return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1" if video_id else None

    if "youtube.com" in host:
        video_id = None
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/")[2]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/")[2]
        return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1" if video_id else None

    if "vimeo.com" in host:
        segments = [segment for segment in parsed.path.split("/") if segment]
        video_id = next((segment for segment in segments if segment.isdigit()), None)
        return f"https://player.vimeo.com/video/{video_id}" if video_id else None

    return None


def render_video_player(url: str, title: str, height: int = 360) -> None:
    embed_url = video_embed_url(url)
    if not embed_url:
        st.link_button("Film öffnen", url, width="stretch")
        return

    safe_url = html.escape(embed_url, quote=True)
    safe_title = html.escape(title)
    components.html(
        f"""
        <style>
            html, body {{
                margin: 0;
                background: transparent;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }}

            .video-shell {{
                width: 100%;
                height: 100%;
                border-radius: 26px;
                overflow: hidden;
                border: 1px solid rgba(201,176,137,0.14);
                background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
                box-shadow: 0 18px 40px rgba(0,0,0,0.22);
            }}

            iframe {{
                width: 100%;
                height: 100%;
                border: 0;
                display: block;
            }}
        </style>
        <div class="video-shell">
            <iframe
                src="{safe_url}"
                title="{safe_title}"
                loading="lazy"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen
            ></iframe>
        </div>
        """,
        height=height,
    )


def inject_css() -> None:
    render_html(
        """
        <style>
        :root {
            --bg: #141110;
            --bg-soft: #1b1716;
            --panel: rgba(255,255,255,0.028);
            --panel-strong: rgba(255,255,255,0.046);
            --line: rgba(201,176,137,0.14);
            --line-strong: rgba(201,176,137,0.32);
            --text: #f3ede4;
            --muted: rgba(243,237,228,0.72);
            --gold: #c9b089;
            --shadow: 0 30px 72px rgba(0,0,0,0.34);
        }

        html {
            scroll-behavior: smooth;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(201,176,137,0.08), transparent 22%),
                linear-gradient(180deg, #151110 0%, #110f0f 100%);
            color: var(--text);
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }

        #MainMenu, footer, header[data-testid="stHeader"] {
            visibility: hidden;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        .block-container {
            max-width: 1230px;
            padding-top: 1.1rem;
            padding-bottom: 5rem;
        }

        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stLinkButton > a {
            width: 100%;
            min-height: 3.05rem;
            border-radius: 999px;
            border: 1px solid var(--line-strong);
            background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.018));
            color: var(--text);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-size: 0.72rem;
            text-decoration: none;
            transition: transform 0.22s ease, background 0.22s ease, border-color 0.22s ease;
            box-shadow: none;
        }

        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stLinkButton > a:hover {
            transform: translateY(-1px);
            border-color: rgba(201,176,137,0.46);
            background: linear-gradient(180deg, rgba(201,176,137,0.18), rgba(255,255,255,0.03));
            color: var(--text);
        }

        .site-shell {
            display: flex;
            flex-direction: column;
            gap: 4.4rem;
        }

        .fade-up {
            animation: fadeUp 0.82s ease both;
        }

        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(24px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
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
        }

        .brand-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }

        .brand-copy {
            display: flex;
            flex-direction: column;
            gap: 0.14rem;
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
            gap: 1.2rem;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero {
            position: relative;
            min-height: 40rem;
            border-radius: 38px;
            overflow: hidden;
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
            transition: transform 8s ease;
        }

        .hero:hover .hero-media {
            transform: scale(1.05);
        }

        .hero-scrim {
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(11,10,10,0.86) 0%, rgba(11,10,10,0.68) 38%, rgba(11,10,10,0.18) 100%),
                linear-gradient(180deg, rgba(11,10,10,0.12) 0%, rgba(11,10,10,0.44) 100%);
        }

        .hero-content {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            justify-content: end;
            min-height: 40rem;
            padding: 3rem;
            max-width: 44rem;
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
            font-size: clamp(3.6rem, 8vw, 6.4rem);
            line-height: 0.92;
            letter-spacing: -0.04em;
            color: #fbf6ef;
        }

        .hero-statement {
            margin-top: 1rem;
            font-size: 1.28rem;
            line-height: 1.32;
            color: rgba(251,246,239,0.90);
            max-width: 34rem;
        }

        .hero-copy {
            margin-top: 1.2rem;
            max-width: 35rem;
            font-size: 1rem;
            line-height: 1.82;
            color: rgba(251,246,239,0.78);
        }

        .hero-note {
            margin-top: 1.1rem;
            display: inline-flex;
            align-items: center;
            width: fit-content;
            border-radius: 999px;
            border: 1px solid rgba(201,176,137,0.22);
            background: rgba(201,176,137,0.09);
            padding: 0.55rem 0.85rem;
            color: rgba(251,246,239,0.84);
            font-size: 0.8rem;
            line-height: 1.4;
        }

        .statement-grid,
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
        }

        .statement-card,
        .skill-card,
        .work-card,
        .quote-panel,
        .contact-panel {
            border-radius: 26px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, var(--panel-strong), var(--panel));
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.16);
        }

        .statement-card,
        .skill-card {
            padding: 1.35rem 1.4rem;
            transition: transform 0.26s ease, border-color 0.26s ease, box-shadow 0.26s ease;
        }

        .statement-card:hover,
        .skill-card:hover,
        .work-card:hover {
            transform: translateY(-4px);
            border-color: rgba(201,176,137,0.28);
            box-shadow: 0 18px 44px rgba(0,0,0,0.24);
        }

        .statement-label,
        .section-label,
        .skill-label,
        .work-label,
        .contact-label {
            margin: 0 0 0.55rem 0;
            font-size: 0.74rem;
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: var(--gold);
        }

        .statement-text,
        .skill-text {
            margin: 0;
            color: var(--text);
            line-height: 1.7;
            font-size: 0.98rem;
        }

        .logo-band {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            overflow: hidden;
        }

        .logo-label {
            margin: 0;
            color: var(--gold);
            font-size: 0.74rem;
            letter-spacing: 0.24em;
            text-transform: uppercase;
        }

        .logo-track {
            display: flex;
            gap: 1.1rem;
            width: max-content;
            animation: marquee 26s linear infinite;
        }

        .logo-band:hover .logo-track {
            animation-play-state: paused;
        }

        @keyframes marquee {
            from { transform: translateX(0); }
            to { transform: translateX(-50%); }
        }

        .logo-card {
            width: 146px;
            height: 78px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 22px;
            border: 1px solid rgba(201,176,137,0.12);
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.018));
            transition: transform 0.24s ease, background 0.24s ease;
        }

        .logo-card:hover {
            transform: translateY(-3px);
            background: linear-gradient(180deg, rgba(201,176,137,0.09), rgba(255,255,255,0.02));
        }

        .logo-card img {
            max-width: 88px;
            max-height: 34px;
            object-fit: contain;
            display: block;
            filter: grayscale(0%);
        }

        .section-heading {
            margin: 0;
            font-size: clamp(2rem, 4vw, 3.4rem);
            line-height: 1.02;
            letter-spacing: -0.03em;
            color: #faf5ed;
        }

        .section-copy {
            margin-top: 1rem;
            max-width: 42rem;
            color: var(--muted);
            line-height: 1.8;
            font-size: 1rem;
        }

        .work-card {
            padding: 1.25rem;
            margin-top: 1.2rem;
            transition: transform 0.26s ease, border-color 0.26s ease;
        }

        .work-placeholder {
            min-height: 330px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border-radius: 26px;
            border: 1px solid rgba(201,176,137,0.14);
            background:
                radial-gradient(circle at top center, rgba(201,176,137,0.08), transparent 46%),
                linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
            box-shadow: 0 18px 40px rgba(0,0,0,0.22);
            padding: 2rem;
        }

        .work-placeholder-title {
            margin: 0;
            font-size: 2rem;
            line-height: 1.04;
            color: #faf5ed;
        }

        .work-placeholder-copy {
            margin-top: 0.9rem;
            max-width: 24rem;
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.75;
        }

        .work-title {
            margin: 0;
            font-size: 1.9rem;
            line-height: 1.02;
            color: #faf5ed;
        }

        .work-role {
            margin-top: 0.5rem;
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.7;
        }

        .work-summary {
            margin-top: 0.9rem;
            color: var(--text);
            font-size: 1rem;
            line-height: 1.78;
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
            border: 1px solid rgba(201,176,137,0.18);
            background: rgba(201,176,137,0.08);
            padding: 0.42rem 0.72rem;
            color: rgba(251,246,239,0.86);
            font-size: 0.82rem;
        }

        .quote-panel {
            padding: 3.8rem 2rem;
            text-align: center;
            background:
                radial-gradient(circle at top center, rgba(201,176,137,0.08), transparent 40%),
                linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
        }

        .quote-text {
            max-width: 44rem;
            margin: 0 auto;
            color: #faf5ed;
            font-size: clamp(1.5rem, 2.8vw, 2.5rem);
            line-height: 1.45;
        }

        .contact-panel {
            padding: 2rem;
        }

        .contact-value {
            margin: 0 0 1rem 0;
            color: var(--text);
            font-size: 1rem;
            line-height: 1.72;
        }

        .site-link {
            color: var(--gold) !important;
            text-decoration: none;
        }

        .site-link:hover {
            text-decoration: underline;
        }

        @media (max-width: 960px) {
            .statement-grid,
            .skills-grid {
                grid-template-columns: 1fr;
            }

            .topbar {
                flex-direction: column;
                align-items: flex-start;
            }

            .hero {
                min-height: 32rem;
            }

            .hero-content {
                min-height: 32rem;
                padding: 2rem;
            }
        }
        </style>
        """
    )


def render_topbar(content: dict[str, Any]) -> None:
    site = content["site"]
    brand_mark_uri = image_data_uri(ROOT / site["brand_mark"])
    render_html(
        f"""
        <div class="topbar fade-up">
            <div class="brand-mark">
                <div class="brand-logo"><img src="{brand_mark_uri}" alt="{html.escape(site["title"])} pictogram"></div>
                <div class="brand-copy">
                    <p class="brand-title">{html.escape(site["title"])}</p>
                    <p class="brand-subtitle">{html.escape(site["subtitle"])}</p>
                </div>
            </div>
            <div class="nav-copy">
                <span>Selected Work</span>
                <span>Clients</span>
                <span>Experience</span>
                <span>Contact</span>
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
        <section class="hero fade-up">
            <div class="hero-media" style="{background_style}"></div>
            <div class="hero-scrim"></div>
            <div class="hero-content">
                <div class="eyebrow">{html.escape(site["hero_kicker"])}</div>
                <h1>{html.escape(site["title"])}</h1>
                <div class="hero-statement">{html.escape(site["hero_statement"])}</div>
                <div class="hero-copy">{html.escape(site["intro"])}</div>
                <div class="hero-note">{html.escape(site["availability_note"])}</div>
            </div>
        </section>
        """
    )

    left, middle, right = st.columns(3, gap="small")
    with left:
        st.link_button("Bewerbungs-PDF", f"data:application/pdf;base64,{base64.b64encode(PDF_PATH.read_bytes()).decode('ascii')}", width="stretch")
    with middle:
        st.link_button("FrameArt", "https://frameart.lu", width="stretch")
    with right:
        st.link_button("Website", content["contact"]["website"], width="stretch")


def render_statements(content: dict[str, Any]) -> None:
    cards = ['<div class="statement-grid fade-up">']
    for text in content["statements"]:
        cards.append(
            f'<div class="statement-card"><p class="statement-label">Erfahrung</p>'
            f'<p class="statement-text">{html.escape(text)}</p></div>'
        )
    cards.append("</div>")
    render_html("".join(cards))


def render_partner_logos(content: dict[str, Any]) -> None:
    logos_markup = []
    for partner in content["partners"]:
        logo_uri = image_data_uri(ROOT / partner["logo"])
        logos_markup.append(
            f'<div class="logo-card"><img src="{logo_uri}" alt="{html.escape(partner["name"])}"></div>'
        )
    repeated = "".join(logos_markup + logos_markup)
    render_html(
        f"""
        <section class="logo-band fade-up">
            <p class="logo-label">Kunden aus dem FrameArt-Umfeld</p>
            <div class="logo-track">{repeated}</div>
        </section>
        """
    )


def render_selected_work_intro() -> None:
    render_html('<div class="section-label">Selected Work</div>')
    render_html('<h2 class="section-heading">Von oben nach unten lesbar. Erst Wirkung, dann Details.</h2>')
    render_html(
        '<p class="section-copy">Weniger Text, klarere Aussagen und Arbeiten, die zeigen, wie breit das Produktionswissen wirklich ist: FrameArt-Produktionen, Corporate-Arbeit und eigene Filme mit kompletter Verantwortung.</p>'
    )


def render_project(project: dict[str, Any], index: int) -> None:
    render_html('<div class="work-card fade-up">')
    video_col, text_col = st.columns([1.12, 0.88], gap="large")
    with video_col:
        if "vimeo.com" in project["video_url"]:
            render_html(
                f"""
                <div class="work-placeholder">
                    <p class="work-placeholder-title">{html.escape(project["title"])}</p>
                    <p class="work-placeholder-copy">Das Showreel ist bewusst Teil der Bewerbung. In dieser Ansicht wird es als sauberer Showcase-Block mit direktem Vimeo-Link gezeigt.</p>
                </div>
                """
            )
        else:
            render_video_player(project["video_url"], project["title"], height=390 if index == 0 else 330)
    with text_col:
        render_html(f'<p class="work-label">{html.escape(project["category"])}</p>')
        render_html(f'<h3 class="work-title">{html.escape(project["title"])}</h3>')
        render_html(f'<p class="work-role">{html.escape(project["role"])}</p>')
        render_html(f'<p class="work-summary">{html.escape(project["summary"])}</p>')
        notes = "".join(f'<span class="tag">{html.escape(note)}</span>' for note in project.get("notes", []))
        render_html(f'<div class="tag-row">{notes}</div>')
        st.link_button("Original öffnen", project["video_url"], width="stretch")
    render_html("</div>")


def render_selected_work(content: dict[str, Any]) -> None:
    render_selected_work_intro()
    for index, project in enumerate(content["projects"]):
        render_project(project, index)


def render_experience(content: dict[str, Any]) -> None:
    render_html('<div class="section-label">Background</div>')
    render_html('<h2 class="section-heading">Lehre, Set-Erfahrung, eigene GmbH.</h2>')
    render_html(
        '<p class="section-copy">Die Kombination aus Lehre bei FrameArt Media, europaweiter Produktionspraxis und späterer Verantwortung als Gesellschafter und Geschäftsführer sorgt dafür, dass Kamera, Licht, Ton, Postproduktion und Kundenlogik zusammen gedacht werden.</p>'
    )

    cols = st.columns(3, gap="large")
    for col, item in zip(cols, content["background"]):
        with col:
            link_markup = ""
            if item.get("link_url"):
                link_markup = (
                    f'<p class="site-link" style="margin-top:0.8rem;"><a class="site-link" href="{html.escape(item["link_url"], quote=True)}" target="_blank">{html.escape(item["link_label"])}</a></p>'
                )
            render_html(
                f"""
                <div class="statement-card fade-up">
                    <p class="statement-label">{html.escape(item["title"])}</p>
                    <p class="statement-text">{html.escape(item["text"])}</p>
                    {link_markup}
                </div>
                """
            )


def render_skills(content: dict[str, Any]) -> None:
    skills = content["skills"]
    render_html('<div class="section-label">Tools & Craft</div>')
    render_html('<h2 class="section-heading">Moderne Filmkameras, Ton, Licht und Post.</h2>')
    render_html(f'<p class="section-copy">{html.escape(skills["focus"])}</p>')

    groups = [
        ("Kamera", skills["camera"]),
        ("Ton & Licht", skills["sound"] + skills["lighting"]),
        ("Postproduktion", skills["postproduction"]),
    ]
    markup = ['<div class="skills-grid fade-up">']
    for title, items in groups:
        pills = "".join(f'<span class="tag">{html.escape(item)}</span>' for item in items)
        markup.append(
            f'<div class="skill-card"><p class="skill-label">{html.escape(title)}</p>'
            f'<div class="tag-row">{pills}</div></div>'
        )
    markup.append("</div>")
    render_html("".join(markup))


def render_quote() -> None:
    render_html(
        """
        <div class="quote-panel fade-up">
            <div class="quote-text">
                Ich kenne Produktion nicht nur aus einer Rolle.<br>
                Ich kenne sie von der Lehre bis zur Geschäftsführung.
            </div>
        </div>
        """
    )


def render_contact(content: dict[str, Any]) -> None:
    site = content["site"]
    contact = content["contact"]
    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        render_html('<div class="section-label">Kontakt</div>')
        render_html(f'<h2 class="section-heading">{html.escape(site["title"])}</h2>')
        render_html(f'<p class="section-copy">{html.escape(site["subtitle"])}<br>{html.escape(site["location"])}</p>')
    with right:
        render_html('<div class="contact-panel fade-up">')
        render_html('<div class="contact-label">Mail</div>')
        render_html(f'<p class="contact-value">{html.escape(contact["email"])}</p>')
        render_html('<div class="contact-label">Telefon</div>')
        render_html(f'<p class="contact-value">{html.escape(contact["phone"])}</p>')
        render_html('<div class="contact-label">Website</div>')
        render_html(
            f'<p class="contact-value"><a class="site-link" href="{html.escape(contact["website"], quote=True)}" target="_blank">{html.escape(contact["website"])}</a></p>'
        )
        render_html(f'<p class="contact-value">{html.escape(contact["note"])}</p>')
        render_html('</div>')


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
    render_statements(content)
    render_partner_logos(content)
    render_selected_work(content)
    render_experience(content)
    render_skills(content)
    render_quote()
    render_contact(content)
    render_html('</div>')


if __name__ == "__main__":
    main()
