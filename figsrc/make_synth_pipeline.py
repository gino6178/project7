"""Schematic of the image-level synthesis pipeline (paper 1, section 3.6).

FIGURE CONTRACT
---------------
Core conclusion: nothing in the rendered image is invented. Camera, player pose,
    shutter and flight each trace back to a measurement on the broadcast, and the
    figure names the measurement under every stage rather than asserting realism.
Archetype: three input streams converging on one renderer, with the validation
    numbers attached to the arrow they validate.
Review risk: a pipeline diagram that only shows boxes invites "how do you know it
    is registered?". Every box therefore carries the number that pins it.
Export: SVG (editable text) + PDF (Type 42) + PNG.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

INK, MUT, LINE = '#141b1e', '#5c6b70', '#dfe6e5'
ACC, ACC2, SOFT, WARM = '#0e7c7b', '#e8552f', '#e9f3f2', '#fdf3ee'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK,
                     'svg.fonttype': 'none', 'pdf.fonttype': 42})

fig = plt.figure(figsize=(12.4, 6.8), dpi=200)
fig.patch.set_facecolor('white')
AX = fig.add_axes([0, 0, 1, 1]); AX.set_xlim(0, 1); AX.set_ylim(0, 1); AX.axis('off')

AX.text(0.035, 0.955, 'Every pixel traces back to a measurement on the broadcast',
        fontsize=15, weight='bold')
AX.text(0.035, 0.915, 'Four streams are measured from the footage, combined in one metric scene, and the '
                      'result is checked against the frame it was built from.', fontsize=9.2, color=MUT)


def box(x, y, w, h, title, lines, kind='meas', fs=8.2):
    face, edge = (SOFT, ACC) if kind == 'meas' else ((WARM, ACC2) if kind == 'built' else ('white', LINE))
    AX.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008,rounding_size=0.012',
                                lw=1.5, ec=edge, fc=face, zorder=2))
    AX.text(x + w / 2, y + h - 0.050, title, ha='center', fontsize=9.4, weight='bold', zorder=3)
    for i, s in enumerate(lines):
        AX.text(x + w / 2, y + h - 0.088 - i * 0.036, s, ha='center', fontsize=fs, color=MUT, zorder=3)


def arrow(x0, y0, x1, y1, rad=0.0, col=INK, lw=1.5, ls='-'):
    AX.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=13,
                                 lw=lw, color=col, linestyle=ls, zorder=1,
                                 connectionstyle='arc3,rad=%.2f' % rad))


# ---- the source, on the left
box(0.030, 0.545, 0.150, 0.245, 'broadcast clip', ['one rally segment', 'no other input',
                                                   'nothing is authored'], 'src')

# ---- four measured streams
box(0.225, 0.700, 0.235, 0.185, 'camera  (§3.1)', ['court lines + net cord,', 'sag withheld as the gate',
                                                   'renders to 3.9 px of the matrix'])
box(0.225, 0.480, 0.235, 0.185, 'player pose  (§3.6)', ['2D skeleton → SMPL-X through', 'that camera; ankles anchored',
                                                        'on the court, pose = latent'])
box(0.225, 0.260, 0.235, 0.185, 'shutter  (§3.2)', ['streak major axis vs speed,', 'regressed per clip',
                                                    'median 1/150 s, 8× spread'])
box(0.225, 0.082, 0.235, 0.185, 'flight  (§3.2)', ['launch, landing, duration', 'from the annotations;',
                                                   'only the height is solved'])
for y in (0.790, 0.570, 0.350, 0.172):
    arrow(0.180, 0.668, 0.225, y, rad=0.0 if abs(y - 0.668) < 0.06 else (0.10 if y > 0.668 else -0.10))
arrow(0.343, 0.700, 0.343, 0.665, lw=1.2, col=MUT)

# ---- the library is built in the camera's frame, and it is what populates a stroke
box(0.505, 0.480, 0.205, 0.185, 'library of strikes', ['3,144 poses, 8 venues,', '51 overhead-class strikes,',
                                                       'tagged by the annotations'], 'built')
arrow(0.460, 0.572, 0.505, 0.572)

# ---- the renderer
box(0.505, 0.082, 0.205, 0.343, 'path-traced scene', ['court and net at BWF sizes,', 'two bodies from the library,',
                                                      'procedural rackets, shuttle on', 'the solved flight, motion blur',
                                                      'at that clip\'s shutter, and the', 'measured camera  —  9 s/frame'], 'built')
arrow(0.607, 0.480, 0.607, 0.425)
arrow(0.460, 0.350, 0.505, 0.330)
arrow(0.460, 0.172, 0.505, 0.180)

# ---- the check, against the frame the scene was built from
box(0.760, 0.230, 0.210, 0.435, 'registered against the same\nbroadcast frame',
    ['', 'court lines            2.2 px', 'fitted players         3.8 px',
     'camera vs matrix       3.9 px', 'shuttle streak   11.1 vs 15.2 px', '',
     'the streak is the one gap: the', 'render used the corpus median',
     'shutter, not this clip\'s'], 'src', fs=8.4)
arrow(0.710, 0.232, 0.865, 0.230, rad=-0.22)
AX.text(0.775, 0.170, 'render, then compare', fontsize=8.2, color=MUT, style='italic')

for x, c, lab in ((0.032, ACC, 'measured from the broadcast'), (0.300, ACC2, 'built from those measurements'),
                  (0.580, LINE, 'input / verification')):
    AX.add_patch(FancyBboxPatch((x, 0.014), 0.016, 0.016, boxstyle='round,pad=0.002,rounding_size=0.004',
                                lw=1.4, ec=c, fc=SOFT if c == ACC else (WARM if c == ACC2 else 'white')))
    AX.text(x + 0.024, 0.022, lab, fontsize=7.8, color=MUT, va='center')

for ext in ('png', 'svg', 'pdf'):
    fig.savefig('assets/fig_synth_pipeline.%s' % ext, facecolor='white', bbox_inches='tight', pad_inches=0.06)
print('wrote assets/fig_synth_pipeline.{png,svg,pdf}')
