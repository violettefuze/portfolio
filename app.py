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


def file_download_href(path: Path, mime_type: str) -> str | None:
    if not path.exists():
        return None
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


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
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/")[2]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/")[2]
        return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1" if video_id else None

    if "vimeo.com" in host:
        segments = [segment for segment in parsed.path.split("/") if segment]
        video_id = next((segment for segment in segments if segment.isdigit()), None)
        return f"https://player.vimeo.com/video/{video_id}" if video_id else None

    return None


def render_video_player(url: str, title: str, height: int = 560) -> None:
    embed_url = video_embed_url(url)
    if not embed_url:
        st.link_button("Film öffnen", url, width="stretch")
        return

    safe_title = html.escape(title)
    safe_url = html.escape(embed_url, quote=True)
    components.html(
        f"""
        <style>
            html, body {{
                margin: 0;
                background: transparent;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }}

            .video-shell {{
                position: relative;
                width: 100%;
                height: 100%;
                border-radius: 34px;
                overflow: hidden;
                border: 1px solid rgba(0, 0, 0, 0.08);
                background:
                    radial-gradient(circle at top, rgba(180, 139, 74, 0.16), transparent 40%),
                    linear-gradient(180deg, rgba(255,255,255,0.92), rgba(255,255,255,0.84));
                box-shadow: 0 34px 90px rgba(15, 23, 42, 0.16);
                padding: 14px;
            }}

            .video-frame {{
                position: relative;
                width: 100%;
                height: 100%;
                border-radius: 24px;
                overflow: hidden;
                background: #0e1016;
            }}

            iframe {{
                width: 100%;
                height: 100%;
                border: 0;
                display: block;
            }}
        </style>
        <div class="video-shell">
            <div class="video-frame">
                <iframe
                    src="{safe_url}"
                    title="{safe_title}"
                    loading="lazy"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen
                ></iframe>
            </div>
        </div>
        """,
        height=height,
    )


def featured_project(content: dict[str, Any]) -> dict[str, Any]:
    target_slug = content["site"].get("featured_project_slug")
    for project in content["projects"]:
        if project["slug"] == target_slug:
            return project
    return content["projects"][0]


def project_preview_path(project: dict[str, Any]) -> Path | None:
    image_path = project.get("hero_image")
    if image_path:
        return ROOT / image_path
    stills = project.get("stills") or []
    if stills:
        return ROOT / stills[0]
    return None


def section_intro(label: str, title: str, copy: str, *, anchor: str | None = None, centered: bool = False) -> None:
    anchor_attr = f' id="{anchor}"' if anchor else ""
    classes = "section-head section-head-center" if centered else "section-head"
    render_html(
        f"""
        <section{anchor_attr} class="{classes}">
            <p class="section-kicker">{html.escape(label)}</p>
            <h2 class="section-title">{html.escape(title)}</h2>
            <p class="section-copy">{html.escape(copy)}</p>
        </section>
        """
    )


