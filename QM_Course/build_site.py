"""
Build the offline HTML version of the course from the markdown sources.

Run:  python build_site.py
Then open site/index.html in any browser. No internet needed.

Re-run this after editing any .md file.
"""
import os
import re
import html as htmllib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

try:
    import markdown as md_lib
    HAVE_MD = True
except ImportError:
    HAVE_MD = False

CHAPTERS = [
    ('01_setup_first_program', 'Setup and your first program', 1),
    ('02_variables_and_types', 'Variables, numbers and types', 1),
    ('03_decisions_and_loops', 'Decisions and loops', 1),
    ('04_lists_and_collections', 'Lists and collections', 1),
    ('05_functions', 'Functions', 1),
    ('06_numpy', 'numpy: arrays and vectorised thinking', 2),
    ('07_matplotlib', 'matplotlib: drawing graphs properly', 2),
    ('08_randomness', 'Randomness, simulation and statistics', 2),
    ('09_task1_random_walk', 'Task 1 — Random walks', 3),
    ('10_task2_brownian', 'Task 2 — Brownian motion', 3),
    ('11_task3_blackbody', 'Task 3 — Planck and Einstein', 3),
    ('12_task4_photoelectric', 'Task 4 — Photoelectric effect', 3),
    ('13_task5_hydrogen', 'Task 5 — Hydrogen spectrum', 3),
    ('14_task6_diffraction', 'Task 6 — Electron diffraction', 3),
    ('15_task7_particle_in_box', 'Task 7 — Particle in a box', 3),
    ('16_task8_cryptography', 'Task 8 — Quantum cryptography', 3),
    ('17_task9_compton', 'Task 9 — Compton scattering', 3),
    ('18_task10_orbitals', 'Task 10 — Hydrogenic orbitals', 3),
    ('19_widgets', 'Widgets and interactivity', 4),
    ('20_tkinter_launcher', 'The tkinter launcher', 4),
    ('21_colour_science', 'Colour science: CIE 1931', 4),
    ('22_capstone', 'Capstone: rebuild everything', 5),
]

REFERENCE = [
    ('python_cheatsheet', 'Python cheat sheet'),
    ('numpy_cheatsheet', 'numpy cheat sheet'),
    ('matplotlib_cheatsheet', 'matplotlib cheat sheet'),
    ('physics_formulas', 'Physics formula sheet'),
    ('errors_decoded', 'Error messages decoded'),
    ('glossary', 'Glossary'),
]

PART_NAMES = {
    1: 'Part 1 — Python from zero',
    2: 'Part 2 — Scientific Python',
    3: 'Part 3 — The ten tasks',
    4: 'Part 4 — Making it interactive',
    5: 'Part 5 — Capstone',
}

