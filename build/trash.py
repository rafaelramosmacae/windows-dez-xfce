# Windows Dez — (c) 2026 Rafael Carvalho Ramos <rafaelramosmacae@gmail.com> — GPL-3.0-or-later
"""3D-style trash can icons (empty and full) for the windows-dez icon theme.
A square-section bin seen in perspective: two shaded faces, a dark opening,
glossy ribs, a darker base band and a soft floor shadow."""

DEFS = '''<defs>
<linearGradient id="tleft" x1="0" y1="0" x2="1" y2="0.15">
 <stop offset="0" stop-color="#F4F8FC"/><stop offset="1" stop-color="#D3E2EE"/></linearGradient>
<linearGradient id="tright" x1="0" y1="0" x2="1" y2="0.1">
 <stop offset="0" stop-color="#BCD0E1"/><stop offset="1" stop-color="#8FAAC2"/></linearGradient>
<linearGradient id="tinner" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#44596D"/><stop offset="1" stop-color="#7F99B0"/></linearGradient>
<radialGradient id="tshadow" cx="0.5" cy="0.5" r="0.5">
 <stop offset="0" stop-color="#000000" stop-opacity="0.30"/><stop offset="1" stop-color="#000000" stop-opacity="0"/></radialGradient>
<linearGradient id="paper1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D5DBE1"/></linearGradient>
<linearGradient id="paper2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF3C4"/><stop offset="1" stop-color="#E5C25E"/></linearGradient>
</defs>'''

# Corners (48 px grid). Top rim: L=left, F=front, R=right, B=back. Bottom: bl, bf, br.
L, F, R, B = (7.5, 12.0), (21.5, 16.5), (40.5, 11.5), (26.5, 8.0)
bl, bf, br = (11.5, 39.5), (22.0, 44.0), (36.8, 39.2)


def P(*pts):
    return " ".join(f"{x:.2f} {y:.2f}" for x, y in pts)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def ribs():
    out = ""
    for face, (t0, t1, b0, b1), light in (("l", (L, F, bl, bf), 0.65), ("r", (F, R, bf, br), 0.45)):
        for t in (0.22, 0.44, 0.66, 0.84):
            top = lerp(t0, t1, t); bot = lerp(b0, b1, t)
            top = (top[0], top[1] + 2.2); bot = (bot[0], bot[1] - 3.2)
            out += f'<path d="M{P(top)}L{P(bot)}" stroke="#FFFFFF" stroke-opacity="{light}" stroke-width="0.9"/>'
            out += (f'<path d="M{P((top[0]+0.8, top[1]))}L{P((bot[0]+0.6, bot[1]))}" '
                    f'stroke="#5F7F9B" stroke-opacity="0.30" stroke-width="0.7"/>')
    return out


def bin_svg(full=False):
    papers = ""
    if full:
        papers = (
            '<path d="M11 12.5l3.5-6.2 5.2 2.4 3.2-5 5.6 3.1 1.6 5.9-8.4 3.4z" fill="url(#paper1)" stroke="#A9B4BF" stroke-width="0.6" stroke-linejoin="round"/>'
            '<path d="M14.5 6.3l2.4 5.4M19.7 8.7l1.3 5.2M22.9 3.7l1.5 6.6" stroke="#C3CBD3" stroke-width="0.6"/>'
            '<path d="M25 10.8l3.4-6.4 6.1 0.9 3.6 5.3-4.2 3.2-7.4-0.4z" fill="url(#paper2)" stroke="#C49B2F" stroke-width="0.6" stroke-linejoin="round"/>'
            '<path d="M28.4 4.4l1.8 6.6M34.5 5.3l-1.3 5.6" stroke="#D6B04B" stroke-width="0.6"/>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">' + DEFS +
        '<ellipse cx="24" cy="42.6" rx="15" ry="3" fill="url(#tshadow)"/>'
        # opening (inner walls)
        f'<path d="M{P(L)}L{P(F)}L{P(R)}L{P(B)}Z" fill="url(#tinner)"/>'
        + papers +
        # faces
        f'<path d="M{P(L)}L{P(F)}L{P(bf)}L{P(bl)}Z" fill="url(#tleft)" fill-opacity="0.96" stroke="#6E8CA6" stroke-width="0.7" stroke-linejoin="round"/>'
        f'<path d="M{P(F)}L{P(R)}L{P(br)}L{P(bf)}Z" fill="url(#tright)" fill-opacity="0.96" stroke="#6E8CA6" stroke-width="0.7" stroke-linejoin="round"/>'
        + ribs() +
        # base band
        f'<path d="M{P(lerp(L, bl, 0.9))}L{P(lerp(F, bf, 0.9))}L{P(lerp(R, br, 0.9))}L{P(br)}L{P(bf)}L{P(bl)}Z" '
        'fill="#7893AC" fill-opacity="0.75"/>'
        # front edge highlight
        f'<path d="M{P(F)}L{P(bf)}" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="1"/>'
        # rim
        f'<path d="M{P(L)}L{P(F)}L{P(R)}L{P(B)}Z" fill="none" stroke="#F7FBFE" stroke-width="1.4" stroke-linejoin="round"/>'
        f'<path d="M{P(L)}L{P(F)}L{P(R)}" fill="none" stroke="#6E8CA6" stroke-width="0.6" stroke-linejoin="round"/>'
        '</svg>\n'
    )


if __name__ == "__main__":
    import sys
    open(sys.argv[1] + "/user-trash.svg", "w").write(bin_svg(False))
    open(sys.argv[1] + "/user-trash-full.svg", "w").write(bin_svg(True))