def inject_css() -> None:
    render_html(
        """
        <style>
        :root {
            --bg: #f5f5f7;
            --bg-soft: #fbf7f1;
            --panel: rgba(255, 255, 255, 0.76);
            --panel-strong: rgba(255, 255, 255, 0.92);
            --line: rgba(15, 23, 42, 0.08);
            --line-strong: rgba(180, 139, 74, 0.26);
            --ink: #121316;
            --ink-soft: #525866;
            --gold: #b48b4a;
            --gold-soft: rgba(180, 139, 74, 0.12);
            --shadow: 0 34px 90px rgba(15, 23, 42, 0.12);
            --shadow-soft: 0 16px 48px rgba(15, 23, 42, 0.08);
        }

        html, body, [data-testid="stAppViewContainer"] {
            scroll-behavior: smooth;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(180, 139, 74, 0.12), transparent 24%),
                radial-gradient(circle at top right, rgba(255, 255, 255, 0.72), transparent 26%),
                linear-gradient(180deg, #f7f6f3 0%, #f5f5f7 48%, #f4efe8 100%);
            color: var(--ink);
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }

        #MainMenu, footer, header[data-testid="stHeader"] {
            visibility: hidden;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1rem;
            padding-bottom: 6rem;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stButton > button,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stDownloadButton > button,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stLinkButton > a {
            width: 100%;
            min-height: 3.25rem;
            border-radius: 999px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(247,247,249,0.9));
            color: var(--ink);
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            text-decoration: none;
            transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
        }

        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stButton > button:hover,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stDownloadButton > button:hover,
        [data-testid="stVerticalBlock"] > [data-testid="element-container"] div.stLinkButton > a:hover {
            transform: translateY(-1px);
            border-color: var(--line-strong);
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.12);
        }

        .site-shell {
            display: flex;
            flex-direction: column;
            gap: 6rem;
        }

        .topbar-wrap {
            position: sticky;
            top: 0.7rem;
            z-index: 30;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1.5rem;
            padding: 0.9rem 1.1rem;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.78);
            background: rgba(255,255,255,0.68);
            backdrop-filter: blur(20px);
            box-shadow: var(--shadow-soft);
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            gap: 0.9rem;
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

        .brand-copy {
            display: flex;
            flex-direction: column;
            gap: 0.12rem;
        }

        .brand-title {
            margin: 0;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--ink);
        }

        .brand-subtitle {
            margin: 0;
            font-size: 0.74rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--ink-soft);
        }

        .nav-copy {
            display: flex;
            align-items: center;
            gap: 1.1rem;
            flex-wrap: wrap;
        }

        .nav-copy a {
            color: var(--ink-soft);
            text-decoration: none;
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            transition: color 0.2s ease;
        }

        .nav-copy a:hover {
            color: var(--ink);
        }

        .hero-shell {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .hero-intro {
            max-width: 56rem;
            margin: 0 auto;
            text-align: center;
            padding-top: 2.8rem;
            animation: rise 0.9s ease both;
        }

        .hero-kicker {
            margin: 0 0 1rem 0;
            color: var(--gold);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.34em;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 0;
            color: var(--ink);
            font-size: clamp(3.8rem, 9vw, 7.6rem);
            line-height: 0.93;
            letter-spacing: -0.065em;
        }

        .hero-statement {
            margin: 1.15rem auto 0 auto;
            max-width: 42rem;
            color: var(--ink);
            font-size: clamp(1.35rem, 2.8vw, 2.15rem);
            line-height: 1.16;
            letter-spacing: -0.04em;
        }

        .hero-copy {
            margin: 1rem auto 0 auto;
            max-width: 40rem;
            color: var(--ink-soft);
            font-size: 1.05rem;
            line-height: 1.85;
        }

        .hero-frame {
            position: relative;
            overflow: hidden;
            border-radius: 42px;
            border: 1px solid rgba(255,255,255,0.82);
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(255,255,255,0.72));
            box-shadow: var(--shadow);
            animation: rise 1.05s ease both;
        }

        .hero-frame::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0)),
                radial-gradient(circle at top, rgba(180,139,74,0.16), transparent 42%);
            pointer-events: none;
            z-index: 1;
        }

        .hero-frame img {
            display: block;
            width: 100%;
            aspect-ratio: 2.36 / 1;
            object-fit: cover;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
        }

        .action-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
        }

        .action-button {
            min-height: 3.35rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(247,247,249,0.9));
            color: var(--ink);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            text-decoration: none;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
            transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
        }

        .action-button:hover {
            transform: translateY(-1px);
            border-color: var(--line-strong);
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.12);
        }

        .metric-card,
        .glass-card,
        .principle-card,
        .review-card,
        .background-card,
        .contact-card {
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.84);
            background:
                linear-gradient(180deg, rgba(255,255,255,0.96), rgba(249,249,251,0.84));
            box-shadow: var(--shadow-soft);
        }

        .metric-card {
            padding: 1.55rem;
            animation: rise 1.1s ease both;
        }

        .metric-title {
            margin: 0;
            color: var(--gold);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.2em;
            text-transform: uppercase;
        }

        .metric-value {
            margin: 0.6rem 0 0 0;
            color: var(--ink);
            font-size: 1.55rem;
            line-height: 1.08;
            letter-spacing: -0.04em;
        }

        .metric-copy {
            margin: 0.75rem 0 0 0;
            color: var(--ink-soft);
            font-size: 0.97rem;
            line-height: 1.72;
        }

        .section-head {
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
        }

        .section-head-center {
            align-items: center;
            text-align: center;
        }

        .section-kicker {
            margin: 0;
            color: var(--gold);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.3em;
            text-transform: uppercase;
        }

        .section-title {
            margin: 0;
            color: var(--ink);
            font-size: clamp(2.2rem, 5vw, 4.1rem);
            line-height: 0.98;
            letter-spacing: -0.055em;
            max-width: 15ch;
        }

        .section-head-center .section-title {
            max-width: 11ch;
        }

        .section-copy {
            margin: 0;
            max-width: 42rem;
            color: var(--ink-soft);
            font-size: 1.02rem;
            line-height: 1.82;
        }

        .story-card,
        .skills-card,
        .proof-card,
        .work-card,
        .detail-card {
            padding: 1.7rem 1.75rem;
        }

        .story-card p,
        .detail-copy,
        .card-copy,
        .review-copy,
        .contact-copy,
        .background-copy {
            margin: 0;
            color: var(--ink-soft);
            font-size: 1rem;
            line-height: 1.85;
        }

        .story-card p + p,
        .background-copy + .background-copy {
            margin-top: 1rem;
        }

        .quote-line {
            margin-top: 1.5rem;
            color: var(--ink);
            font-size: 1.34rem;
            line-height: 1.32;
            letter-spacing: -0.04em;
        }

        .mini-title {
            margin: 0 0 0.9rem 0;
            color: var(--gold);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
        }

        .fact-list,
        .skill-list,
        .tag-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
        }

        .fact-pill,
        .skill-pill,
        .tag {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            border: 1px solid rgba(180,139,74,0.18);
            background: rgba(180,139,74,0.08);
            padding: 0.58rem 0.82rem;
            color: var(--ink);
            font-size: 0.86rem;
            line-height: 1.4;
        }

        .sticky-stack {
            position: sticky;
            top: 6rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .media-shell {
            overflow: hidden;
            border-radius: 34px;
            border: 1px solid rgba(255,255,255,0.84);
            background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(247,247,249,0.9));
            box-shadow: var(--shadow-soft);
        }

        .media-shell img {
            width: 100%;
            display: block;
            aspect-ratio: 16 / 10;
            object-fit: cover;
            transition: transform 0.8s ease;
        }

        .media-shell:hover img {
            transform: scale(1.04);
        }

        .detail-card h3,
        .work-card h3 {
            margin: 0;
            color: var(--ink);
            font-size: clamp(1.85rem, 3vw, 2.75rem);
            line-height: 1.02;
            letter-spacing: -0.045em;
        }

        .detail-meta,
        .work-meta {
            margin-top: 0.7rem;
            color: var(--ink-soft);
            font-size: 0.95rem;
            line-height: 1.7;
        }

        .detail-copy {
            margin-top: 1rem;
        }

        .parallax-band {
            position: relative;
            min-height: 34rem;
            display: flex;
            align-items: end;
            overflow: hidden;
            border-radius: 42px;
            border: 1px solid rgba(255,255,255,0.84);
            background-position: center center;
            background-size: cover;
            background-attachment: fixed;
            box-shadow: var(--shadow);
        }

        .parallax-band::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(180deg, rgba(17, 18, 24, 0.08), rgba(17, 18, 24, 0.48)),
                linear-gradient(90deg, rgba(17, 18, 24, 0.72), rgba(17, 18, 24, 0.08));
        }

        .parallax-copy-wrap {
            position: relative;
            z-index: 1;
            max-width: 38rem;
            padding: 2.6rem;
            color: white;
        }

        .parallax-kicker {
            margin: 0;
            color: rgba(255,255,255,0.72);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.24em;
            text-transform: uppercase;
        }

        .parallax-text {
            margin: 0.8rem 0 0 0;
            font-size: clamp(1.9rem, 4vw, 3.4rem);
            line-height: 1.02;
            letter-spacing: -0.05em;
        }

        .principle-card,
        .background-card,
        .review-card {
            padding: 1.55rem;
        }

        .principle-title,
        .background-title,
        .review-name {
            margin: 0;
            color: var(--ink);
            font-size: 1.16rem;
            line-height: 1.2;
            letter-spacing: -0.03em;
        }

        .principle-copy,
        .review-copy,
        .background-copy {
            margin-top: 0.78rem;
            color: var(--ink-soft);
            font-size: 0.98rem;
            line-height: 1.75;
        }

        .review-meta,
        .background-meta,
        .source-note {
            margin-top: 0.7rem;
            color: var(--ink-soft);
            font-size: 0.85rem;
            line-height: 1.65;
        }

        .proof-score {
            margin: 0.15rem 0 0 0;
            color: var(--ink);
            font-size: 4rem;
            line-height: 0.9;
            letter-spacing: -0.08em;
        }

        .proof-line {
            margin: 0.8rem 0 0 0;
            color: var(--ink-soft);
            font-size: 1rem;
            line-height: 1.72;
        }

        .source-note a,
        .site-link {
            color: var(--gold);
            text-decoration: none;
        }

        .source-note a:hover,
        .site-link:hover {
            text-decoration: underline;
        }

        .work-stack {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .meta-panel {
            border-radius: 34px;
            border: 1px solid rgba(255,255,255,0.82);
            background:
                linear-gradient(180deg, rgba(255,255,255,0.96), rgba(249,249,251,0.9));
            padding: 2rem;
            box-shadow: var(--shadow-soft);
        }

        .meta-panel p {
            margin: 0;
        }

        .meta-label {
            color: var(--gold);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
        }

        .meta-value {
            margin-top: 0.7rem;
            color: var(--ink);
            font-size: 1.4rem;
            line-height: 1.15;
            letter-spacing: -0.04em;
        }

        .meta-copy {
            margin-top: 0.75rem;
            color: var(--ink-soft);
            font-size: 0.98rem;
            line-height: 1.72;
        }

        .partner-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 1rem;
        }

        .partner-pill {
            min-height: 4.8rem;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.82);
            background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(249,249,251,0.9));
            box-shadow: var(--shadow-soft);
        }

        .partner-pill img {
            max-width: 100%;
            max-height: 2.4rem;
            object-fit: contain;
            display: block;
        }

        .contact-card {
            padding: 1.8rem;
        }

        .contact-label {
            margin: 0 0 0.25rem 0;
            color: var(--gold);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
        }

        .contact-value {
            margin: 0 0 1.1rem 0;
            color: var(--ink);
            font-size: 1rem;
            line-height: 1.72;
        }

        .footer-note {
            color: var(--ink-soft);
            font-size: 0.9rem;
            line-height: 1.72;
        }

        .reveal {
            animation: rise 0.9s ease both;
        }

        @keyframes rise {
            from {
                opacity: 0;
                transform: translateY(22px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 1000px) {
            .action-row,
            .metrics-grid {
                grid-template-columns: 1fr;
            }

            .topbar {
                flex-direction: column;
                align-items: flex-start;
                border-radius: 28px;
            }

            .sticky-stack {
                position: static;
            }

            .parallax-band {
                min-height: 26rem;
                background-attachment: scroll;
            }
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 0.6rem;
                padding-bottom: 4rem;
            }

            .site-shell {
                gap: 4.5rem;
            }

            .hero-intro {
                padding-top: 2rem;
            }

            .hero-frame {
                border-radius: 28px;
            }

            .hero-frame img {
                aspect-ratio: 1.7 / 1;
            }

            .parallax-copy-wrap {
                padding: 1.6rem;
            }
        }
        </style>
        """
    )


