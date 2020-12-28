---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.7.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# R2 maps

```{code-cell} ipython3
from dypac import Dypac
from dypac.bascpp import stab_maps
import numpy as np
import matplotlib.pyplot as plt
from nilearn.input_data import NiftiMasker
from nilearn import plotting
from cneuromod_embeddings.dypac_utils import get_root_data, load_dypac, load_r2_intra, load_r2_inter, load_r2_other, mean_r2, mean_inter_r2
```

```{code-cell} ipython3
subject = 'sub-01'
fwhm = '5'
cluster = 300
state = 900
root_data = get_root_data('friends-s01')
model, mask_img = load_dypac(subject=subject, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state)
```

```{code-cell} ipython3
width_fig = 20
fig = plt.figure(figsize=(width_fig, 3))
hdf5_file = load_r2_intra(subject=subject, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state)
r2_intra = mean_r2(hdf5_file['validation'], ref_img=mask_img)
plotting.plot_stat_map(r2_intra, cut_coords=[2, -30, 15], display_mode='ortho', threshold=0.1, 
    vmax=1, title=f'r2_{subject}_intra', colorbar=False, axes=plt.subplot(1, 2, 1))
hdf5_file = load_r2_inter(subject=subject, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state)
r2_inter = mean_inter_r2(hdf5_file['inter'], ref_img=mask_img)
plotting.plot_stat_map(r2_inter, cut_coords=[2, -30, 15], display_mode='ortho', threshold=0.1, 
    vmax=1, title=f'r2_{subject}_inter', colorbar=False, axes=plt.subplot(1, 2, 2))
```

```{code-cell} ipython3
list_atlas = ['smith', 'mist197', 'mist444', 'schaefer', 'difumo256', 'difumo512', 'difumo1024']
n_comp = len(list_atlas)
width_fig = 20
fig = plt.figure(figsize=(width_fig, n_comp * 3))

for ind, atlas in enumerate(list_atlas):
    hdf5_file = load_r2_other(atlas=atlas, root_data=root_data, fwhm=fwhm)
    r2_atlas = mean_r2(hdf5_file[subject], ref_img=mask_img)
    plotting.plot_stat_map(r2_atlas, cut_coords=[2, -30, 15], display_mode='ortho', threshold=0.1, 
            vmax=1, title=f'r2_{subject}_{atlas}', colorbar=False, 
            axes=plt.subplot(n_comp, 2, ind + 1))
```