CSS = """
:root{
  --bg:#0d1117; --panel:#161b22; --border:#30363d; --fg:#e6edf3;
  --muted:#8b949e; --accent:#58a6ff; --code:#1f2630; --green:#3fb950;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.7 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
#layout{display:flex;min-height:100vh}
#sidebar{width:310px;flex:0 0 310px;background:var(--panel);
  border-right:1px solid var(--border);padding:22px 18px;overflow-y:auto;
  height:100vh;position:sticky;top:0}
#sidebar h1{font-size:17px;margin:0 0 4px;color:var(--accent)}
#sidebar .sub{font-size:12px;color:var(--muted);margin-bottom:18px}
#sidebar .part{font-size:11px;text-transform:uppercase;letter-spacing:.09em;
  color:var(--muted);margin:18px 0 7px}
#sidebar a{display:block;color:var(--fg);text-decoration:none;padding:5px 9px;
  border-radius:6px;font-size:13.5px;margin-bottom:1px}
#sidebar a:hover{background:var(--code)}
#sidebar a.active{background:var(--accent);color:#0d1117;font-weight:600}
main{flex:1;padding:44px 56px;max-width:900px}
h1{font-size:31px;margin:0 0 22px;line-height:1.25}
h2{font-size:22px;margin:36px 0 12px;padding-bottom:7px;
  border-bottom:1px solid var(--border)}
h3{font-size:17px;margin:26px 0 9px;color:var(--accent)}
p{margin:12px 0}
a{color:var(--accent)}
code{background:var(--code);padding:2px 6px;border-radius:4px;
  font:14px/1.5 "Cascadia Code",Consolas,monospace;color:#ffa657}
pre{background:var(--code);border:1px solid var(--border);border-radius:9px;
  padding:15px 17px;overflow-x:auto;margin:16px 0}
pre code{background:none;padding:0;color:#e6edf3;font-size:13.5px}
table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14.5px}
th,td{border:1px solid var(--border);padding:8px 11px;text-align:left}
th{background:var(--panel);color:var(--accent)}
tr:nth-child(even) td{background:rgba(255,255,255,.02)}
blockquote{border-left:3px solid var(--accent);margin:16px 0;padding:2px 18px;
  color:var(--muted)}
hr{border:none;border-top:1px solid var(--border);margin:30px 0}
ul,ol{padding-left:26px}
li{margin:5px 0}
strong{color:#fff}
.nav{display:flex;justify-content:space-between;margin-top:52px;
  padding-top:22px;border-top:1px solid var(--border);gap:14px}
.nav a{padding:9px 15px;background:var(--panel);border:1px solid var(--border);
  border-radius:8px;text-decoration:none;font-size:14px}
.nav a:hover{border-color:var(--accent)}
.hero{background:linear-gradient(135deg,#161b22,#1f2937);
  border:1px solid var(--border);border-radius:13px;padding:30px;margin:22px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
  gap:13px;margin:20px 0}
.card{background:var(--panel);border:1px solid var(--border);border-radius:10px;
  padding:15px 17px;text-decoration:none;color:var(--fg);display:block}
.card:hover{border-color:var(--accent)}
.card b{display:block;margin-bottom:4px}
.card span{font-size:12.5px;color:var(--muted)}
@media(max-width:900px){#layout{flex-direction:column}
  #sidebar{width:100%;height:auto;position:static}main{padding:26px 20px}}
"""


def simple_markdown(text):
    """Very small markdown converter, used only if the markdown lib is absent."""
    out, in_code, in_table, in_list = [], False, False, False
    for raw in text.split('\n'):
        if raw.startswith('```'):
            if in_code:
                out.append('</code></pre>')
            else:
                out.append('<pre><code>')
            in_code = not in_code
            continue
        if in_code:
            out.append(htmllib.escape(raw))
            continue
        line = htmllib.escape(raw)
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', line)
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '):
                continue
            if not in_table:
                out.append('<table>')
                in_table = True
                out.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            else:
                out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            continue
        if in_table:
            out.append('</table>')
            in_table = False
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{m.group(2)}</h{lvl}>')
            continue
        if re.match(r'^\s*[-*]\s+', line):
            if not in_list:
                out.append('<ul>')
                in_list = True
            out.append('<li>' + re.sub(r'^\s*[-*]\s+', '', line) + '</li>')
            continue
        if re.match(r'^\d+\.\s+', line):
            if not in_list:
                out.append('<ol>')
                in_list = True
            out.append('<li>' + re.sub(r'^\d+\.\s+', '', line) + '</li>')
            continue
        if in_list and line.strip() == '':
            out.append('</ul>')
            in_list = False
        if line.strip() == '---':
            out.append('<hr>')
        elif line.strip() == '':
            out.append('')
        else:
            out.append(f'<p>{line}</p>')
    if in_table:
        out.append('</table>')
    if in_list:
        out.append('</ul>')
    return '\n'.join(out)


def to_html(text):
    if HAVE_MD:
        return md_lib.markdown(text, extensions=['tables', 'fenced_code'])
    return simple_markdown(text)


def sidebar(active=''):
    parts = [f'<h1>Computational Quantum Physics</h1>'
             f'<div class="sub">a course built from your own project</div>',
             f'<a href="index.html" class="{"active" if active=="index" else ""}">'
             f'&#8962; Home</a>']
    last = None
    for slug, title, part in CHAPTERS:
        if part != last:
            parts.append(f'<div class="part">{PART_NAMES[part]}</div>')
            last = part
        num = slug.split('_')[0]
        cls = 'active' if active == slug else ''
        parts.append(f'<a href="{slug}.html" class="{cls}">{num}. {title}</a>')
    parts.append('<div class="part">Reference</div>')
    for slug, title in REFERENCE:
        cls = 'active' if active == slug else ''
        parts.append(f'<a href="{slug}.html" class="{cls}">{title}</a>')
    return '\n'.join(parts)