def render_topbar(content: dict[str, Any]) -> None:
    site = content["site"]
    brand_mark_path = ROOT / site["brand_mark"] if site.get("brand_mark") else None
    brand_mark_uri = image_data_uri(brand_mark_path) if brand_mark_path else None
    brand_visual = ""
    if brand_mark_uri:
        brand_visual = (
            f'<div class="brand-logo"><img src="{brand_mark_uri}" alt="{html.escape(site["title"])} pictogram"></div>'
        )

    render_html(
        f"""
        <div class="topbar-wrap">
            <div class="topbar">
                <div class="brand-mark">
                    {brand_visual}
                    <div class="brand-copy">
                        <p class="brand-title">{html.escape(site["title"])}</p>
                        <p class="brand-subtitle">{html.escape(site["subtitle"])}</p>
                    </div>
                </div>
                <div class="nav-copy">
                    <a href="#featured-reel">Featured Reel</a>
                    <a href="#selected-work">Selected Work</a>
                    <a href="#reviews">Reviews</a>
                    <a href="#contact">Contact</a>
                </div>
            </div>
        </div>
        """
    )


def render_hero(content: dict[str, Any], project: dict[str, Any]) -> None:
    site = content["site"]
    proof = content["social_proof"]
    hero_uri = image_data_uri(ROOT / site["hero_image"])
    pdf_href = file_download_href(PDF_PATH, "application/pdf")
    hero_markup = ""
    if hero_uri:
        hero_markup = f'<div class="hero-frame"><img src="{hero_uri}" alt="Landing image for {html.escape(site["title"])}"></div>'

    action_button_markup = [
        f'<a class="action-button" href="{html.escape(project["video_url"], quote=True)}" target="_blank">Film abspielen</a>',
        f'<a class="action-button" href="{html.escape(content["contact"]["website"], quote=True)}" target="_blank">Website</a>',
    ]
    if pdf_href:
        action_button_markup.insert(
            1,
            f'<a class="action-button" href="{pdf_href}" download="{html.escape(PDF_PATH.name, quote=True)}">Bewerbungs-PDF</a>',
        )
    else:
        action_button_markup.insert(1, '<a class="action-button" href="#contact">Kontakt</a>')

    render_html(
        f"""
        <section id="top" class="hero-shell">
            <div class="hero-intro">
                <p class="hero-kicker">{html.escape(site["hero_kicker"])}</p>
                <h1 class="hero-title">{html.escape(site["title"])}</h1>
                <p class="hero-statement">{html.escape(site["hero_statement"])}</p>
                <p class="hero-copy">{html.escape(site["intro"])}</p>
            </div>
            {hero_markup}
            <div class="action-row">{''.join(action_button_markup)}</div>
        </section>
        """
    )

    metrics = [
        {
            "title": "Fundament",
            "value": "Werbefilmproduktion",
            "copy": "Praxis in Kamera, Licht, Postproduktion und realen Produktionsabläufen.",
        },
        {
            "title": "Featured Motion",
            "value": project["title"],
            "copy": project["summary"],
        },
        {
            "title": "Öffentliche Resonanz",
            "value": f'{proof["rating"]} / 5',
            "copy": f'{proof["count"]} {proof["platform"]} mit Fokus auf Qualität, Zuverlässigkeit und Zusammenarbeit.',
        },
    ]
    metrics_markup = ['<div class="metrics-grid">']
    for metric in metrics:
        metrics_markup.append(
            f'<div class="metric-card"><p class="metric-title">{html.escape(metric["title"])}</p>'
            f'<p class="metric-value">{html.escape(metric["value"])}</p>'
            f'<p class="metric-copy">{html.escape(metric["copy"])}</p></div>'
        )
    metrics_markup.append("</div>")
    render_html("".join(metrics_markup))


