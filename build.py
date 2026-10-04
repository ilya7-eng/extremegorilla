"""Build index.html from template.html + videos.json (newest first). Add a video: append {id,title,thumb,date} to videos.json, rerun, push gh-pages."""
import json, html, datetime, pathlib
P = pathlib.Path(__file__).parent
vids = sorted(json.loads((P/'videos.json').read_text()), key=lambda v: v['date'], reverse=True)
def card(v):
    t = v['title'].replace(' | Extreme Gorilla', '')
    d = datetime.datetime.fromisoformat(v['date'].replace('Z', '+00:00')).strftime('%b %-d, %Y')
    thumb = f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg"
    return (f'  <article class="card"><button class="thumb" data-id="{v["id"]}" aria-label="Play: {html.escape(t)}">'
            f'<img src="{thumb}" alt="" loading="lazy"><span class="play"><span></span></span></button>'
            f'<div class="meta"><h3>{html.escape(t)}</h3><div class="date">{d}</div></div></article>')
out = (P/'template.html').read_text().replace('{{VIDEO_CARDS}}', '\n'.join(card(v) for v in vids)) \
    .replace('{{VIDEO_COUNT}}', str(len(vids))).replace('{{YEAR}}', str(datetime.date.today().year))
(P/'index.html').write_text(out); print('built', len(vids), 'videos')
