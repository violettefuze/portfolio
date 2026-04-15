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
        if not video_id:
            return None

        video_index = segments.index(video_id)
        video_hash = segments[video_index + 1] if len(segments) > video_index + 1 else None
        embed_url = f"https://player.vimeo.com/video/{video_id}"
        if video_hash:
            embed_url = f"{embed_url}?h={video_hash}"
        return embed_url

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
            --parallax-offset: 0px;
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
            max-width: 1380px;
            padding-top: 1.55rem;
            padding-bottom: 6.5rem;
            padding-left: clamp(1.4rem, 3vw, 2.6rem);
            padding-right: clamp(1.4rem, 3vw, 2.6rem);
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
            gap: 5.35rem;
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
            gap: 1.8rem;
            position: sticky;
            top: 1rem;
            z-index: 30;
            padding: 0.9rem 1.35rem;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 999px;
            background: linear-gradient(180deg, rgba(24,20,19,0.72), rgba(24,20,19,0.48));
            box-shadow: 0 18px 36px rgba(0,0,0,0.18);
            backdrop-filter: blur(20px) saturate(135%);
            -webkit-backdrop-filter: blur(20px) saturate(135%);
            overflow: hidden;
            isolation: isolate;
        }

        .topbar::before {
            content: "";
            position: absolute;
            inset: 1px 1px auto 1px;
            height: 56%;
            border-radius: inherit;
            background: linear-gradient(180deg, rgba(255,255,255,0.12), rgba(255,255,255,0.02));
            pointer-events: none;
            z-index: 0;
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            gap: 1rem;
            position: relative;
            z-index: 1;
        }

        .brand-logo {
            width: 48px;
            height: 48px;
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
            gap: 0.2rem;
        }

        .brand-title {
            margin: 0;
            font-size: 1rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--text);
        }

        .brand-subtitle {
            margin: 0;
            font-size: 0.79rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--muted);
        }

        .nav-copy {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 0.8rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            position: relative;
            z-index: 1;
        }

        .hero {
            position: relative;
            --hero-media-offset: 0px;
            --hero-content-offset: 0px;
            --hero-glow-offset: 0px;
            --hero-media-scale: 1.04;
            min-height: 43rem;
            border-radius: 42px;
            overflow: hidden;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.015));
            box-shadow: var(--shadow);
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 78% 16%, rgba(255,255,255,0.18), transparent 24%),
                linear-gradient(180deg, rgba(255,255,255,0.08), transparent 26%);
            opacity: 0.45;
            pointer-events: none;
            mix-blend-mode: screen;
            transform: translate3d(0, var(--hero-glow-offset), 0) scale(1.02);
            transition: transform 0.18s linear;
            will-change: transform;
        }

        .hero-media {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center top;
            transform: translate3d(0, var(--hero-media-offset), 0) scale(var(--hero-media-scale));
            transition: transform 0.18s linear;
            will-change: transform;
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
            min-height: 43rem;
            padding: 3.65rem;
            max-width: 47rem;
            transform: translate3d(0, var(--hero-content-offset), 0);
            transition: transform 0.18s linear;
            will-change: transform;
        }

        [data-parallax-speed] {
            transform: translate3d(0, var(--parallax-offset), 0);
            transition: transform 0.18s linear;
            will-change: transform;
        }

        .eyebrow {
            margin: 0 0 1.2rem 0;
            font-size: 0.8rem;
            letter-spacing: 0.32em;
            text-transform: uppercase;
            color: var(--gold);
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(4.2rem, 8.2vw, 7.25rem);
            line-height: 0.92;
            letter-spacing: -0.04em;
            color: #fbf6ef;
        }

        .hero-statement {
            margin-top: 1.15rem;
            font-size: 1.38rem;
            line-height: 1.34;
            color: rgba(251,246,239,0.90);
            max-width: 36rem;
        }

        .hero-copy {
            margin-top: 1.35rem;
            max-width: 38rem;
            font-size: 1.04rem;
            line-height: 1.88;
            color: rgba(251,246,239,0.78);
        }

        .hero-note {
            margin-top: 1.35rem;
            display: inline-flex;
            align-items: center;
            width: fit-content;
            border-radius: 999px;
            border: 1px solid rgba(201,176,137,0.22);
            background: rgba(201,176,137,0.09);
            padding: 0.62rem 0.98rem;
            color: rgba(251,246,239,0.84);
            font-size: 0.84rem;
            line-height: 1.4;
        }

        .statement-grid,
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1.18rem;
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
        .skill-card,
        .quote-panel,
        .contact-panel,
        .logo-card {
            position: relative;
            backdrop-filter: blur(16px) saturate(125%);
            -webkit-backdrop-filter: blur(16px) saturate(125%);
            isolation: isolate;
        }

        .statement-card::before,
        .skill-card::before,
        .quote-panel::before,
        .contact-panel::before,
        .logo-card::before {
            content: "";
            position: absolute;
            inset: 1px 1px auto 1px;
            height: 42%;
            border-radius: inherit;
            background: linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0));
            pointer-events: none;
            z-index: 0;
        }

        .statement-card,
        .skill-card {
            padding: 1.58rem 1.62rem;
            transition: transform 0.26s ease, border-color 0.26s ease, box-shadow 0.26s ease;
        }

        .statement-card:hover,
        .skill-card:hover {
            transform: translateY(-4px);
            border-color: rgba(201,176,137,0.28);
            box-shadow: 0 18px 44px rgba(0,0,0,0.24);
        }

        .statement-label,
        .section-label,
        .skill-label,
        .work-label,
        .contact-label {
            margin: 0 0 0.72rem 0;
            font-size: 0.76rem;
            letter-spacing: 0.26em;
            text-transform: uppercase;
            color: var(--gold);
        }

        .statement-text,
        .skill-text {
            margin: 0;
            color: var(--text);
            line-height: 1.82;
            font-size: 1.02rem;
        }

        .logo-band {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            overflow: hidden;
            padding-top: 0.2rem;
        }

        .logo-label {
            margin: 0;
            color: var(--gold);
            font-size: 0.76rem;
            letter-spacing: 0.26em;
            text-transform: uppercase;
        }

        .logo-track {
            display: flex;
            gap: 1.35rem;
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
            width: 156px;
            height: 84px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 24px;
            border: 1px solid rgba(201,176,137,0.12);
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.018));
            transition: transform 0.24s ease, background 0.24s ease;
        }

        .logo-card:hover {
            transform: translateY(-3px);
            background: linear-gradient(180deg, rgba(201,176,137,0.09), rgba(255,255,255,0.02));
        }

        .logo-card img {
            max-width: 96px;
            max-height: 38px;
            object-fit: contain;
            display: block;
            filter: grayscale(0%);
        }

        .section-heading {
            margin: 0;
            font-size: clamp(2.35rem, 4.4vw, 3.95rem);
            line-height: 1.04;
            letter-spacing: -0.03em;
            color: #faf5ed;
        }

        .section-copy {
            margin-top: 1.15rem;
            max-width: 46rem;
            color: var(--muted);
            line-height: 1.9;
            font-size: 1.04rem;
        }

        .work-card {
            min-height: 0.38rem;
            margin-top: 0.45rem;
            border-radius: 999px;
            border: 1px solid rgba(201,176,137,0.08);
            background: linear-gradient(90deg, rgba(255,255,255,0.015), rgba(201,176,137,0.06), rgba(255,255,255,0.015));
            box-shadow: none;
        }

        .work-title {
            margin: 0;
            font-size: 1.72rem;
            line-height: 1.04;
            color: #faf5ed;
        }

        .work-role {
            margin-top: 0.36rem;
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.56;
        }

        .work-summary {
            margin-top: 0.68rem;
            color: var(--text);
            font-size: 0.94rem;
            line-height: 1.58;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .tag-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.42rem;
            margin-top: 0.75rem;
        }

        .tag {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            border: 1px solid rgba(201,176,137,0.18);
            background: rgba(201,176,137,0.08);
            padding: 0.34rem 0.62rem;
            color: rgba(251,246,239,0.86);
            font-size: 0.76rem;
        }

        .work-link {
            margin-top: 0.48rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 2.2rem;
            border-radius: 14px;
            border: 1px solid rgba(201,176,137,0.18);
            background: rgba(255,255,255,0.015);
            color: var(--text) !important;
            text-decoration: none;
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            transition: border-color 0.22s ease, background 0.22s ease, transform 0.22s ease;
        }

        .work-link:hover {
            border-color: rgba(201,176,137,0.34);
            background: rgba(201,176,137,0.08);
            transform: translateY(-1px);
        }

        .quote-panel {
            margin-top: 0.9rem;
            padding: 4.35rem 3rem;
            text-align: center;
            background:
                radial-gradient(circle at top center, rgba(201,176,137,0.08), transparent 40%),
                linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
            display: flex;
            flex-direction: column;
            gap: 0.7rem;
            align-items: center;
        }

        .quote-text {
            max-width: 52rem;
            margin: 0;
            color: #faf5ed;
            font-size: clamp(2.15rem, 3.8vw, 3.45rem);
            line-height: 1.3;
            font-weight: 600;
        }

        .contact-gap {
            height: 1.65rem;
        }

        .contact-panel {
            padding: 2.45rem;
        }

        .contact-value {
            margin: 0 0 1.12rem 0;
            color: var(--text);
            font-size: 1.02rem;
            line-height: 1.78;
        }

        .contact-value:last-child {
            margin-bottom: 0;
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

            .site-shell {
                gap: 4.1rem;
            }

            .topbar {
                flex-direction: column;
                align-items: flex-start;
                position: static;
                border-radius: 30px;
            }

            .hero {
                min-height: 35rem;
            }

            .hero-content {
                min-height: 35rem;
                padding: 2.35rem;
            }

            .hero::after,
            .hero-media,
            .hero-content,
            [data-parallax-speed] {
                transform: none !important;
                transition: none !important;
                will-change: auto;
            }

            .hero h1 {
                font-size: clamp(3.4rem, 12vw, 5rem);
            }

            .hero-statement {
                font-size: 1.18rem;
            }

            .section-heading {
                font-size: clamp(2.1rem, 7vw, 3rem);
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


def render_statements(content: dict[str, Any]) -> None:
    cards = ['<div class="statement-grid fade-up">']
    for item in content["statements"]:
        label = item["label"] if isinstance(item, dict) else "Erfahrung"
        text = item["text"] if isinstance(item, dict) else item
        cards.append(
            f'<div class="statement-card"><p class="statement-label">{html.escape(label)}</p>'
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
        <section class="logo-band fade-up" data-parallax-speed="0.06">
            <p class="logo-label">Kunden aus dem FrameArt-Umfeld</p>
            <div class="logo-track">{repeated}</div>
        </section>
        """
    )


def render_selected_work_intro() -> None:
    render_html('<div class="section-label">Selected Work</div>')
    render_html('<h2 class="section-heading">Drei Projekte im Blick. Der Rest im horizontalen Film-Strip.</h2>')
    render_html(
        '<p class="section-copy">Die ersten Arbeiten sind sofort sichtbar. Weitere Projekte lassen sich seitlich durchscrollen, damit die Seite kompakter bleibt und trotzdem alles zeigen kann.</p>'
    )


def render_selected_work(content: dict[str, Any]) -> None:
    render_selected_work_intro()
    cards = []
    for project in content["projects"]:
        embed_url = video_embed_url(project["video_url"]) or project["video_url"]
        cards.append(
            f"""
            <article class="slider-card">
                <div class="slider-video-shell">
                    <iframe
                        src="{html.escape(embed_url, quote=True)}"
                        title="{html.escape(project["title"])}"
                        loading="lazy"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        allowfullscreen
                    ></iframe>
                </div>
                <div class="slider-copy">
                    <p class="slider-label">{html.escape(project["category"])}</p>
                    <h3>{html.escape(project["title"])}</h3>
                    <p class="slider-role">{html.escape(project["role"])}</p>
                    <p class="slider-summary">{html.escape(project["summary"])}</p>
                    <a class="slider-link" href="{html.escape(project["video_url"], quote=True)}" target="_blank" rel="noreferrer">Original öffnen</a>
                </div>
            </article>
            """
        )

    components.html(
        f"""
        <style>
            html, body {{
                margin: 0;
                background: transparent;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                color: #f3ede4;
            }}

            .slider-shell {{
                display: flex;
                flex-direction: column;
                gap: 1.15rem;
                padding-top: 0.35rem;
                position: relative;
            }}

            .slider-note {{
                margin: 0;
                color: rgba(243,237,228,0.54);
                font-size: 0.8rem;
                letter-spacing: 0.14em;
                text-transform: uppercase;
            }}

            .slider-track-wrap {{
                position: relative;
            }}

            .slider-track-wrap::before,
            .slider-track-wrap::after {{
                content: "";
                position: absolute;
                top: 0;
                bottom: 0.75rem;
                width: 42px;
                z-index: 3;
                pointer-events: none;
            }}

            .slider-track-wrap::before {{
                left: 0;
                background: linear-gradient(90deg, rgba(17,15,15,0.98), rgba(17,15,15,0));
            }}

            .slider-track-wrap::after {{
                right: 0;
                background: linear-gradient(270deg, rgba(17,15,15,0.98), rgba(17,15,15,0));
            }}

            .slider-track {{
                display: grid;
                grid-auto-flow: column;
                grid-auto-columns: calc((100% - 2.5rem) / 3);
                gap: 1.25rem;
                overflow-x: auto;
                padding: 0.15rem 0 0.85rem;
                scroll-snap-type: x mandatory;
                scrollbar-width: thin;
                scrollbar-color: rgba(201,176,137,0.36) transparent;
            }}

            .slider-track::-webkit-scrollbar {{
                height: 8px;
            }}

            .slider-track::-webkit-scrollbar-thumb {{
                background: rgba(201,176,137,0.34);
                border-radius: 999px;
            }}

            .slider-card {{
                scroll-snap-align: start;
                border-radius: 28px;
                border: 1px solid rgba(201,176,137,0.12);
                background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.02));
                overflow: hidden;
                box-shadow: 0 18px 46px rgba(0,0,0,0.2);
                transition: transform 0.26s ease, border-color 0.26s ease, box-shadow 0.26s ease;
            }}

            .slider-card:hover {{
                transform: translateY(-4px);
                border-color: rgba(201,176,137,0.26);
                box-shadow: 0 24px 58px rgba(0,0,0,0.24);
            }}

            .slider-video-shell {{
                aspect-ratio: 16 / 9;
                background: #0f0d0c;
            }}

            .slider-video-shell iframe {{
                width: 100%;
                height: 100%;
                border: 0;
                display: block;
            }}

            .slider-copy {{
                padding: 1.18rem 1.18rem 1.22rem;
            }}

            .slider-label {{
                margin: 0 0 0.52rem 0;
                font-size: 0.74rem;
                letter-spacing: 0.24em;
                text-transform: uppercase;
                color: #c9b089;
            }}

            .slider-copy h3 {{
                margin: 0;
                font-size: 1.24rem;
                line-height: 1.16;
                color: #faf5ed;
            }}

            .slider-role {{
                margin: 0.52rem 0 0 0;
                color: rgba(243,237,228,0.66);
                font-size: 0.85rem;
                line-height: 1.58;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}

            .slider-summary {{
                margin: 0.75rem 0 0 0;
                color: rgba(243,237,228,0.84);
                font-size: 0.92rem;
                line-height: 1.65;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}

            .slider-link {{
                margin-top: 0.95rem;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                min-height: 2.35rem;
                border-radius: 15px;
                border: 1px solid rgba(201,176,137,0.18);
                background: rgba(255,255,255,0.018);
                color: #f3ede4;
                text-decoration: none;
                font-size: 0.79rem;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease;
            }}

            .slider-link:hover {{
                border-color: rgba(201,176,137,0.34);
                background: rgba(201,176,137,0.08);
                transform: translateY(-1px);
            }}

            @media (max-width: 980px) {{
                .slider-track {{
                    grid-auto-columns: calc((100% - 1.25rem) / 2);
                }}
            }}

            @media (max-width: 720px) {{
                .slider-track-wrap::before,
                .slider-track-wrap::after {{
                    width: 24px;
                }}

                .slider-track {{
                    grid-auto-columns: 92%;
                }}
            }}
        </style>
        <div class="slider-shell">
            <p class="slider-note">Drei Projekte im Blick. Seitlich scrollen für mehr.</p>
            <div class="slider-track-wrap">
                <div class="slider-track">
                    {"".join(cards)}
                </div>
            </div>
        </div>
        """,
        height=590,
    )


def render_experience(content: dict[str, Any]) -> None:
    render_html('<div class="section-label">Background</div>')
    render_html('<h2 class="section-heading">Ausbildung, Set-Erfahrung, eigene GmbH.</h2>')
    render_html(
        '<p class="section-copy">Die Kombination aus Ausbildung bei FrameArt Media, europaweiter Produktionspraxis und späterer Verantwortung als Gesellschafter und Geschäftsführer sorgt dafür, dass Kamera, Licht, Ton, Postproduktion und Kundenlogik zusammen gedacht werden.</p>'
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
        <div class="quote-panel fade-up" data-parallax-speed="0.1">
            <p class="quote-text">Ich kenne Produktion nicht nur aus einer Rolle.</p>
            <p class="quote-text">Ich kenne sie von der Ausbildung bis zur Geschäftsführung.</p>
        </div>
        """
    )


def render_parallax_effects() -> None:
    components.html(
        """
        <script>
            const parentWindow = window.parent;
            const parentDocument = parentWindow.document;
            const cleanupKey = "__timPortfolioParallaxCleanup";
            const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

            if (parentWindow[cleanupKey]) {
                parentWindow[cleanupKey]();
            }

            const clearParallax = () => {
                const hero = parentDocument.querySelector(".hero");
                if (hero) {
                    hero.style.removeProperty("--hero-media-offset");
                    hero.style.removeProperty("--hero-content-offset");
                    hero.style.removeProperty("--hero-glow-offset");
                    hero.style.removeProperty("--hero-media-scale");
                }

                parentDocument.querySelectorAll("[data-parallax-speed]").forEach((element) => {
                    element.style.removeProperty("--parallax-offset");
                });
            };

            let frame = null;

            const updateParallax = () => {
                frame = null;
                const prefersReducedMotion = parentWindow.matchMedia("(prefers-reduced-motion: reduce)").matches;
                const enableParallax = parentWindow.innerWidth > 960 && !prefersReducedMotion;

                if (!enableParallax) {
                    clearParallax();
                    return;
                }

                const viewportHeight = parentWindow.innerHeight;
                const hero = parentDocument.querySelector(".hero");

                if (hero) {
                    const rect = hero.getBoundingClientRect();
                    const centerOffset = rect.top + rect.height / 2 - viewportHeight / 2;
                    const normalized = clamp(centerOffset / viewportHeight, -1.2, 1.2);

                    hero.style.setProperty("--hero-media-offset", `${normalized * -48}px`);
                    hero.style.setProperty("--hero-content-offset", `${normalized * 18}px`);
                    hero.style.setProperty("--hero-glow-offset", `${normalized * -30}px`);
                    hero.style.setProperty("--hero-media-scale", `${1.05 + Math.abs(normalized) * 0.035}`);
                }

                parentDocument.querySelectorAll("[data-parallax-speed]").forEach((element) => {
                    const rect = element.getBoundingClientRect();
                    const centerOffset = rect.top + rect.height / 2 - viewportHeight / 2;
                    const speed = Number(element.dataset.parallaxSpeed || "0.08");
                    const offset = clamp(centerOffset * speed * -1, -42, 42);
                    element.style.setProperty("--parallax-offset", `${offset}px`);
                });
            };

            const requestUpdate = () => {
                if (frame !== null) {
                    return;
                }
                frame = parentWindow.requestAnimationFrame(updateParallax);
            };

            const observer = new parentWindow.MutationObserver(requestUpdate);
            observer.observe(parentDocument.body, { childList: true, subtree: true });

            parentWindow.addEventListener("scroll", requestUpdate, { passive: true });
            parentWindow.addEventListener("resize", requestUpdate);

            parentWindow[cleanupKey] = () => {
                if (frame !== null) {
                    parentWindow.cancelAnimationFrame(frame);
                    frame = null;
                }
                observer.disconnect();
                parentWindow.removeEventListener("scroll", requestUpdate);
                parentWindow.removeEventListener("resize", requestUpdate);
            };

            requestUpdate();
        </script>
        """,
        height=0,
    )


def render_contact(content: dict[str, Any]) -> None:
    site = content["site"]
    contact = content["contact"]
    render_html('<div class="contact-gap" aria-hidden="true"></div>')
    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        render_html('<div class="section-label">Kontakt</div>')
        render_html(f'<h2 class="section-heading">{html.escape(site["title"])}</h2>')
        render_html(f'<p class="section-copy">{html.escape(site["subtitle"])}<br>{html.escape(site["location"])}</p>')
    with right:
        contact_markup = [
            '<div class="contact-panel fade-up">',
            '<div class="contact-label">Mail</div>',
            f'<p class="contact-value">{html.escape(contact["email"])}</p>',
            '<div class="contact-label">Telefon</div>',
            f'<p class="contact-value">{html.escape(contact["phone"])}</p>',
        ]
        if contact.get("website"):
            contact_markup.append('<div class="contact-label">Website</div>')
            contact_markup.append(
                f'<p class="contact-value"><a class="site-link" href="{html.escape(contact["website"], quote=True)}" target="_blank">{html.escape(contact["website"])}</a></p>'
            )
        contact_markup.append(f'<p class="contact-value">{html.escape(contact["note"])}</p>')
        contact_markup.append('</div>')
        render_html("".join(contact_markup))


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
    render_parallax_effects()


if __name__ == "__main__":
    main()