def render_story(content: dict[str, Any]) -> None:
    section_intro(
        "Profil",
        content["about"]["headline"],
        "Die Seite soll wie eine gute Produktseite funktionieren: klar, ruhig und mit genug Raum, damit Arbeit und Haltung glaubwürdig wirken.",
    )

    left, right = st.columns([1.618, 1], gap="large")
    with left:
        story_markup = ['<div class="glass-card story-card reveal">']
        for paragraph in content["about"]["paragraphs"]:
            story_markup.append(f'<p>{html.escape(paragraph)}</p>')
        story_markup.append('<p class="quote-line">Viele Filme sind technisch sauber. Interessant werden sie erst, wenn Haltung, Timing und Licht zusammenspielen.</p>')
        story_markup.append("</div>")
        render_html("".join(story_markup))

    with right:
        facts = ['<div class="glass-card skills-card"><p class="mini-title">Kurzprofil</p><div class="fact-list">']
        for fact in content["about"]["facts"]:
            facts.append(f'<span class="fact-pill">{html.escape(fact)}</span>')
        facts.append("</div></div>")

        skills = ['<div class="glass-card skills-card"><p class="mini-title">Werkzeuge</p><div class="skill-list">']
        for item in content["skills"]["camera"] + content["skills"]["postproduction"]:
            skills.append(f'<span class="skill-pill">{html.escape(item)}</span>')
        skills.append("</div>")
        skills.append(f'<p class="detail-copy" style="margin-top: 1rem;">{html.escape(content["skills"]["focus"])}</p>')
        skills.append("</div>")

        render_html(f'<div class="sticky-stack">{"".join(facts)}{"".join(skills)}</div>')


