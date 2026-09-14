"""Schematic of the SMPL-X fit used to populate the scene (paper 1, section 3.6).

FIGURE CONTRACT
---------------
Core conclusion: the body is METRIC, not merely plausible, and three specific terms are what
    make it so. The figure has to show what is optimised, what pins the depth, and what the
    prior is -- because "we fit SMPL-X" is exactly the sentence a reviewer will not accept.
Archetype: unknowns on the left, objective in the middle, the two measurements that pin the
    solution on the right, with the failure each term prevents named under it.
Review risk: readers assume apparent height sets the depth. The figure says, on the diagram,
    that it does not and what happens if you let it (0.8 m toward the camera).
Export: SVG (editable text) + PDF (Type 42) + PNG.
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

INK, MUT, LINE = '#141b1e', '#5c6b70', '#dfe6e5'
ACC, ACC2, SOFT, WARM = '#0e7c7b', '#e8552f', '#e9f3f2', '#fdf3ee'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK,
                     'svg.fonttype': 'none', 'pdf.fonttype': 42})

fig = plt.figure(figsize=(12.4, 5.6), dpi=200)
fig.patch.set_facecolor('white')
AX = fig.add_axes([0, 0, 1, 1]); AX.set_xlim(0, 1); AX.set_ylim(0, 1); AX.axis('off')
AX.text(0.035, 0.945, 'What makes the fitted body metric rather than merely plausible', fontsize=14.5, weight='bold')
AX.text(0.035, 0.897, 'The unknowns are solved per frame against one broadcast skeleton, then the whole sequence is refined together.',
        fontsize=9.2, color=MUT)


def panel(x, y, w, h, title, kind='meas'):
    face, edge = (SOFT, ACC) if kind == 'meas' else ((WARM, ACC2) if kind == 'built' else ('white', LINE))
    AX.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008,rounding_size=0.012',
                                lw=1.5, ec=edge, fc=face, zorder=2))
    AX.text(x + w / 2, y + h - 0.055, title, ha='center', fontsize=9.6, weight='bold', zorder=3)


def lines(x, y, rows, fs=8.3, dy=0.042, col=MUT, ha='left'):
    for i, r in enumerate(rows):
        AX.text(x, y - i * dy, r, fontsize=fs, color=col, ha=ha, zorder=3)


# ---------------- unknowns
panel(0.030, 0.375, 0.200, 0.430, 'what is solved for', 'built')
lines(0.048, 0.705, ['global orientation      3',
                     'pose latent            32',
                     'translation             3',
                     'body shape             10', '',
                     'per frame, warm-started', 'from the previous solution'])
AX.text(0.130, 0.415, '48 numbers per body', ha='center', fontsize=8.6, color=ACC2, weight='bold')

# ---------------- objective
panel(0.270, 0.245, 0.290, 0.560, 'the objective')
rows = [('reprojection of 17 joints', 'weighted Huber, through the', 'venue projection matrix', ACC),
        ('ankle anchor', 'ankle pixels back-projected to', 'the court plane — pins the depth', ACC),
        ('sole contact', 'lowest MESH vertex at z = 0,', 'not the ankle joint (7 cm off)', ACC),
        ('pose prior', 'the pose IS a decoded latent,', 'so implausible poses are unreachable', ACC)]
yy = 0.688
for title, a, b, c in rows:
    AX.text(0.288, yy, title, fontsize=8.8, color=INK, weight='bold', zorder=3)
    AX.text(0.288, yy - 0.036, a, fontsize=8.0, color=MUT, zorder=3)
    AX.text(0.288, yy - 0.070, b, fontsize=8.0, color=MUT, zorder=3)
    yy -= 0.122

# ---------------- what each term prevents
panel(0.600, 0.245, 0.175, 0.560, 'what it prevents', 'built')
prevent = ['fitting to noise in\nlow-confidence joints', 'depth from apparent height:\nboth players pulled\n0.8 m toward the camera',
           'the body floating or\nsinking by 7 cm', 'lunges paid for with\nimplausible joint angles']
yy = 0.700
for i, t in enumerate(prevent):
    AX.text(0.6875, yy, t, fontsize=8.0, color=ACC2, ha='center', va='top', zorder=3, linespacing=1.45)
    yy -= 0.122
for i in range(4):
    AX.add_patch(FancyArrowPatch((0.562, 0.700 - i * 0.122), (0.598, 0.700 - i * 0.122),
                                 arrowstyle='-|>', mutation_scale=9, lw=1.0, color=MUT, zorder=1))

# ---------------- result
panel(0.812, 0.375, 0.158, 0.430, 'what comes out', 'src')
lines(0.891, 0.705, ['reprojection', '3.8 px median', '', 'max joint angle 111°',
                     'joint speed p99', '253 °/s', '', 'on the human manifold'], ha='center')

# ---------------- the sequence stage, underneath
AX.add_patch(FancyBboxPatch((0.030, 0.075), 0.940, 0.135, boxstyle='round,pad=0.008,rounding_size=0.012',
                            lw=1.5, ec=ACC, fc=SOFT, zorder=2))
AX.text(0.050, 0.163, 'then the whole sequence at once', fontsize=9.6, weight='bold', zorder=3)
AX.text(0.050, 0.122, 'One body shape shared across all frames, and second-difference penalties on the latent, the root orientation and the translation.',
        fontsize=8.6, color=MUT, zorder=3)
AX.text(0.050, 0.092, 'This replaces post-hoc smoothing, which filtered in the wrong space: filtering vertices slides the joints, filtering parameters does not.',
        fontsize=8.6, color=MUT, zorder=3)
AX.add_patch(FancyArrowPatch((0.500, 0.245), (0.500, 0.212), arrowstyle='-|>', mutation_scale=10,
                             lw=1.2, color=ACC, zorder=1))
AX.add_patch(FancyArrowPatch((0.230, 0.590), (0.268, 0.590), arrowstyle='-|>', mutation_scale=10, lw=1.2, color=MUT))
AX.add_patch(FancyArrowPatch((0.777, 0.590), (0.810, 0.590), arrowstyle='-|>', mutation_scale=10, lw=1.2, color=MUT))

for ext in ('png', 'svg', 'pdf'):
    fig.savefig('assets/fig_smplx_fit.%s' % ext, facecolor='white', bbox_inches='tight', pad_inches=0.06)
print('wrote assets/fig_smplx_fit.{png,svg,pdf}')
