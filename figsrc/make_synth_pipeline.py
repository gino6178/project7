"""Image-level synthesis pipeline (paper 1, §3.6) -- paper-figure style: modules, short labels, numbers on the arrows they pin.
Export: SVG + PDF + PNG."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
INK, MUT, LINE = '#1a1a1a', '#6b6b6b', '#d9d9d9'; ACC, ACC2 = '#0e7c7b', '#e8552f'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK, 'svg.fonttype': 'none', 'pdf.fonttype': 42})
fig = plt.figure(figsize=(14.0, 5.6), dpi=200); fig.patch.set_facecolor('white')
AX = fig.add_axes([0, 0, 1, 1]); AX.set_xlim(0, 1); AX.set_ylim(0, 1); AX.axis('off')


def blk(x, y, w, h, name, spec='', col=ACC, fs=8.0, lw=1.4, fill=True):
    face = ({ACC: '#e6f2f1', ACC2: '#fdeee9', LINE: 'white'}[col]) if fill else 'white'
    AX.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.003,rounding_size=0.008', lw=lw, ec=col, fc=face, zorder=2))
    AX.text(x + w / 2, y + h / 2 + (0.022 if spec else 0), name, ha='center', va='center', fontsize=fs + 0.8, weight='bold', zorder=3)
    if spec: AX.text(x + w / 2, y + h / 2 - 0.024, spec, ha='center', va='center', fontsize=fs - 0.6, color=MUT, zorder=3, linespacing=1.3)


def arrow(x0, y0, x1, y1, col=INK, lw=1.3, ls='-', rad=0.0, label='', lx=None, ly=None, lc=None):
    AX.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=10, lw=lw, color=col, linestyle=ls, connectionstyle='arc3,rad=%.2f' % rad, zorder=1))
    if label: AX.text(lx if lx is not None else (x0 + x1) / 2, ly if ly is not None else (y0 + y1) / 2 + 0.03, label, ha='center', fontsize=7.0, color=lc or MUT, style='italic', zorder=3)


AX.text(0.03, 0.94, 'Image-level synthesis: every stream is measured from the clip', fontsize=14, weight='bold')
AX.text(0.03, 0.885, 'Four quantities are measured from the broadcast, composed in one metric scene, and the render is checked against the frame it came from.', fontsize=8.6, color=MUT)

blk(0.030, 0.36, 0.105, 0.30, 'broadcast\nclip', 'one rally segment', LINE, fill=False)
ys = [0.700, 0.535, 0.370, 0.205]
blk(0.190, ys[0], 0.165, 0.125, 'camera', 'court lines + net cord\nsag-gated  (§3.1)')
blk(0.190, ys[1], 0.165, 0.125, 'player pose', 'YOLO 2D → SMPL-X\nankles on the court plane')
blk(0.190, ys[2], 0.165, 0.125, 'shutter', 'streak vs speed, per clip\nmedian 1/150 s')
blk(0.190, ys[3], 0.165, 0.125, 'flight', 'launch, landing, duration\nfrom labels; height solved')
for y in ys:
    arrow(0.135, 0.51, 0.190, y + 0.0625, rad=0.12 if y > 0.51 else -0.12)
arrow(0.2725, ys[0], 0.2725, ys[1] + 0.125, col=MUT, lw=1.0)

blk(0.410, ys[1], 0.150, 0.125, 'strike library', '3,144 poses · 8 venues\n51 overhead strikes', ACC2)
arrow(0.355, ys[1] + 0.0625, 0.410, ys[1] + 0.0625)
AX.add_patch(FancyBboxPatch((0.410, 0.13), 0.150, 0.365, boxstyle='round,pad=0.003,rounding_size=0.008', lw=1.4, ec=ACC2, fc='#fdeee9', zorder=2))
AX.text(0.485, 0.455, 'path-traced scene', ha='center', va='center', fontsize=8.8, weight='bold', zorder=3)
AX.text(0.485, 0.30, 'BWF court + net\ntwo bodies, rackets\nshuttle on the flight\nmotion blur at shutter\nmeasured camera\n\n9 s / frame, CPU', ha='center', va='center', fontsize=7.4, color=MUT, zorder=3, linespacing=1.35)
arrow(0.485, ys[1], 0.485, 0.495)
arrow(0.355, ys[2] + 0.0625, 0.410, ys[2] + 0.03)
arrow(0.355, ys[3] + 0.0625, 0.410, ys[3] + 0.02)
arrow(0.355, ys[0] + 0.0625, 0.485, 0.495 + 0.0, rad=-0.35, label='camera', lx=0.43, ly=0.70)

blk(0.630, 0.20, 0.150, 0.30, 'render', '1280 × 720', LINE, fill=False)
arrow(0.560, 0.31, 0.630, 0.35)
# registration numbers, as a compact table on the right
AX.add_patch(FancyBboxPatch((0.815, 0.13), 0.160, 0.53, boxstyle='round,pad=0.003,rounding_size=0.008', lw=1.1, ec=LINE, fc='white', zorder=2))
AX.text(0.895, 0.62, 'vs the same broadcast frame', ha='center', fontsize=7.6, weight='bold', zorder=3)
rows = [('court lines', '2.2 px', ACC), ('players', '3.8 px', ACC), ('camera', '3.9 px', ACC),
        ('detector, vs truth', '2.7 px', ACC), ('heatmap peak', '0.66 / 0.69', ACC), ('streak length', '11.1 / 15.2 px', ACC2)]
for i, (a, b, c) in enumerate(rows):
    AX.text(0.825, 0.565 - i * 0.062, a, fontsize=7.4, color=MUT, zorder=3)
    AX.text(0.965, 0.565 - i * 0.062, b, fontsize=7.4, color=c, ha='right', weight='bold', zorder=3)
AX.text(0.895, 0.155, 'render / real', ha='center', fontsize=6.4, color=MUT, style='italic', zorder=3)
arrow(0.780, 0.35, 0.815, 0.35, label='compare', ly=0.395)
AX.plot([0.083, 0.083, 0.895], [0.36, 0.095, 0.095], color=MUT, lw=0.9, ls=(0, (3, 2)), zorder=1)
arrow(0.895, 0.095, 0.895, 0.128, col=MUT, lw=0.9, ls=(0, (3, 2)))
AX.text(0.50, 0.112, 'the same clip is the ground truth for the check', ha='center', fontsize=7.0, color=MUT, style='italic', backgroundcolor='white')

for i, (c, f, t) in enumerate([(ACC, '#e6f2f1', 'measured from the broadcast'), (ACC2, '#fdeee9', 'built from those measurements')]):
    AX.add_patch(FancyBboxPatch((0.030 + i * 0.190, 0.030), 0.012, 0.012, boxstyle='round,pad=0.001,rounding_size=0.002', lw=1.1, ec=c, fc=f))
    AX.text(0.047 + i * 0.190, 0.036, t, fontsize=6.8, color=MUT, va='center')
for ext in ('png', 'svg', 'pdf'):
    fig.savefig('assets/fig_synth_pipeline.%s' % ext, facecolor='white', bbox_inches='tight', pad_inches=0.05)
print('wrote assets/fig_synth_pipeline.{png,svg,pdf}')