def render_featured_reel(project: dict[str, Any]) -> None:
    section_intro(
        "Featured Reel",
        "Bewegung zuerst. Alles andere danach.",
        "Der erste Blick soll nicht nach Portfolio schreien, sondern nach Qualität aussehen. Deshalb steht ein Film zentral und nicht fünf gleich laute Projekte nebeneinander.",
        anchor="featured-reel",
        centered=True,
    )

    left, right = st.columns([1.618, 1], gap="large")
    with left:
        render_video_player(project["video_url"], project["title"])

    with right:
        tags = "".join(f'<span class="tag">{html.escape(note)}</span>' for note in project.get("notes", []))
        render_html(
            f"""
            <div class="glass-card detail-card">
                <p class="mini-title">Jetzt im Fokus</p>
                <h3>{html.escape(project["title"])}</h3>
                <p class="detail-meta">{html.escape(project["category"])} · {html.escape(project["role"])}</p>
                <p class="detail-copy">{html.escape(project["summary"])}</p>
                <div class="tag-row">{tags}</div>
                <p class="source-note">Direkte Wiedergabe über YouTube.</p>
            </div>
            """
        )
        st.link_button("Original öffnen", project["video_url"], width="stretch")


def render_parallax_band(content: dict[str, Any]) -> None:
    hero_uri = image_data_uri(ROOT / content["site"]["hero_image"])
    background_style = f"background-image: url('{hero_uri}');" if hero_uri else ""
    render_html(
        f"""
        <section class="parallax-band reveal" style="{background_style}">
            <div class="parallax-copy-wrap">
                <p class="parallax-kicker">Rhythmus statt Lautstärke</p>
                <p class="parallax-text">Eine gute Seite braucht dieselbe Ruhe wie ein gutes Bild: Fokus, Luft und klare Prioritäten.</p>
            </div>
        </section>
        """
    )


