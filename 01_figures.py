"""Figures 1-3 and Supplementary Fig. 1. Writes PNG (300 dpi) and PDF to outputs/figures/.
Needs data/extraction_and_ratings.json and outputs/study_coding.json."""
import json, re, statistics as st, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.colors import ListedColormap, BoundaryNorm
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.load(open(HERE / 'data' / 'extraction_and_ratings.json')); R = d['rows']; A = d['ratings']
RC = json.load(open(HERE / 'outputs' / 'study_coding.json'))
(HERE / 'outputs' / 'figures').mkdir(parents=True, exist_ok=True)
OUT = str(HERE / 'outputs' / 'figures') + '/'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#8a8984', 'xtick.color': '#52514e', 'ytick.color': '#0b0b0b'})
TXT2 = '#52514e'
YES, PAR, NO = '#1f5fa8', '#8fb6e6', '#dddcd8'          # reported / partially reported / not reported
VAL = {'Yes': 1, 'Partial': .5, 'No': 0}                 # 'NA' items are left out of every denominator
funcs = ['Diagnosis and referral', 'Endpoint measurement', 'Biomarker quantification', 'Response prediction']
year = {k: int(re.search(r'(20\d\d)', R[k]['study']).group(1)) for k in R}


def panel(fig, ax, letter, title, dy=0.035):
    """Bold panel letter and plain title above the panel, at the figure's left edge."""
    y = ax.get_position().y1 + dy
    fig.text(0.02, y, letter, fontsize=11, fontweight='bold', va='bottom')
    fig.text(0.05, y + 0.002, title, fontsize=8.5, va='bottom')


def save(fig, name):
    for e in ['png', 'pdf']:
        fig.savefig(OUT + f'{name}.{e}', dpi=300)
    plt.close(fig)


# ---------------- Fig 1: PRISMA-ScR flow diagram (numbers from the Covidence screening record)
def box(ax, x, y, w, h, text, fs=7.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='square,pad=0', fc='white', ec='#3b3b3b', lw=0.8))
    ax.text(x + 0.012, y + h - 0.012, text, ha='left', va='top', fontsize=fs, linespacing=1.35)


def arrow(ax, x0, y0, x1, y1):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='-|>', lw=0.8, color='#3b3b3b'))


