"""Generate standalone tool pages from points-optimizer.html.

Usage: python3 build_tools.py <repo_dir>
"""
import sys, os

repo = sys.argv[1]
src = open(os.path.join(repo, 'points-optimizer.html'), encoding='utf-8').read()


def between(start, end, inclusive_end=False, frm=0):
    i = src.index(start, frm)
    j = src.index(end, i + len(start))
    return src[i:j + (len(end) if inclusive_end else 0)]


head_css = src[src.index('<style>'):src.index('</style>') + len('</style>')]

# Shared JS: data + helpers every tool needs.
data_js = between('const CURRENCY_PRESETS', '/* ---------------------------------------------------------\n   STATE + STORAGE')
helpers_js = "\n".join([
    "function cid(){ return 'c_' + Math.random().toString(36).slice(2,10); }",
    "function fmt(n){ return Math.round(n).toLocaleString('en-US'); }",
    between('function fmtCash(n){', '\n}\n', inclusive_end=True),
    between('function escapeHtml(s){', '\n}\n', inclusive_end=True),
    between('// Official program / portal URLs', '/* ---------------------------------------------------------\n   DOMESTIC AIRLINE ALLIANCES'),
])

TOOLS = [
    {
        'file': 'transfer-partners.html',
        'nav': 'Transfer Partners',
        'title': 'Transfer Partners',
        'h1': 'Where can my points transfer?',
        'lede': 'Pick a credit card points currency to see every airline and hotel partner it transfers to, and at what ratio.',
        'section': 'section-transfer',
        'js': between('function renderExplorerSelect(){', '/* ---------------------------------------------------------\n   RENDER: trip target select'),
        'init': 'renderExplorerSelect();\nrenderPartnerList();',
        'warn': True,
    },
    {
        'file': 'compare-overlap.html',
        'nav': 'Compare Overlap',
        'title': 'Compare Transfer Overlap',
        'h1': 'Which partners do my cards share?',
        'lede': 'Select two or more points currencies to see which airline and hotel programs more than one of them can reach, so you know where you can pool points.',
        'section': 'section-compare',
        'js': 'let cards = DEFAULT_CARDS;\n' + between('let compareSelection = null;', '/* ---------------------------------------------------------\n   UTIL + INIT'),
        'init': 'renderCompareChecks();\nrenderMatrix();',
        'warn': True,
    },
    {
        'file': 'airline-alliances.html',
        'nav': 'Airline Alliances',
        'title': 'Airline Alliances',
        'h1': 'Which partner airlines can I book?',
        'lede': 'Pick a US airline and a points currency to see its global alliance and which partner airlines that currency can actually reach.',
        'section': 'section-alliances',
        'js': between('const ALLIANCE_LINKS = {', '/* ---------------------------------------------------------\n   STEP 2: PATHWAY FINDER'),
        'init': 'renderAllianceSelect();\nrenderAllianceResult();',
        'warn': True,
    },
    {
        'file': 'points-or-cash.html',
        'nav': 'Points or Cash?',
        'title': 'Points or Cash?',
        'h1': 'Transfer points or pay cash?',
        'lede': 'Enter the points price, the taxes and fees, and the cash price to see your cents-per-point value and whether the redemption is worth it.',
        'section': 'section-cpp',
        'js': between('function computeCpp(){', '\ncomputeCpp();\n', inclusive_end=True),
        'init': '',
        'warn': False,
    },
]

WARNING = ('<div class="hero-warning"><strong>This is a planning tool, not a booking guarantee.</strong> '
           'Confirm the current transfer rate and partner list on the issuer\'s and loyalty program\'s own site '
           'before you move any points. Both can change without notice, and most transfers are final.</div>')

for t in TOOLS:
    sec_start = src.index(f'<section class="panel" id="{t["section"]}">')
    sec_end = src.index('</section>', sec_start) + len('</section>')
    section_html = src[sec_start:sec_end]

    nav_links = ['<a href="index.html">&larr; Dad Hat Travel</a>',
                 '<a href="points-optimizer.html">Full Optimizer</a>']
    for o in TOOLS:
        if o is not t:
            nav_links.append(f'<a href="{o["file"]}">{o["nav"]}</a>')

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t["title"]} | Dad Hat Travel and Points</title>
<meta name="description" content="{t["lede"]}">
{head_css}
<style>.topnav{{position:static;}}</style>
</head>
<body>
<div class="wrap">

  <nav class="topnav">
    {chr(10).join("    " + l if i else l for i, l in enumerate(nav_links))}
  </nav>

  <div class="hero">
    <p class="hero-eyebrow">DAD HAT TRAVEL &amp; POINTS TOOLS</p>
    <h1>{t["h1"]}</h1>
    <p>{t["lede"]}</p>
    {WARNING if t["warn"] else ""}
  </div>

  {section_html}

</div>

<script>
/* Generated from points-optimizer.html by build_tools.py. Edit the optimizer, then regenerate. */
{helpers_js}
{data_js}
{t["js"]}
{t["init"]}
</script>
</body>
</html>
'''
    with open(os.path.join(repo, t['file']), 'w', encoding='utf-8') as f:
        f.write(page)
    print('wrote', t['file'], len(page))