def render_process(content: dict[str, Any]) -> None:
    section_intro(
        "Arbeitsweise",
        "Wie die Arbeit aufgebaut ist.",
        "Nicht alles muss maximal auffallen. Oft wirkt eine Produktion stärker, wenn Vorbereitung, Set-Ruhe und Postproduktion so ineinandergreifen, dass es selbstverständlich aussieht.",
        centered=True,
    )

    cols = st.columns(3, gap="large")
    for col, item in zip(cols, content["process"]):
        with col:
            render_html(
                f"""
                <div class="principle-card reveal">
                    <p class="mini-title">{html.escape(item["title"])}</p>
                    <p class="principle-title">{html.escape(item["title"])}</p>
                    <p class="principle-copy">{html.escape(item["text"])}</p>
                </div>
                """
            )


def render_reviews(content: dict[str, Any]) -> None:
    proof = content["social_proof"]
    section_intro(
        "Reviews",
        "Gute Rückmeldungen helfen nur, wenn sie echt wirken.",
        "Darum steht hier nicht bloß eine Zahl, sondern ein kurzer Eindruck davon, was Menschen über Zusammenarbeit und Ergebnis öffentlich zurückmelden.",
        anchor="reviews",
        centered=True,
    )

    cols = st.columns([0.95, 1, 1, 1], gap="large")
    with cols[0]:
        render_html(
            f"""
            <div class="glass-card proof-card reveal">
                <p class="mini-title">{html.escape(proof["platform"])}</p>
                <p class="proof-score">{html.escape(proof["rating"])}</p>
                <p class="proof-line">{html.escape(str(proof["count"]))} öffentliche Bewertungen</p>
                <p class="proof-line">{html.escape(proof["summary"])}</p>
                <p class="source-note">
                    Stand: {html.escape(proof["checked_on"])}<br>
                    Quelle: <a href="{html.escape(proof["source_url"], quote=True)}" target="_blank">{html.escape(proof["source_label"])}</a>
                </p>
            </div>
            """
        )

    for col, item in zip(cols[1:], content["testimonials"]):
        with col:
            render_html(
                f"""
                <div class="review-card reveal">
                    <p class="review-name">{html.escape(item["name"])}</p>
                    <p class="review-meta">{html.escape(item["meta"])}</p>
                    <p class="review-copy">{html.escape(item["text"])}</p>
                </div>
                """
            )


