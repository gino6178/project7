"""Schematic + measurement for section 5.8: what the fitted body says about contact-frame depth.

FIGURE CONTRACT
---------------
Core conclusion: the annotated PIXEL agrees with an independently fitted human arm; the
    reconstructed DEPTH along that pixel's ray does not. The figure has to make "along the ray"
    visible, because that is the whole claim -- a reader who sees only "1.37 m apart" will
    conclude the annotation or the body is wrong.
Panel (a) is geometry drawn to scale in the plane containing the camera ray and the wrist.
Panel (b) is the control that makes the measurement credible: the wrist-to-ray distance has a
    clean minimum exactly at the contact frame, so the striker and the frame are right.
Review risk: a schematic with no numbers invites "how far off, and biased which way?". The
    depth interquartile range is therefore drawn as a band on the ray, not described in prose.
Export: SVG (editable text) + PDF (Type 42) + PNG.
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Polygon, FancyBboxPatch

INK, MUT, LINE = '#141b1e', '#5c6b70', '#dfe6e5'
ACC, ACC2, SOFT, WARM = '#0e7c7b', '#e8552f', '#e9f3f2', '#fdf3ee'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK,
                     'svg.fonttype': 'none', 'pdf.fonttype': 42,
                     'axes.linewidth': 0.8})

fig = plt.figure(figsize=(12.2, 5.4), dpi=200)
fig.patch.set_facecolor('white')
fig.text(0.035, 0.950, 'The annotated pixel agrees with the arm. The depth along that pixel’s ray does not.',
         fontsize=14, weight='bold')
fig.text(0.035, 0.892, 'At the contact frame, over 58 contacts in 8 venues. The fitted body never sees a shuttle annotation.',
         fontsize=9.2, color=MUT)

# ------------------------------------------------------------------ (a) geometry, in the ray-wrist plane
A = fig.add_axes([0.035, 0.10, 0.545, 0.74]); A.axis('off')
A.set_xlim(-0.5, 11.6); A.set_ylim(-1.9, 5.9)
A.text(-0.4, 5.5, '(a)  in the plane through the camera centre and the wrist', fontsize=9.4, weight='bold')

A.add_patch(Polygon([[0.0, 3.0], [1.1, 3.6], [1.1, 2.4]], closed=True, fc=SOFT, ec=ACC, lw=1.4))
A.text(0.30, 2.05, 'camera', fontsize=8.6, color=MUT)

ray0, ray1 = np.array([1.1, 3.0]), np.array([11.3, 3.55])
d = (ray1 - ray0) / np.linalg.norm(ray1 - ray0)
A.plot([ray0[0], ray1[0]], [ray0[1], ray1[1]], color=INK, lw=1.3, zorder=3)
A.text(2.0, 3.30, 'line of sight through the annotated pixel', fontsize=8.6, style='italic',
       rotation=np.degrees(np.arctan2(d[1], d[0])), rotation_mode='anchor')

W = np.array([7.3, 0.95])
t = float(np.dot(W - ray0, d)); Q = ray0 + t * d
R = ray0 + (t + 1.35) * d

# depth band on the ray, drawn first so the markers sit on top
P0, P1 = Q + (-0.93) * d, Q + 1.34 * d
A.plot([P0[0], P1[0]], [P0[1], P1[1]], color=ACC, lw=9, alpha=0.22, solid_capstyle='butt', zorder=2)
n = np.array([-d[1], d[0]]) * 0.26
for P in (P0, P1):
    A.plot([P[0] - n[0], P[0] + n[0]], [P[1] - n[1], P[1] + n[1]], color=ACC, lw=1.4, zorder=3)
A.text(5.00, 4.60, 'where the annotation puts the shuttle along the ray:\nIQR −0.93 to +1.34 m, median bias only −0.06 m',
       fontsize=8.4, color=ACC, ha='center')
A.add_patch(FancyArrowPatch((5.9, 4.22), (float(Q[0]), float(Q[1] + 0.30)), arrowstyle='-|>',
                            mutation_scale=9, lw=1.0, color=ACC, connectionstyle='arc3,rad=-0.25', zorder=3))

# closest approach, wrist, reconstructed point
A.plot([Q[0]], [Q[1]], marker='|', ms=9, color=INK, mew=1.6, zorder=5)
A.add_patch(Circle(W, 0.20, fc=WARM, ec=ACC2, lw=1.7, zorder=6))
A.text(W[0] - 0.35, W[1] - 0.45, 'striking wrist, fitted\nfrom the 2D skeleton', fontsize=8.6,
       color=ACC2, ha='center', va='top')
A.add_patch(Circle(R, 0.18, fc='white', ec=INK, lw=1.6, zorder=6))
A.text(R[0] + 0.35, R[1] + 0.30, 'reconstructed\n3D shuttle', fontsize=8.6, color=INK, va='bottom')

A.plot([W[0], Q[0]], [W[1], Q[1]], color=ACC2, lw=1.3, ls=(0, (4, 2.5)), zorder=4)
A.text(W[0] - 0.30, (W[1] + Q[1]) / 2, '0.58 m', fontsize=10.0, color=ACC2, weight='bold', ha='right')
A.text(W[0] - 0.30, (W[1] + Q[1]) / 2 - 0.42, 'about one racket', fontsize=8.2, color=ACC2, ha='right')

A.add_patch(FancyArrowPatch(tuple(W + np.array([0.16, 0.06])), tuple(R - np.array([0.10, 0.16])),
                            arrowstyle='<|-|>', mutation_scale=10, lw=1.2, color=MUT, zorder=4))
A.text(9.15, 1.55, '1.37 m', fontsize=10.0, color=MUT, weight='bold')
A.text(9.15, 1.13, 'beyond arm + racket', fontsize=8.2, color=MUT)

A.plot([-0.4, 11.4], [-1.35, -1.35], color=LINE, lw=1.2)
A.text(-0.4, -1.68, 'court plane  —  the body’s depth is pinned here, by its ankles', fontsize=8.4, color=MUT)

# ------------------------------------------------------------------ (b) the control sweep
B = fig.add_axes([0.665, 0.255, 0.305, 0.555])
off = np.array([-8, -4, 0, 4, 8])
dist = np.array([1.20, 0.86, 0.58, 1.00, 1.44])
B.axhspan(0.44, 0.68, color=WARM, zorder=0)
B.plot(off, dist, marker='o', ms=5.5, color=ACC, lw=1.6, zorder=3)
B.plot([0], [0.58], marker='o', ms=9, mfc=WARM, mec=ACC2, mew=2.0, zorder=4)
B.text(8.2, 0.505, 'one racket', fontsize=8.0, color=ACC2, ha='right', va='center')
B.set_xticks(off); B.set_xlabel('frames from the annotated contact', fontsize=9, labelpad=4)
B.set_ylabel('nearest wrist to the ray (m)', fontsize=9)
B.set_ylim(0.30, 1.62); B.tick_params(labelsize=8.5, length=3)
for sp in ('top', 'right'):
    B.spines[sp].set_visible(False)
for sp in ('left', 'bottom'):
    B.spines[sp].set_color(LINE)
B.set_title('(b)  the control: the minimum is exactly at contact', fontsize=9.4, weight='bold', loc='left', pad=8)
fig.text(0.665, 0.035, 'A wrist that merely happened to lie near the shuttle’s sight-line would not dip at frame 0.\nThis is what rules out a misidentified striker.',
         fontsize=8.4, color=MUT)

for ext in ('png', 'svg', 'pdf'):
    fig.savefig('assets/fig_contact_depth.%s' % ext, facecolor='white', bbox_inches='tight', pad_inches=0.06)
print('wrote assets/fig_contact_depth.{png,svg,pdf}')
