"""The virtual court: what is placed where, and where the camera stands (paper 1, section 3.6).

FIGURE CONTRACT
---------------
Core conclusion: the scene is not a stylised court. Every dimension is the BWF specification or a
    measured broadcast camera, and the figure gives the reader the numbers to check it against.
Panel (a) is a plan view: court, service lines, net, the twin's actual camera position, and the
    range of camera positions the corpus spans.
Panel (b) is the elevation the plan cannot show: camera height and depression, the net's two
    heights and its 26 mm sag, and a solved flight passing over.
Review risk: "a Blender court" reads as decoration. Drawing the measured camera envelope, and the
    sag that gates the calibration, is what makes it a measurement instrument instead.
Export: SVG (editable text) + PDF (Type 42) + PNG.
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon, Arc, Circle

INK, MUT, LINE = '#141b1e', '#5c6b70', '#dfe6e5'
ACC, ACC2, SOFT, WARM = '#0e7c7b', '#e8552f', '#e9f3f2', '#fdf3ee'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK,
                     'svg.fonttype': 'none', 'pdf.fonttype': 42})

W, L, NET = 6.10, 13.40, 6.70
fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor('white')
fig.text(0.035, 0.950, 'The virtual court is the specification, and the camera is a measured one',
         fontsize=14.5, weight='bold')
fig.text(0.035, 0.902, 'Nothing in the scene is chosen for looks: court and net follow BWF dimensions, and the camera is solved from the broadcast it reconstructs.',
         fontsize=9.2, color=MUT)

# ------------------------------------------------------------------ (a) plan
A = fig.add_axes([0.030, 0.075, 0.400, 0.780]); A.axis('off')
A.set_aspect('equal'); A.set_xlim(-7.5, 13.6); A.set_ylim(-2.2, 27.5)
A.text(-7.2, 26.6, '(a)  plan', fontsize=9.6, weight='bold')

A.add_patch(Rectangle((-1.4, -1.4), W + 2.8, L + 2.8, fc='#eef4f5', ec='none'))
A.add_patch(Rectangle((0, 0), W, L, fc=SOFT, ec=ACC, lw=1.4))
for y in (0.76, NET - 1.98, NET + 1.98, L - 0.76):                     # service lines
    A.plot([0, W], [y, y], color=ACC, lw=0.8, alpha=0.65)
for x in (0.46, W / 2, W - 0.46):                                      # side and centre lines
    A.plot([x, x], [0, L], color=ACC, lw=0.8, alpha=0.65)
A.plot([0, W], [NET, NET], color=INK, lw=2.2)                          # net
A.text(W + 0.35, NET, 'net', fontsize=8.4, color=INK, va='center')

CAM = (3.18, 23.36)
A.add_patch(Polygon([[CAM[0], CAM[1]], [-1.2, 1.0], [W + 1.2, 1.0]], closed=True,
                    fc=ACC, alpha=0.09, ec='none'))
A.plot([CAM[0], -1.2], [CAM[1], 1.0], color=ACC, lw=0.9, ls=(0, (4, 3)))
A.plot([CAM[0], W + 1.2], [CAM[1], 1.0], color=ACC, lw=0.9, ls=(0, (4, 3)))
A.add_patch(Circle(CAM, 0.42, fc=WARM, ec=ACC2, lw=1.6, zorder=5))
A.text(CAM[0] + 0.75, CAM[1] + 0.35, 'camera of the reconstructed clip\n(3.18, 23.36, 4.91) m',
       fontsize=8.3, color=ACC2)

A.annotate('', xy=(-2.6, 0), xytext=(-2.6, L), arrowprops=dict(arrowstyle='<|-|>', color=MUT, lw=1.0))
A.text(-3.0, L / 2, '13.40 m', fontsize=8.4, color=MUT, rotation=90, va='center', ha='right')
A.annotate('', xy=(0, -2.0), xytext=(W, -2.0), arrowprops=dict(arrowstyle='<|-|>', color=MUT, lw=1.0))
A.text(W / 2, -2.35, '6.10 m', fontsize=8.4, color=MUT, ha='center', va='top')
A.annotate('', xy=(W + 2.4, NET), xytext=(W + 2.4, CAM[1]), arrowprops=dict(arrowstyle='<|-|>', color=ACC, lw=1.0))
A.text(W + 2.7, (NET + CAM[1]) / 2, 'the camera sits\nbehind the baseline', fontsize=8.2, color=ACC, va='center')

# ------------------------------------------------------------------ (b) elevation
B = fig.add_axes([0.480, 0.075, 0.500, 0.780]); B.axis('off')
B.set_aspect('equal'); B.set_xlim(-2.0, 28.0); B.set_ylim(-2.6, 12.6)
B.text(-1.8, 11.9, '(b)  elevation, looking along the net', fontsize=9.6, weight='bold')

B.plot([0, 26.0], [0, 0], color=INK, lw=1.4)                            # floor
B.text(0.2, -0.85, 'court plane, z = 0', fontsize=8.2, color=MUT)
B.add_patch(Rectangle((0, 0), 13.40, 0.06, fc=SOFT, ec=ACC, lw=1.0))
B.plot([NET, NET], [0, 1.524], color=INK, lw=2.0)
B.plot([NET, NET], [1.524, 1.55], color=ACC2, lw=2.0)
B.annotate('net: posts 1.55 m, centre 1.524 m\n26 mm sag — withheld as the gate (§3.1)',
           xy=(NET, 1.60), xytext=(NET - 1.4, 6.6), fontsize=8.2, color=ACC2, ha='center',
           arrowprops=dict(arrowstyle='-', color=ACC2, lw=0.9, shrinkA=2, shrinkB=2))

camx, camz = 23.36, 4.91
B.add_patch(Polygon([[camx, camz], [0.0, 0.0], [0.0, 3.4]], closed=True, fc=ACC, alpha=0.09, ec='none'))
B.plot([camx, 0.0], [camz, 0.0], color=ACC, lw=0.9, ls=(0, (4, 3)))
B.plot([camx, 0.0], [camz, 3.4], color=ACC, lw=0.9, ls=(0, (4, 3)))
B.add_patch(Circle((camx, camz), 0.34, fc=WARM, ec=ACC2, lw=1.6, zorder=5))
B.plot([camx, camx], [0, camz], color=MUT, lw=0.9, ls=(0, (2, 2)))
B.annotate('', xy=(camx + 1.1, 0), xytext=(camx + 1.1, camz), arrowprops=dict(arrowstyle='<|-|>', color=MUT, lw=1.0))
B.text(camx + 1.4, camz / 2, '4.91 m', fontsize=8.4, color=MUT, va='center')
B.plot([camx, camx - 6.0], [camz, camz], color=MUT, lw=0.8)
B.add_patch(Arc((camx, camz), 8.0, 8.0, angle=0, theta1=180, theta2=192, color=ACC, lw=1.2))
B.text(camx - 6.4, camz + 0.55, 'depression 12°', fontsize=8.2, color=ACC, ha='right')

t = np.linspace(0, 1, 120)
arcx = 1.2 + 11.0 * t
arcz = 1.0 + 9.6 * t - 8.4 * t ** 2
B.plot(arcx, arcz, color=ACC2, lw=1.6, alpha=0.9)
B.text(7.5, 4.35, 'a solved flight (§3.2)', fontsize=8.2, color=ACC2, ha='center')

B.text(-1.8, -1.75, 'measured across the corpus (n = 11):  focal 1179–3756 px   |   height 2.6–13.3 m   |   '
                    'distance 12.0–38.7 m   |   depression −10.5 to 20.5°',
       fontsize=8.3, color=MUT)
B.text(-1.8, -2.45, 'The WACV 2026 table-tennis synthetic range is 7–17 m at 30–70°: zero overlap in elevation. '
                    'Camera geometry has to be measured per sport.', fontsize=8.3, color=ACC)

for ext in ('png', 'svg', 'pdf'):
    fig.savefig('assets/fig_virtual_court.%s' % ext, facecolor='white', bbox_inches='tight', pad_inches=0.06)
print('wrote assets/fig_virtual_court.{png,svg,pdf}')
