import pandas as pd
import streamlit as st

st.title("Ludrin House Floor Plan")
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

st.html(f'<div style="max-width:900px;margin:0 auto">{svg}</div>')

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