fig = plt.figure(figsize=(7.2, 6.4)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
for y0, h, lab in [(0.80, 0.18, 'Identification'), (0.15, 0.62, 'Screening'), (0.03, 0.10, 'Included')]:
    ax.add_patch(FancyBboxPatch((0.015, y0), 0.045, h, boxstyle='round,pad=0,rounding_size=0.01', fc='#dbe7f5', ec='none'))
    ax.text(0.0375, y0 + h / 2, lab, rotation=90, ha='center', va='center', fontsize=8, fontweight='bold')
L, W, RX, RW = 0.08, 0.40, 0.545, 0.44
box(ax, L, 0.81, W, 0.16, 'Records identified from databases\n(n = 2,380)\n    Embase (n = 1,719)\n    MEDLINE (n = 568)\n    CENTRAL (n = 93)')
box(ax, RX, 0.81, RW, 0.16, 'Records removed before screening:\n    Duplicate records (n = 384)\n        Identified by Covidence (n = 379)\n        Identified manually (n = 5)')
box(ax, L, 0.66, W, 0.07, 'Records screened\n(n = 1,996)')
box(ax, RX, 0.66, RW, 0.07, 'Records excluded at title and abstract\n(n = 1,878)')
box(ax, L, 0.53, W, 0.07, 'Reports sought for retrieval\n(n = 118)')
box(ax, RX, 0.53, RW, 0.07, 'Reports not retrieved\n(n = 0)')
box(ax, L, 0.40, W, 0.07, 'Reports assessed for eligibility\n(n = 118)')
box(ax, RX, 0.15, RW, 0.32, 'Reports excluded (n = 82):\n'
    '    Conference abstract only (n = 27)\n'
    '    Protocol, registry entry or no results\n        reported (n = 27)\n'
    '    Trial data used only as an AI dataset,\n        no trial-related question (n = 20)\n'
    '    Not a clinical trial or trial data\n        (observational, registry or\n        real-world data) (n = 6)\n'
    '    AI not used in study methods (n = 1)\n'
    '    Not retinal disease, or retinal results\n        not separable (n = 1)')
box(ax, L, 0.05, W, 0.07, 'Studies included in review\n(n = 36)')
mx = L + W / 2
for y0, y1 in [(0.81, 0.73), (0.66, 0.60), (0.53, 0.47), (0.40, 0.12)]:
    arrow(ax, mx, y0, mx, y1)
for y in [0.89, 0.695, 0.565, 0.435]:
    arrow(ax, L + W, y, RX, y)
save(fig, 'Fig1_PRISMA_ScR')

# ---------------- Fig 2: when the studies were published, which trials they came from, and what the AI did
TIM = [('Prospective, AI changed trial conduct', '#c4421a'), ('Prospective, AI did not change trial conduct', '#f2a07b'),
       ('Retrospective (secondary or post hoc analysis)', '#2a78d6')]


def tim(k):
    if RC[k]['timing'].startswith('Prosp'):
        return 0 if RC[k]['influenced_trial_conduct'] == 'Yes' else 1
    return 2


fig = plt.figure(figsize=(7.2, 7.4))
gs = fig.add_gridspec(3, 1, height_ratios=[0.95, 0.75, 1.0], hspace=1.0, left=0.30, right=0.95, top=0.93, bottom=0.06)
# a: publication year, with the share published from 2022 onwards
ax = fig.add_subplot(gs[0]); yrs = list(range(2018, 2026)); v = [sum(year[k] == y for k in R) for y in yrs]
ax.bar(yrs, v, color='#6b7785', width=0.65)
for y, n in zip(yrs, v):
    ax.text(y, n + 0.15, str(n), ha='center', fontsize=7.5)
n22 = sum(year[k] >= 2022 for k in R)
ax.plot([2021.6, 2021.6, 2025.4, 2025.4], [8.2, 8.5, 8.5, 8.2], color=TXT2, lw=0.8)
ax.text(2023.5, 8.75, f'2022–2025: {n22} of {len(R)} studies ({round(100 * n22 / len(R))}%)', ha='center', fontsize=7.5, color=TXT2)
ax.set_xticks(yrs); ax.set_ylabel('Number of studies'); ax.set_ylim(0, 10); ax.set_yticks([0, 2, 4, 6, 8])
# b: trial programs contributing more than one study (companion trials analyzed together count as one program)
prog = {'HARBOR': 5, 'FILLY': 5, 'OAKS/DERBY': 2, 'HAWK/HARRIER': 2}
bx = fig.add_subplot(gs[1]); names = list(prog)
for i, p in enumerate(names):
    bx.barh(i, prog[p], color='#6b7785', height=0.6); bx.text(prog[p] + 0.1, i, str(prog[p]), va='center', fontsize=8)
bx.set_yticks(range(len(names))); bx.set_yticklabels(names); bx.set_ylim(len(names) - 0.5, -0.5); bx.set_xlim(0, 6)
bx.set_xlabel('Number of included studies'); bx.tick_params(axis='y', length=0)
# c: AI function, stacked by timing and integration, with each segment labelled
cx = fig.add_subplot(gs[2])
for i, f in enumerate(funcs):
    left = 0
    for j, (lab, c) in enumerate(TIM):
        n = sum(1 for k in R if RC[k]['function'] == f and tim(k) == j)
        if n:
            cx.barh(i, n, left=left, color=c, height=0.62, edgecolor='white', lw=1)
            cx.text(left + n / 2, i, str(n), ha='center', va='center', fontsize=7.5, color='white' if j != 1 else '#0b0b0b')
        left += n
    cx.text(left + 0.25, i, f'Total {left}', va='center', fontsize=7.5)
cx.set_yticks(range(4)); cx.set_yticklabels(funcs); cx.set_ylim(3.6, -0.6); cx.set_xlim(0, 14)
cx.set_xlabel('Number of studies'); cx.tick_params(axis='y', length=0)
cx.legend(handles=[Patch(color=c, label=l) for l, c in TIM], loc='lower left', bbox_to_anchor=(-0.40, 1.02), ncol=2,
          frameon=False, fontsize=7, columnspacing=1.2, handlelength=1.2)
fig.canvas.draw()
panel(fig, ax, 'a', 'Included studies by publication year (n = 36)')
panel(fig, bx, 'b', 'Trial programs contributing more than one study')
panel(fig, cx, 'c', 'AI function, by timing and whether AI changed trial conduct (n = 36)', dy=0.075)
save(fig, 'Fig2_ai_use')

# ---------------- Fig 3: reporting completeness by study type
Mst = [k for k in RC if RC[k]['appraisal_group'] == 'AI measurement study']
dims = [('Reproducibility', [('AI-5-i', 'Algorithm name and version'), ('AI-4b', 'Place of AI in the analysis pipeline'), ('AI-25', 'Access to code or model')]),
        ('Measurement validity', [('MV', 'Accuracy or agreement on trial images*'), ('AI-19', 'Error analysis'), ('AI-5-iv', 'Human review or correction of outputs')]),
        ('Transportability', [('AI-4a-ii', 'Image eligibility criteria'), ('AI-5-iii', 'Handling of poor-quality images'), ('AI-5-ii', 'Image acquisition and device')]),
        ('Output definition', [('AI-5-v', 'Definition of AI outputs')])]
fig = plt.figure(figsize=(7.2, 10.4))
gs = fig.add_gridspec(3, 1, height_ratios=[1.75, 1.0, 0.45], hspace=0.95, left=0.37, right=0.84, top=0.935, bottom=0.08)
ax = fig.add_subplot(gs[0]); y = 0; yt = []; yl = []; heads = []; n = len(Mst)
for dname, its in dims:
    heads.append((dname, y)); y += 1.0
    for it, lab in its:
        if it == 'MV':
            yv = sum(RC[k]['measurement_validation'].startswith(('Accuracy', 'Agreement')) for k in Mst)
            p = sum(RC[k]['measurement_validation'].startswith('Outputs corrected') for k in Mst)
        else:
            rs = [A[k]['ai_items'][it]['r'] for k in Mst]; yv, p = rs.count('Yes'), rs.count('Partial')
        nn = n - yv - p
        ax.barh(y, yv / n, color=YES, height=0.62, edgecolor='white'); ax.barh(y, p / n, left=yv / n, color=PAR, height=0.62, edgecolor='white')
        ax.barh(y, nn / n, left=(yv + p) / n, color=NO, height=0.62, edgecolor='white')
        ax.text(1.06, y, f'{yv}', va='center', ha='center', fontsize=7.5, color=TXT2)
        ax.text(1.19, y, f'{p}', va='center', ha='center', fontsize=7.5, color=TXT2)
        yt.append(y); yl.append(lab); y += 1
    y += 0.5
for dname, y0 in heads:
    ax.text(-0.02, y0 + 0.1, dname, ha='right', va='center', fontsize=8, fontweight='bold', transform=ax.get_yaxis_transform())
ax.text(1.06, -0.9, 'Reported', fontsize=6.8, color=TXT2, ha='center', va='center')
ax.text(1.19, -0.9, 'Partial', fontsize=6.8, color=TXT2, ha='center', va='center')
ax.set_yticks(yt); ax.set_yticklabels(yl); ax.tick_params(axis='y', length=0); ax.set_ylim(y - 0.4, -1.4); ax.set_xlim(0, 1)
ax.set_xticks([0, .5, 1]); ax.set_xticklabels(['0%', '50%', '100%']); ax.set_xlabel('Share of the 22 AI measurement studies')
LEG = [Patch(color=YES, label='Reported'), Patch(color=PAR, label='Partially reported'), Patch(color=NO, label='Not reported')]
ax.legend(handles=LEG, loc='upper left', bbox_to_anchor=(-0.6, -0.105), ncol=3, frameon=False, fontsize=7.2)
ax.text(-0.6, -0.185, '*Accuracy or agreement: partially reported means analysts corrected all AI outputs\n  but the AI\'s own accuracy was not reported. Other rows: see Supplementary Table 7.',
        transform=ax.transAxes, fontsize=6.6, color=TXT2, va='top')
# b: TRIPOD+AI, share of applicable item ratings by checklist section, with percentage labels
TR = sorted([k for k in RC if RC[k]['appraisal_group'].startswith('Prediction')], key=int)
secs = [('Title and abstract', ['1', '2']), ('Introduction', ['3a', '3b', '3c', '4']),
        ('Methods', ['5a', '5b', '6a', '6b', '6c', '7', '8a', '8b', '8c', '9a', '9b', '9c', '10', '11', '12a', '12b', '12c', '12d', '12e', '12f', '12g', '13', '14', '15', '16', '17']),
        ('Open science', ['18a', '18b', '18c', '18d', '18e', '18f']), ('Patient and public involvement', ['19']),
        ('Results', ['20a', '20b', '20c', '21', '22', '23a', '23b', '24']), ('Discussion', ['25', '26', '27a', '27b', '27c'])]
bx = fig.add_subplot(gs[1])
for i, (s, its) in enumerate(secs):
    rs = [A[k]['full_items'][it]['r'] for k in TR for it in its]; rs = [r for r in rs if r in VAL]; m = len(rs)
    a, b, c = rs.count('Yes') / m, rs.count('Partial') / m, rs.count('No') / m
    bx.barh(i, a, color=YES, height=0.62, edgecolor='white'); bx.barh(i, b, left=a, color=PAR, height=0.62, edgecolor='white')
    bx.barh(i, c, left=a + b, color=NO, height=0.62, edgecolor='white')
    for x0, w, col in [(0, a, 'white'), (a, b, '#0b0b0b'), (a + b, c, '#0b0b0b')]:
        if w >= 0.08:
            bx.text(x0 + w / 2, i, f'{round(100 * w)}%', ha='center', va='center', fontsize=6.8, color=col)
    bx.text(1.03, i, f'{len(its)} item' + ('s' if len(its) > 1 else ''), va='center', fontsize=7.5, color=TXT2)
bx.set_yticks(range(len(secs))); bx.set_yticklabels([s for s, _ in secs]); bx.tick_params(axis='y', length=0)
bx.set_ylim(len(secs) - 0.5, -0.5); bx.set_xlim(0, 1)
bx.set_xticks([0, .5, 1]); bx.set_xticklabels(['0%', '50%', '100%']); bx.set_xlabel('Share of applicable item ratings, 12 studies pooled')
bx.legend(handles=LEG, loc='upper left', bbox_to_anchor=(-0.6, -0.2), ncol=3, frameon=False, fontsize=7.2)
adh = []
for k in TR:
    v = [VAL[x['r']] for x in A[k]['full_items'].values() if x['r'] in VAL]; adh.append(100 * sum(v) / len(v))
# c: CONSORT-AI, with colours that are not reused from panels a and b
C2010, CAI = '#7a5195', '#ef8a17'
cx = fig.add_subplot(gs[2]); rows = []
for k, nm in [('2', 'ACCESS'), ('24', 'RAIDERS')]:
    for part, items, col in [('CONSORT 2010 items', A[k]['full_items'], C2010), ('AI extension items', A[k]['ai_items'], CAI)]:
        v = [VAL[x['r']] for x in items.values() if x['r'] in VAL]; rows.append((f'{nm}: {part}', 100 * sum(v) / len(v), len(v), col))
for i, (l, v, m, col) in enumerate(rows):
    cx.barh(i, v, color=col, height=0.6, edgecolor='white'); cx.text(v + 1.5, i, f'{v:.0f}% of {m} items', va='center', fontsize=7.2)
cx.set_yticks(range(len(rows))); cx.set_yticklabels([r[0] for r in rows]); cx.tick_params(axis='y', length=0)
cx.set_ylim(len(rows) - 0.5, -0.5); cx.set_xlim(0, 115); cx.set_xticks([0, 25, 50, 75, 100]); cx.set_xlabel('Adherence (%)')
cx.legend(handles=[Patch(color=C2010, label='CONSORT 2010 items'), Patch(color=CAI, label='CONSORT-AI extension items')],
          loc='upper left', bbox_to_anchor=(-0.6, -0.55), ncol=2, frameon=False, fontsize=7.2)
fig.canvas.draw()
panel(fig, ax, 'a', 'AI measurement studies (n = 22): ten domains adapted from CONSORT-AI')
panel(fig, bx, 'b', f'Prediction and diagnostic model studies (n = 12): TRIPOD+AI, median adherence {st.median(adh):.0f}%')
panel(fig, cx, 'c', 'Randomized trials of AI interventions (n = 2): CONSORT-AI')
save(fig, 'Fig3_reporting_by_study_type')
print([(r[0], round(r[1], 1), r[2]) for r in rows], 'TRIPOD median', st.median(adh))

# ---------- Supplementary Fig. 1: TRIPOD+AI item-level heatmap
items = list(A[TR[0]]['full_items'].keys())
H = np.full((len(TR), len(items)), np.nan)
for i, k in enumerate(TR):
    for j, it in enumerate(items):
        H[i, j] = VAL.get(A[k]['full_items'][it]['r'], np.nan)
cmap = ListedColormap([NO, PAR, YES]); cmap.set_bad('white')
fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.imshow(np.ma.masked_invalid(H), cmap=cmap, norm=BoundaryNorm([-.25, .25, .75, 1.25], 3), aspect='auto', interpolation='none')
ax.set_xticks(np.arange(-.5, len(items), 1), minor=True); ax.set_yticks(np.arange(-.5, len(TR), 1), minor=True)
ax.grid(which='minor', color='white', lw=0.8); ax.tick_params(which='minor', length=0)
ax.set_yticks(range(len(TR))); ax.set_yticklabels([R[k]['study'].split(' (')[0] for k in TR], fontsize=6.5)
ax.set_xticks(range(len(items))); ax.set_xticklabels(items, rotation=90, fontsize=5.5)
for s in ax.spines.values():
    s.set_visible(False)
ax.legend(handles=LEG + [Patch(facecolor='white', edgecolor='#8a8984', label='Not applicable')], loc='lower center',
          bbox_to_anchor=(0.5, 1.01), ncol=4, frameon=False, fontsize=7)
fig.subplots_adjust(left=0.2, right=0.98, top=0.88, bottom=0.17)
save(fig, 'FigS1_tripod_items')
