Decentralized SPTD(0)
================================

Author: Jiahua Ma
Research topic: Decentralized Stochastic Preconditioned TD(0) for Off-Policy Policy Evaluation

Repository: https://github.com/baerkesi26710/Decentralized-SPTD-0
Version: v1.0.0
No Zenodo DOI is currently assigned.
It contains the simulation notebooks and saved results corresponding to the manuscript figures.
No experimental result was modified during figure export.

Quick start
-----------
Python 3.12 is recommended. From this folder:
    python -m pip install -r requirements.txt
    python export_figures.py

The export command redraws from saved numerical arrays. It does NOT rerun simulations.
Open notebooks/ in Jupyter to examine or rerun the full experiments.
When running all notebook cells, execute them in order. Full simulations can take substantially
longer than replotting; they write fresh results to the relative output directories defined in
the parameter cells. The archived article data in data/ are retained separately.

Files
-----
notebooks/convergence_rate_experiment.ipynb: all convergence examples, algorithms and plotting.
notebooks/preconditioner_sensitivity.ipynb: preconditioner sensitivity experiment.
data/: archived numerical arrays, CSV summaries, experiment configurations and diagnostics.
figures/: individual vector PDFs / 800 dpi PNGs, plus compound PDF and 800 dpi TIFF artwork.
figure-index.csv: mapping between manuscript figures, archived results and notebook cells.
verification.json: raw-data SHA-256 hashes and export verification information.

Convergence experiments
-----------------------
All curves are means over 10 independent runs, with 10000 online samples and checkpoint spacing 20.
All plotted errors are Euclidean parameter errors normalized by the norm of theta*.
No smoothing, interpolation or confidence bands were added. Original plot limits are retained.
Some unstable TD curves leave the displayed y-axis range; full numerical values remain in data/.
The horizontal axis excludes presampling and does not represent wall-clock or communication cost.

Cliff: T0=500, T0'=7, T'=7, K=8, seed=1000, alpha=0.005, alpha0=10;
       TDC auxiliary steps are 0.01 times the primary steps.
Two-state diagnostic: T0=999, T0'=7, T'=7, K=1, seed=1000, alpha=0.002, alpha0=3;
       TDC auxiliary steps are 0.01 and 6/(t+1).
Chen synthetic MDP, both networks: T0=800, T0'=5, T'=5, K=5, trajectory seed=30000;
       environment seed=20210501, alpha=0.02, alpha0=7, TDC beta/alpha=0.01.
Full settings and any projection diagnostics are in each archived config.json / diagnostics.json.
The empirical runs are not guaranteed to meet the stronger sufficient preconditioner bound
max_n ||M^n A-I|| <= 1/2. They must not be described as verifying every theorem assumption.

Sensitivity experiment
----------------------
The plotted curves are medians over 20 independent Markov runs.
T0={50,100,200,400,800,999,1600,3200,6400,12800}.
T0'={2,3,5,8,12,20,40,80,120}. Environment seed=20210501, trajectory seed=91000.
The figure displays T0'={2,5,12,40,120}, and the horizontal reference line is DM=1.
Only the dense x-axis tick label 999 is omitted; its data point is retained.
The archived CSV's pass_rate_le_half column refers to DM <= 1/2; it is a different statistic
from the DM=1 line used in the manuscript. Its values must not be relabelled as pass rates at 1.

Figure numbering
----------------
The reviewed manuscript has four main figures. Main Figure 4 combines the original manuscript's
two unstable-example figures (constant and diminishing schedules) into one 3-by-2 exhibit.
Supplement S1 is the environment diagram supplied separately with the manuscript; it is not
included in this code/data release. S2 and S3 are the two cliff convergence exhibits.

Verification scope
------------------
The exporter has been executed against every archived result folder, and source cells compile.
Exported PDF curves and labels are vector elements with embedded fonts; TIFFs are real 800 dpi
renderings of the artwork. Original numerical arrays were hashed before and after export and
were unchanged. Full simulations were not rerun during this figure-only revision.

Attribution and license
-----------------------
The synthetic MDP and ratio-communication baseline follow Chen, Zhou and Chen,
Multi-Agent Off-Policy TDC with Near-Optimal Sample and Communication Complexities,
Transactions on Machine Learning Research (2022), https://openreview.net/forum?id=tnPjQpYk7D.
SPTD builds on Liu, Ma, Mao and Tang (2025), https://doi.org/10.1109/TPAMI.2025.3572807.
No publisher PDFs, third-party source repositories or manuscript files are included here.
No open-source reuse license is currently selected. The author should select a suitable
license and confirm attribution/rights before public release. Public visibility alone does
not grant general reuse rights.

Archiving suggestion
----------------------
This code/data set is published in the public GitHub repository linked above. The v1.0.0 tag
identifies the uploaded version.
For a persistent scholarly citation, archive the same release on Zenodo and use its DOI in the
manuscript's Data Availability Statement. The repository link can be used in the manuscript after verifying its public accessibility.
