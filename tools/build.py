#!/usr/bin/env python3
"""Build residentroom-site: inject Bicyclette headline outlines into the HTML templates.

Headlines are pre-converted to SVG paths (tools/outlines.json) so the licensed font file is
never published. Run from the repo root: python3 tools/build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
O = json.loads((ROOT / 'tools/outlines.json').read_text())
H = O['top'] + 40  # viewBox height: accents above the cap line, a little room below


def heading(key, label, tag='h2', cls=''):
    words = ''.join(
        f'<svg class="hw" viewBox="0 0 {w["w"]} {H}" style="--w:{w["w"]}" aria-hidden="true" focusable="false">'
        f'<path d="{w["d"]}"/></svg>'
        for w in O['headings'][key])
    return f'<{tag} class="display {cls}"><span class="sr">{label}</span>{words}</{tag}>'


MAIL_BODY = ('Dagsetning / Date:%0D%0AFjöldi gesta / Guests:%0D%0ATilefni / Occasion:'
             '%0D%0ANafn og fyrirtæki / Name and company:%0D%0A')
HIRE_MAIL = f'mailto:info@residentroom.is?subject=Einkasamkv%C3%A6mi%20%2F%20Private%20hire&body={MAIL_BODY}'
MAPS = ('https://www.google.com/maps/dir/?api=1&destination=Hverfisgata%2026%2C%20101%20Reykjav%C3%ADk'
        '&travelmode=walking')

for tpl, out in (('tools/index.tpl.html', 'index.html'), ('tools/privacy.tpl.html', 'privacy/index.html')):
    html = (ROOT / tpl).read_text()
    html = (html
            .replace('{{H1}}', heading('h1', 'Dyrnar eru opnar', 'h1'))
            .replace('{{H1_EN}}', heading('h1en', 'The door is open', 'p', 'display--en'))
            .replace('{{DAYS}}', heading('days', 'Miðvikudaga til sunnudaga', 'p', 'display--xl'))
            .replace('{{TIME}}', heading('time', 'frá klukkan 16:00', 'p', 'display--xl'))
            .replace('{{HIRE}}', heading('hire', 'Herbergið er ykkar'))
            .replace('{{HIRE_EN}}', heading('hireen', 'The room is yours', 'p', 'display--en'))
            .replace('{{GIFT}}', heading('gift', 'Gjafabréf'))
            .replace('{{PRIVACY}}', heading('privacy', 'Persónuvernd', 'h1'))
            .replace('{{HIRE_MAIL}}', HIRE_MAIL)
            .replace('{{MAPS}}', MAPS))
    (ROOT / out).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / out).write_text(html)
    print('built', out, f'{len(html) // 1024} KB')