def render_background(content: dict[str, Any]) -> None:
    section_intro(
        "Production Background",
        "Woher der Blick kommt.",
        "Die Arbeit soll nicht so tun, als käme sie aus dem Nichts. Sie ist gewachsen aus Set-Erfahrung, Eigenverantwortung und einem klareren Verständnis davon, worauf es wirklich ankommt.",
    )

    cols = st.columns(3, gap="large")
    for col, item in zip(cols, content["background"]):
        with col:
            link_markup = ""
            if item.get("link_url"):
                link_markup = (
                    f'<p class="source-note"><a class="site-link" href="{html.escape(item["link_url"], quote=True)}" target="_blank">'
                    f'{html.escape(item["link_label"])}</a></p>'
                )
            render_html(
                f"""
                <div class="background-card reveal">
                    <p class="mini-title">{html.escape(item["title"])}</p>
                    <p class="background-title">{html.escape(item["title"])}</p>
                    <p class="background-copy">{html.escape(item["text"])}</p>
                    {link_markup}
                </div>
                """
            )


def render_projects(content: dict[str, Any], featured_slug: str) -> None:
    section_intro(
        "Selected Work",
        "Weitere Arbeiten, sauber gruppiert.",
        "Nicht jeder Film muss direkt auf der Startseite losspielen. Die Auswahl darunter zeigt Bandbreite, ohne die Seite zu überladen.",
        anchor="selected-work",
        centered=True,
    )

    for index, project in enumerate(content["projects"]):
        if project["slug"] == featured_slug:
            continue

        preview_path = project_preview_path(project)
        preview_uri = image_data_uri(preview_path) if preview_path else None
        notes = "".join(f'<span class="tag">{html.escape(note)}</span>' for note in project.get("notes", []))

        left, right = st.columns([1.618, 1], gap="large")
        media_col, text_col = (left, right) if index % 2 == 0 else (right, left)

        with media_col:
            if preview_uri:
                render_html(
                    f"""
                    <div class="media-shell reveal">
                        <img src="{preview_uri}" alt="{html.escape(project["title"])} preview">
                    </div>
                    """
                )
            else:
                render_html(
                    f"""
                    <div class="meta-panel reveal">
                        <p class="meta-label">{html.escape(project["category"])}</p>
                        <p class="meta-value">{html.escape(project["title"])}</p>
                        <p class="meta-copy">{html.escape(project["role"])}</p>
                    </div>
                    """
                )

        with text_col:
            render_html(
                f"""
                <div class="glass-card work-card reveal">
                    <p class="mini-title">{html.escape(project["category"])}</p>
                    <h3>{html.escape(project["title"])}</h3>
                    <p class="work-meta">{html.escape(project["role"])}</p>
                    <p class="detail-copy">{html.escape(project["summary"])}</p>
                    <div class="tag-row">{notes}</div>
                </div>
                """
            )
            st.link_button("Film öffnen", project["video_url"], width="stretch")