def page(title, body, active='', prev_link='', next_link=''):
    nav = '<div class="nav">'
    nav += (f'<a href="{prev_link[0]}.html">&larr; {prev_link[1]}</a>'
            if prev_link else '<span></span>')
    nav += (f'<a href="{next_link[0]}.html">{next_link[1]} &rarr;</a>'
            if next_link else '<span></span>')
    nav += '</div>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{htmllib.escape(title)}</title><style>{CSS}</style></head>
<body><div id="layout">
<nav id="sidebar">{sidebar(active)}</nav>
<main>{body}{nav}</main>
</div></body></html>"""


def build():
    os.makedirs(OUT, exist_ok=True)
    made = 0

    # chapters
    for i, (slug, title, part) in enumerate(CHAPTERS):
        src = os.path.join(HERE, 'chapters', slug + '.md')
        if not os.path.exists(src):
            print('  missing:', src)
            continue
        with open(src, encoding='utf-8') as f:
            body = to_html(f.read())
        prev_link = (CHAPTERS[i-1][0], CHAPTERS[i-1][1]) if i > 0 else ''
        next_link = (CHAPTERS[i+1][0], CHAPTERS[i+1][1]) if i < len(CHAPTERS)-1 else ''
        with open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8') as f:
            f.write(page(title, body, slug, prev_link, next_link))
        made += 1

    # reference
    for slug, title in REFERENCE:
        src = os.path.join(HERE, 'reference', slug + '.md')
        if not os.path.exists(src):
            continue
        with open(src, encoding='utf-8') as f:
            body = to_html(f.read())
        with open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8') as f:
            f.write(page(title, body, slug))
        made += 1

    # home page
    cards = []
    last = None
    home = ['<h1>Computational Quantum Physics</h1>',
            '<div class="hero"><p style="margin:0;font-size:17px">Everything in '
            'this course teaches one thing: how to build the BPhO 2026 Quantum '
            'Mechanics entry from an empty file, by yourself. Nothing is '
            'assumed. If you have never written a line of Python, start at '
            'Chapter 1 and do not skip.</p></div>',
            '<h2>How to use it</h2>',
            '<p><strong>Read &rarr; type &rarr; break &rarr; fix.</strong> '
            'Reading code teaches you almost nothing. Typing it teaches you a '
            'little. Breaking it on purpose and fixing it teaches you almost '
            'everything. Every chapter has "Break it" exercises &mdash; do '
            'them.</p>',
            '<p><strong>Never copy-paste in this course.</strong> Type every '
            'line, even when it is slow. Your fingers learn syntax your eyes '
            'skip over.</p>',
            '<p>Exercises are at the end of each chapter; worked solutions live '
            'in the <code>solutions/</code> folder as runnable Python. Try '
            'before you look.</p>']
    for slug, title, part in CHAPTERS:
        if part != last:
            if cards:
                home.append('<div class="grid">' + ''.join(cards) + '</div>')
                cards = []
            home.append(f'<h2>{PART_NAMES[part]}</h2>')
            last = part
        num = slug.split('_')[0]
        cards.append(f'<a class="card" href="{slug}.html"><b>{num}. {title}</b>'
                     f'<span>chapter</span></a>')
    home.append('<div class="grid">' + ''.join(cards) + '</div>')
    home.append('<h2>Reference</h2><div class="grid">')
    for slug, title in REFERENCE:
        home.append(f'<a class="card" href="{slug}.html"><b>{title}</b>'
                    f'<span>quick lookup</span></a>')
    home.append('</div>')
    home.append('<hr><p style="color:#8b949e">Some chapters will feel hard. '
                'That feeling is not a signal that you are unsuited to this '
                '&mdash; it is the feeling of learning. The people who look '
                'effortless at this had the same weeks; they just had them '
                'earlier. Keep going.</p>')

    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page('Computational Quantum Physics', '\n'.join(home), 'index'))
    made += 1

    print(f'Built {made} pages in {OUT}')
    print('Open site/index.html in any browser.')
    if not HAVE_MD:
        print('(using the built-in converter; "pip install markdown" gives '
              'slightly nicer output)')


if __name__ == '__main__':
    build()
