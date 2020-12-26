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

# Parcel matching (state=60)

```{code-cell} ipython3
import os
import numpy as np
from cneuromod_embeddings.dypac_utils import get_root_data, load_dypac
from cneuromod_embeddings.repro_summary import load_repro, visu_match
```

```{code-cell} ipython3
root_data = get_root_data('friends-s01')
fwhm = 5
cluster = 20
state = 60
R = load_repro(root_data=os.path.join(root_data, 'repro_friends-s01'), fwhm=fwhm, cluster=cluster, state=state)
```

## Intra-subject matching

```{code-cell} ipython3
subject = 'sub-01'
Rintra = R[subject][subject]
match_val = np.max(Rintra, axis=0)
match_pair = np.argmax(Rintra, axis=0)
order = np.argsort(-match_val)
model1, mask_img1 = load_dypac(subject=subject, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state, batch="even")
model2, mask_img2 = load_dypac(subject=subject, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state, batch="odd")
```

### High reproducibility parcels

```{code-cell} ipython3
visu_match(0, 5, model1, model2, order, match_pair, match_val)
```

### Median reproducibility parcels

```{code-cell} ipython3
visu_match(30, 5, model1, model2, order, match_pair, match_val)
```

### Low reproducibility parcels

```{code-cell} ipython3
visu_match(50, 5, model1, model2, order, match_pair, match_val)
```

## Inter-subject matching 

```{code-cell} ipython3
Rintra.shape
model1.components_.shape
```

```{code-cell} ipython3
sub1 = 'sub-01'
sub2 = 'sub-05'
Rintra = R[sub1][sub2]
match_val = np.max(Rintra, axis=1)
match_pair = np.argmax(Rintra, axis=1)
order = np.argsort(-match_val)
model1, mask_img1 = load_dypac(subject=sub1, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state, batch="even")
model2, mask_img2 = load_dypac(subject=sub2, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state, batch="even")
```

### High reproducibility parcels

```{code-cell} ipython3
visu_match(0, 5, model1, model2, order, match_pair, match_val)
```

### Median reproducibility parcels

```{code-cell} ipython3
visu_match(30, 5, model1, model2, order, match_pair, match_val)
```

### Low reproducibility parcels

```{code-cell} ipython3
visu_match(50, 5, model1, model2, order, match_pair, match_val)
```
