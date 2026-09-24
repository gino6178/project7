"""SMPL-X fit (paper 1, §3.6) -- paper-figure style: unknowns -> objective terms -> what each pins, with the numbers.
Export: SVG + PDF + PNG."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
INK, MUT, LINE = '#1a1a1a', '#6b6b6b', '#d9d9d9'; ACC, ACC2 = '#0e7c7b', '#e8552f'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK, 'svg.fonttype': 'none', 'pdf.fonttype': 42})
fig = plt.figure(figsize=(14.0, 5.0), dpi=200); fig.patch.set_facecolor('white')
AX = fig.add_axes([0, 0, 1, 1]); AX.set_xlim(0, 1); AX.set_ylim(0, 1); AX.axis('off')


def blk(x, y, w, h, name, spec='', col=ACC, fs=8.0, lw=1.4, fill=True, top=False):
    face = ({ACC: '#e6f2f1', ACC2: '#fdeee9', LINE: 'white'}[col]) if fill else 'white'
    AX.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.003,rounding_size=0.008', lw=lw, ec=col, fc=face, zorder=2))
    if top:      # tall boxes: title at the top, the list below it
        AX.text(x + w / 2, y + h - 0.045, name, ha='center', va='center', fontsize=fs + 0.8, weight='bold', zorder=3)
        AX.text(x + w / 2, y + (h - 0.09) / 2 + 0.01, spec, ha='center', va='center', fontsize=fs - 0.6, color=MUT, zorder=3, linespacing=1.4)
        return
    AX.text(x + w / 2, y + h / 2 + (0.024 if spec else 0), name, ha='center', va='center', fontsize=fs + 0.8, weight='bold', zorder=3)
    if spec: AX.text(x + w / 2, y + h / 2 - 0.026, spec, ha='center', va='center', fontsize=fs - 0.6, color=MUT, zorder=3, linespacing=1.3)


def arrow(x0, y0, x1, y1, col=INK, lw=1.3, ls='-', rad=0.0):
    AX.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=10, lw=lw, color=col, linestyle=ls, connectionstyle='arc3,rad=%.2f' % rad, zorder=1))


AX.text(0.03, 0.935, 'Body fit: what is solved, what each term pins', fontsize=14, weight='bold')
AX.text(0.03, 0.875, 'Per frame against one broadcast skeleton, warm-started; then the whole sequence together.', fontsize=8.6, color=MUT)

# unknowns
blk(0.030, 0.30, 0.140, 0.44, 'unknowns', 'orientation   3\nlatent pose  32\ntranslation   3\nshape        10\n\n48 per body', ACC2, fs=8.0, top=True)
# objective terms, each with what it pins
terms = [('reprojection', '17 joints, Huber\nthrough the venue P', 'the pose'),
         ('ankle anchor', 'ankle px → court plane', 'the depth\n(else −0.8 m)'),
         ('sole contact', 'lowest vertex at z = 0', 'the height\n(joint is 7 cm up)'),
         ('pose prior', 'decoded VPoser latent', 'the manifold\n(no L2 to T-pose)')]
for i, (n, sp, pin) in enumerate(terms):
    x = 0.225 + i * 0.165
    blk(x, 0.50, 0.140, 0.24, n, sp, ACC, fs=7.8)
    AX.text(x + 0.070, 0.455, 'pins', ha='center', fontsize=6.8, color=MUT, style='italic')
    AX.text(x + 0.070, 0.395, pin, ha='center', va='center', fontsize=7.6, color=ACC2, weight='bold', linespacing=1.3)
    arrow(x + 0.070, 0.50, x + 0.070, 0.470, col=MUT, lw=0.9)
arrow(0.170, 0.62, 0.225, 0.62)
for i in range(3):
    arrow(0.365 + i * 0.165, 0.62, 0.390 + i * 0.165, 0.62, col=LINE, lw=1.0)
AX.text(0.555, 0.78, 'summed objective, Adam, 120 steps per frame', ha='center', fontsize=7.0, color=MUT, style='italic')

# then the sequence
blk(0.225, 0.13, 0.635, 0.17, 'then the whole sequence at once', 'one shape per player  ·  second-difference penalties on latent, orientation, translation  ·  replaces post-hoc filtering', ACC, fs=8.0)
arrow(0.555, 0.36, 0.555, 0.30, col=MUT, lw=1.0)

# result
blk(0.905, 0.30, 0.070, 0.44, 'out', 'reproj\n3.8 px\n\njoint speed\np99 253°/s\n\nmax angle\n111°', LINE, fs=7.2, fill=False, top=True)
arrow(0.860, 0.62, 0.905, 0.62)
for ext in ('png', 'svg', 'pdf'):
    fig.savefig('assets/fig_smplx_fit.%s' % ext, facecolor='white', bbox_inches='tight', pad_inches=0.05)
print('wrote assets/fig_smplx_fit.{png,svg,pdf}')