def render_partners(content: dict[str, Any]) -> None:
    partners = content.get("partners") or []
    if not partners:
        return

    section_intro(
        "Zusammenarbeit",
        "Mit wem bereits gearbeitet wurde.",
        "Wenn du mir Logos gibst, kann dieser Block Größe und Vertrauen sehr schnell sichtbar machen.",
        centered=True,
    )

    cards = ['<div class="partner-grid">']
    for partner in partners:
        logo_path = ROOT / partner["logo"]
        logo_uri = image_data_uri(logo_path) if logo_path.exists() else None
        if logo_uri:
            cards.append(
                f'<div class="partner-pill"><img src="{logo_uri}" alt="{html.escape(partner["name"])} logo"></div>'
            )
    cards.append("</div>")
    render_html("".join(cards))


def render_contact(content: dict[str, Any]) -> None:
    site = content["site"]
    contact = content["contact"]
    section_intro(
        "Kontakt",
        "Wenn du magst, bauen wir den nächsten Block direkt mit.",
        "Die Seite ist jetzt so angelegt, dass weitere Logos, zusätzliche Referenzen oder neue Featured-Arbeiten sauber ergänzt werden können, ohne das System neu zu bauen.",
        anchor="contact",
    )

    left, right = st.columns([1.3, 0.9], gap="large")
    with left:
        render_html(
            f"""
            <div class="glass-card story-card reveal">
                <p class="mini-title">{html.escape(site["title"])}</p>
                <p class="quote-line">Filmmaker, Kamera, Licht, Schnitt und Color mit Blick für Wirkung statt bloßer Oberfläche.</p>
                <p class="card-copy" style="margin-top: 1rem;">{html.escape(site["location"])}</p>
                <p class="footer-note" style="margin-top: 1rem;">Logos von bisherigen Zusammenarbeiten kann ich als nächsten Schritt direkt in einen eigenen Social-Proof-Block integrieren.</p>
            </div>
            """
        )

    with right:
        render_html(
            f"""
            <div class="contact-card reveal">
                <p class="contact-label">Mail</p>
                <p class="contact-value">{html.escape(contact["email"])}</p>
                <p class="contact-label">Telefon</p>
                <p class="contact-value">{html.escape(contact["phone"])}</p>
                <p class="contact-label">Website</p>
                <p class="contact-value"><a class="site-link" href="{html.escape(contact["website"], quote=True)}" target="_blank">{html.escape(contact["website"])}</a></p>
                <p class="footer-note">{html.escape(contact["note"])}</p>
            </div>
            """
        )


def main() -> None:
    st.set_page_config(
        page_title="Tim Heid | Portfolio",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    content = load_content()
    current_featured_project = featured_project(content)

    inject_css()
    render_html('<div class="site-shell">')
    render_topbar(content)
    render_hero(content, current_featured_project)
    render_story(content)
    render_featured_reel(current_featured_project)
    render_parallax_band(content)
    render_process(content)
    render_reviews(content)
    render_background(content)
    render_projects(content, current_featured_project["slug"])
    render_partners(content)
    render_contact(content)
    render_html("</div>")


if __name__ == "__main__":
    main()
