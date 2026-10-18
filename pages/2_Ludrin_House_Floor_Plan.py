import base64
import re

import pandas as pd
import streamlit as st


def show_svg(svg, max_width):
    head, rest = svg.split(">", 1)
    head = re.sub(r'\sstyle="[^"]*"', "", head)
    svg = head + ">" + rest
    if "width=" not in svg.split(">", 1)[0]:
        w, h = svg.split('viewBox="0 0 ', 1)[1].split('"', 1)[0].split()
        svg = svg.replace("<svg ", f'<svg width="{w}" height="{h}" ', 1)
    data = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    st.markdown(
        f'<img src="data:image/svg+xml;base64,{data}" style="width:100%;max-width:{max_width}px;height:auto;display:block" alt="">',
        unsafe_allow_html=True,
    )

BANNER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" font-family="Source Sans Pro, sans-serif" style="width:100%;height:auto;display:block;border-radius:12px">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0e1117"/><stop offset="1" stop-color="#1a2233"/>
    </linearGradient>
  </defs>
  <rect width="640" height="360" fill="url(#bg)"/>
  <text x="40" y="70" font-size="14" fill="#60a5fa" font-weight="bold" letter-spacing="2">PROJECT HUB</text>
  <text x="40" y="128" font-size="44" fill="#f3f4f6" font-weight="bold">Ludrin</text>
  <text x="40" y="178" font-size="44" fill="#f3f4f6" font-weight="bold">House</text>
  <text x="40" y="218" font-size="15" fill="#9aa0a6">TCG shop, play hall,</text>
  <text x="40" y="240" font-size="15" fill="#9aa0a6">PC room and kitchen</text>
  <g font-size="12" fill="#cbd5e1">
    <rect x="40" y="276" width="118" height="30" rx="15" fill="none" stroke="#60a5fa"/>
    <text x="99" y="296" text-anchor="middle">Business model</text>
    <rect x="168" y="276" width="96" height="30" rx="15" fill="none" stroke="#60a5fa"/>
    <text x="216" y="296" text-anchor="middle">Floor plan</text>
  </g>
  
  <g transform="translate(330,48)" stroke="#6b7280" fill="none" stroke-width="1.5">
    <text x="0" y="0" font-size="11" fill="#9aa0a6" stroke="none">Ground floor</text>
    <rect x="0" y="10" width="270" height="110" rx="4"/>
    <line x1="95" y1="10" x2="95" y2="120"/>
    <rect x="8" y="22" width="5" height="88" fill="rgba(96,165,250,0.25)"/>
    <rect x="20" y="30" width="40" height="8" rx="2"/><rect x="20" y="46" width="40" height="8" rx="2"/><rect x="20" y="62" width="40" height="8" rx="2"/>
    <rect x="64" y="18" width="24" height="22" rx="3" stroke="#60a5fa" fill="rgba(96,165,250,0.15)"/>
    <g>
      <rect x="108" y="28" width="22" height="11" rx="2"/><rect x="140" y="28" width="22" height="11" rx="2"/><rect x="172" y="28" width="22" height="11" rx="2"/><rect x="204" y="28" width="22" height="11" rx="2"/>
      <rect x="108" y="50" width="22" height="11" rx="2"/><rect x="140" y="50" width="22" height="11" rx="2"/><rect x="172" y="50" width="22" height="11" rx="2"/><rect x="204" y="50" width="22" height="11" rx="2"/>
      <rect x="108" y="72" width="22" height="11" rx="2"/><rect x="140" y="72" width="22" height="11" rx="2"/><rect x="172" y="72" width="22" height="11" rx="2"/><rect x="204" y="72" width="22" height="11" rx="2"/>
      <rect x="236" y="28" width="26" height="6" fill="rgba(96,165,250,0.25)"/>
      <line x1="120" y1="100" x2="210" y2="100" stroke-width="3"/>
    </g>
    <line x1="30" y1="120" x2="70" y2="120" stroke="#60a5fa" stroke-width="3"/>
    <text x="0" y="148" font-size="11" fill="#9aa0a6" stroke="none">Second floor</text>
    <rect x="0" y="158" width="270" height="110" rx="4"/>
    <line x1="175" y1="158" x2="175" y2="268"/>
    <rect x="64" y="166" width="24" height="22" rx="3" stroke="#60a5fa" fill="rgba(96,165,250,0.15)"/>
    <g>
      <rect x="10" y="200" width="14" height="10" rx="2"/><rect x="30" y="200" width="14" height="10" rx="2"/><rect x="50" y="200" width="14" height="10" rx="2"/><rect x="70" y="200" width="14" height="10" rx="2"/><rect x="90" y="200" width="14" height="10" rx="2"/><rect x="110" y="200" width="14" height="10" rx="2"/><rect x="130" y="200" width="14" height="10" rx="2"/><rect x="150" y="200" width="14" height="10" rx="2"/>
      <rect x="10" y="218" width="14" height="10" rx="2"/><rect x="30" y="218" width="14" height="10" rx="2"/><rect x="50" y="218" width="14" height="10" rx="2"/><rect x="70" y="218" width="14" height="10" rx="2"/><rect x="90" y="218" width="14" height="10" rx="2"/><rect x="110" y="218" width="14" height="10" rx="2"/><rect x="130" y="218" width="14" height="10" rx="2"/><rect x="150" y="218" width="14" height="10" rx="2"/>
      <line x1="14" y1="246" x2="40" y2="246" stroke-width="3"/><line x1="54" y1="246" x2="80" y2="246" stroke-width="3"/><line x1="94" y1="246" x2="120" y2="246" stroke-width="3"/><line x1="134" y1="246" x2="160" y2="246" stroke-width="3"/>
    </g>
    <rect x="183" y="170" width="80" height="12" rx="2" fill="rgba(96,165,250,0.25)"/>
    <rect x="183" y="192" width="80" height="8" rx="2"/>
    <rect x="183" y="210" width="36" height="28" rx="2"/><rect x="227" y="210" width="36" height="28" rx="2"/>
    <line x1="175" y1="244" x2="175" y2="262" stroke="#60a5fa" stroke-width="3"/>
  </g>
