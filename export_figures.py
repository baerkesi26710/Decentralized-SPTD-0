"""This file is copied into the portable article-reproduction package."""
from pathlib import Path
import json,hashlib,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pymupdf as fitz
from PIL import Image

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data';FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
def nb(name):return json.loads((ROOT/'notebooks'/name).read_text(encoding='utf8'))
def execute(n,i,ns):exec(compile(''.join(n['cells'][i]['source']),f'notebook cell {i}','exec'),ns)
def fingerprint(path):return hashlib.sha256(path.read_bytes()).hexdigest()
original_hashes={str(p.relative_to(ROOT)):fingerprint(p) for p in DATA.rglob('*.npz')}

n=nb('convergence_rate_experiment.ipynb');ns={'__name__':'article_export'}
for i in [2,4,6,8,10]:execute(n,i,ns)
for name in ['individual_cliff_result','individual_unstable_two_state_result','synthetic_fully_connected_result','synthetic_ring_result']:
 d=DATA/name;config=json.loads((d/'config.json').read_text(encoding='utf8'));args=config.get('algorithm_config',config)
 cfg=ns['Config'](**args);cfg.online_ratio_rounds=tuple(cfg.online_ratio_rounds)
 diag=json.loads((d/'diagnostics.json').read_text(encoding='utf8'))
 z=np.load(d/'raw_trajectories.npz',allow_pickle=False)
 assert z['curves'].shape[3]==cfg.runs
 assert np.isfinite(z['curves']).all()
 profile='synthetic_'+config['network'] if 'network' in config else cfg.environment
 out=FIG/name;out.mkdir(exist_ok=True)
 ns['draw_individual_plots'](out,z['samples'],z['curves'],np.array([diag['theta_norm']]),cfg,plot_profile=profile)
 print('Exported:',name,flush=True)

n=nb('preconditioner_sensitivity.ipynb');ss={'__name__':'article_export'}
for i in [1,3,5,7,9]:
 # Avoid creating a directory relative to the caller's working directory.
 code=''.join(n['cells'][i]['source'])
 if i==1:code=code.replace('Path("preconditioner_sensitivity_result")',repr(str(FIG/'sensitivity')))
 if i==1:code=code.replace('OUTPUT_DIR = '+repr(str(FIG/'sensitivity')),'OUTPUT_DIR = Path('+repr(str(FIG/'sensitivity'))+')')
 exec(compile(code,f'sensitivity cell {i}','exec'),ss)
z=np.load(DATA/'preconditioner_sensitivity_result/raw_preconditioner_sensitivity.npz',allow_pickle=False)
ss.update({'residuals':z['residuals'],'conditions':z['conditions'],'population_floors':z['population_floors'],
           'median_residual':np.nanmedian(z['residuals'],axis=1)})
ss['T0_VALUES']=z['T0_values'];ss['T0_PRIME_VALUES']=z['T0_prime_values'];ss['NETWORKS']=tuple(z['networks'])
execute(n,15,ss)

def compose(name,paths,labels,cols):
 docs=[fitz.open(p) for p in paths];width=max(d[0].rect.width for d in docs);height=max(d[0].rect.height for d in docs)
 gap=10;head=16;rows=math.ceil(len(docs)/cols);doc=fitz.open()
 page=doc.new_page(width=cols*width+(cols-1)*gap,height=rows*(height+head)+(rows-1)*gap)
 for i,(source,label) in enumerate(zip(docs,labels)):
  x=(i%cols)*(width+gap);y=(i//cols)*(height+head+gap)
  page.insert_text((x+2,y+10),label,fontsize=8,fontname='hebo')
  page.show_pdf_page(fitz.Rect(x,y+head,x+width,y+head+height),source,0)
 out=FIG/'article';out.mkdir(exist_ok=True)
 doc.save(out/(name+'.pdf'),garbage=4,deflate=True)
 pix=page.get_pixmap(matrix=fitz.Matrix(800/72,800/72),alpha=False)
 im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
 im.save(out/(name+'.tiff'),compression='tiff_lzw',dpi=(800,800))
 thumb=page.get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False);thumb.save(out/(name+'-preview.png'))
 for d in docs:d.close()
 doc.close();print('Composed:',name,flush=True)

compose('Ma-Figure-1',[FIG/'sensitivity'/f'residual_vs_T0_{k}.pdf' for k in ['fully_connected','ring']],['(a) Fully connected network','(b) Ring network'],2)
for num,network in [(2,'fully_connected'),(3,'ring')]:
 folder=FIG/f'synthetic_{network}_result'
 compose(f'Ma-Figure-{num}',[folder/f'{schedule}_{metric}.pdf' for schedule in ['constant','decay'] for metric in ['convergence_error','total_error']],['(a) Constant: estimation error','(b) Constant: maximum error','(c) Diminishing: estimation error','(d) Diminishing: maximum error'],2)
folder=FIG/'individual_unstable_two_state_result'
compose('Ma-Figure-4',[folder/f'{s}_{m}.pdf' for m in ['convergence_error','total_error','consensus_error'] for s in ['constant','decay']],['(a) Constant: estimation','(b) Diminishing: estimation','(c) Constant: maximum','(d) Diminishing: maximum','(e) Constant: consensus','(f) Diminishing: consensus'],2)
folder=FIG/'individual_cliff_result'
for num,schedule in [(2,'constant'),(3,'decay')]:
 compose(f'Ma-Figure-S{num}',[folder/f'{schedule}_{m}.pdf' for m in ['convergence_error','total_error','consensus_error']],['(a) Estimation error','(b) Maximum-agent error','(c) Consensus error'],3)
assert original_hashes=={str(p.relative_to(ROOT)):fingerprint(p) for p in DATA.rglob('*.npz')}
manifest={'npz_sha256':original_hashes,'plotting_only':True,'main_figures':4,'supplementary_convergence_figures':2,'raster_export_dpi':800,'note':'Original numerical results and plot limits retained. PDF contains vector paths and embedded fonts.'}
(ROOT/'verification.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('Verified: saved numerical data are unchanged. No simulation was rerun.')