</svg>"""

show_svg(BANNER, 640)
st.subheader("Floor plan")
st.write(
    "Concept layout for the two-floor, roughly 3,000 sq ft building. Gaps in walls "
    "are open walkways, and customers never pass through the kitchen. Furniture is not to scale."
)

INK = "#e8e8ea"
QUIET = "#9aa0a6"
EDGE = "#6b7280"
ACCENT = "#60a5fa"
TINT = "rgba(96,165,250,0.15)"
BG = "#161a23"


def text(x, y, s, size=11.5, fill=QUIET, weight=None, anchor=None):
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{w}{a}>{s}</text>'


def wall(d):
    return f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="1.25"/>'


def item(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="none" stroke="{EDGE}" stroke-width="1"/>'


def stairs(y):
    lines = "".join(
        f'<line x1="232" x2="280" y1="{y + d}" y2="{y + d}" stroke="{ACCENT}" stroke-width="1"/>'
        for d in (10, 19, 28, 37, 46)
    )
    return (
        f'<rect x="224" y="{y}" width="64" height="56" rx="4" fill="{ACCENT}" fill-opacity="0.12" '
        f'stroke="{ACCENT}" stroke-width="2"/>{lines}'
    )


parts = []
# Ground floor
parts.append(text(24, 86, "Ground floor: card shop", 13, INK, 600))
parts.append(wall("M304 200V96H24V376H304V300"))
parts.append(text(120, 120, "Card retail", 13, INK, 600, "middle"))
parts.append(text(120, 136, "600 sq ft", anchor="middle"))
parts.append(f'<rect x="36" y="150" width="12" height="200" fill="{TINT}" stroke="{EDGE}" stroke-width="1"/>')
parts.append(text(58, 162, "Sealed wall"))
parts += [item(64, y, 96, 18) for y in (180, 210, 240)]
parts.append(text(64, 274, "Singles cases"))
parts.append(item(64, 284, 96, 18))
parts.append(text(64, 318, "Graded case"))
parts.append(item(196, 290, 92, 20))
parts.append(item(266, 220, 22, 70))
parts.append(text(196, 332, "Checkout and"))
parts.append(text(196, 348, "buylist counter"))
parts.append(f'<line x1="120" x2="200" y1="376" y2="376" stroke="{ACCENT}" stroke-width="4"/>')
parts.append(stairs(108))
parts.append(text(256, 180, "Stairs and lift", fill=INK, anchor="middle"))
parts.append(f'<path d="M160 420V384" fill="none" stroke="{ACCENT}" stroke-width="1.5" marker-end="url(#arrow)"/>')
parts.append(text(172, 414, "Street entrance", fill=INK))

parts.append(wall("M304 200V96H736V376H304V300"))
parts.append(text(466, 120, "Play hall", 13, INK, 600, "middle"))
parts.append(text(466, 136, "900 sq ft, 20 tables, 80 seats", anchor="middle"))
parts += [item(x, y, 44, 22) for x in (324, 384, 444, 504, 564) for y in (156, 196, 236, 276)]
parts.append(f'<rect x="360" y="322" width="200" height="6" fill="{EDGE}"/>')
parts.append(text(460, 350, "Event screen", anchor="middle"))
parts.append(f'<rect x="640" y="160" width="84" height="12" fill="{TINT}" stroke="{EDGE}" stroke-width="1"/>')
parts.append(text(682, 190, "Game library", anchor="middle"))
parts.append(item(640, 214, 84, 26))
parts.append(text(682, 231, "Judge desk", anchor="middle"))

# Second floor
parts.append(text(24, 450, "Second floor: internet cafe and kitchen", 13, INK, 600))
parts.append(wall("M444 460H24V740H528"))
parts.append(text(120, 486, "PC and console room", 13, INK, 600, "middle"))
parts.append(text(120, 502, "900 sq ft", anchor="middle"))
parts.append(stairs(468))
parts.append(text(256, 540, "Stairs and lift", fill=INK, anchor="middle"))
parts += [item(60 + i * 44, y, 30, 22) for i in range(8) for y in (560, 596)]
parts.append(text(229, 640, "16 gaming PCs", anchor="middle"))
for x in (70, 160, 250, 340):
    parts.append(f'<rect x="{x}" y="660" width="60" height="6" fill="{EDGE}"/>')
    parts.append(item(x, 678, 60, 14))
parts.append(text(230, 716, "4 console stations", anchor="middle"))

parts.append(wall("M444 500V460H528V580H444V540"))
parts.append(text(486, 516, "Restrooms", anchor="middle"))
parts.append(text(486, 532, "and", anchor="middle"))
parts.append(text(486, 548, "storage", anchor="middle"))

parts.append(f'<rect x="528" y="460" width="208" height="280" fill="none" stroke="{EDGE}" stroke-width="1.25"/>')
parts.append(text(632, 486, "Kitchen", 13, INK, 600, "middle"))
parts.append(text(632, 502, "450 sq ft, staff only", anchor="middle"))
parts.append(f'<rect x="540" y="516" width="184" height="26" rx="3" fill="{TINT}" stroke="{EDGE}" stroke-width="1"/>')
parts.append(text(632, 533, "Hood line", fill=INK, anchor="middle"))
parts.append(text(632, 558, "Flat-top, fryers and range", anchor="middle"))
parts.append(item(564, 570, 136, 18))
parts.append(text(632, 604, "Prep tables", anchor="middle"))
parts.append(item(540, 618, 84, 56))
parts.append(text(582, 642, "Walk-in", anchor="middle"))
parts.append(text(582, 658, "cooler", anchor="middle"))
parts.append(item(640, 618, 84, 56))
parts.append(text(682, 642, "Dish", anchor="middle"))
parts.append(text(682, 658, "station", anchor="middle"))
parts.append(f'<line x1="528" x2="528" y1="690" y2="730" stroke="{ACCENT}" stroke-width="4"/>')
parts.append(text(632, 704, "Runner pickup at the pass", fill=INK, anchor="middle"))
parts.append(text(632, 720, "opens to the PC room", anchor="middle"))

svg = (
    '<svg viewBox="0 0 760 760" xmlns="http://www.w3.org/2000/svg" role="img" '
    'aria-label="Ludrin House floor plan" font-family="Source Sans Pro, sans-serif" '
    'style="width:100%;height:auto;display:block">'
    '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
    f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{ACCENT}"/></marker></defs>'
    f'<rect x="0" y="0" width="760" height="760" rx="12" fill="{BG}"/>'
    + "".join(parts)
    + "</svg>"
)

show_svg(svg, 900)

st.subheader("Space plan")
zones = pd.DataFrame(
    [
        ["Ground", "Card retail", 600, "Sealed wall behind the counter, singles cases, graded case, accessories rack, checkout and buylist counter near the entrance, stairs and lift at the back"],
        ["Ground", "Play hall", 900, "20 tables, 80 seats, board game library wall, judge desk, event screen"],
        ["Second", "PC and console room", 900, "16 gaming PCs in two rows, 4 console stations on couches"],
        ["Second", "Kitchen", 450, "Hood line with flat-top, fryers and range, prep tables, walk-in cooler, dish station, runner pickup at the pass"],
        ["Second", "Stairs, restrooms and storage", 150, "Stairs and lift, restrooms, event product storage"],
    ],
    columns=["Floor", "Zone", "Sq ft", "What goes there"],
)
st.dataframe(zones, hide_index=True)
st.caption(
    "Food is ordered by QR code or at checkout and runners carry it from the pass to wherever "
    "customers are sitting, at a PC or a game table. There is no dining area."
)
