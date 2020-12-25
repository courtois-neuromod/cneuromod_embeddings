---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.8.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from dypac_utils import visu_repro, load_dypac, subject_keys
```

```{code-cell} ipython3
root_data = '/data/cisl/pbellec/cneuromod_embeddings/xp_202012/repro_friends-s01'
```

```{code-cell} ipython3
fwhm = (5, 8)
cluster = (20, 20, 50, 50, 300)
state = (60, 120, 150, 300, 900)
list_subject = subject_keys(6)
```

```{code-cell} ipython3
def parameter_keys(fwhm=[5]):
    cluster = (20, 20, 50, 50, 300)
    state = (60, 120, 150, 300, 900)
    list_keys = []
    for numf in range(len(fwhm)):
        for nump in range(len(cluster)):
            list_keys.append(f'fwhm-{fwhm[numf]}_cluster-{cluster[nump]}_state-{state[nump]}')
    return list_keys
```

```{code-cell} ipython3
import re
def load_repro(root_data, list_keys, skip_fwhm=True):
    val = np.array([])
    all_label = np.array([])
    type_comp = np.array([])

    for key in list_keys:
        print(key)
        file_repro = os.path.join(root_data, f'Rmatch_{key}.p')
        R = pickle.load(open(file_repro, 'rb'))
        for sub1 in list_subject:
            for sub2 in list_subject:
                match_val = np.max(R[sub1][sub2], axis=1)
                val = np.append(val, match_val)
                if skip_fwhm:
                    label = re.search('.......(.+)', key).group(1)
                else:
                    label = key
                all_label = np.append(all_label, np.repeat(label, match_val.shape[0]))
                if sub1 == sub2:
                    type_comp = np.append(type_comp, np.repeat('intra', match_val.shape[0]))
                else:
                    type_comp = np.append(type_comp, np.repeat('inter', match_val.shape[0]))
    return val, all_label, type_comp
```

```{code-cell} ipython3
list_keys = parameter_keys([5])
val, all_label, type_comp = load_repro(root_data, list_keys)
sns.set_theme(style="whitegrid")
sns.set(font_scale=1.5)
fig = plt.figure(figsize=(20, 15))
sns.boxenplot(x=all_label, y=val, hue=type_comp, scale='area')
plt.ylabel('Parcel reproducibility (even vs odd runs friends-s01)')
plt.title('FWHM=5')
```

```{code-cell} ipython3
list_keys = parameter_keys([8])
val, all_label, type_comp = load_repro(root_data, list_keys)
sns.set_theme(style="whitegrid")
sns.set(font_scale=1.5)
fig = plt.figure(figsize=(20, 15))
sns.boxenplot(x=all_label, y=val, hue=type_comp, scale='area')
plt.ylabel('Parcel reproducibility (even vs odd runs friends-s01)')
plt.title('FWHM=8')
```

```{code-cell} ipython3
list_keys = parameter_keys([5])
val, all_label, type_comp = load_repro(list_keys)
sns.set_theme(style="whitegrid")
sns.set(font_scale=1.5)
fig = plt.figure(figsize=(20, 15))
sns.boxenplot(x=all_label, y=val, hue=type_comp, scale='area')
plt.ylabel('spatial correlation even vs odd runs friends-s01)')
plt.title('Parcel reproducibility FWHM=5')
```

```{code-cell} ipython3
fwhm = (5, 8)
cluster = (20, 20, 50, 50, 300)
state = (60, 120, 150, 300, 900)
list_subject = subject_keys(6)

keys = []
for numf in range(2):
    for nump in range(5):
        keys.append(f'fwhm-{fwhm[numf]}_cluster-{cluster[nump]}_state-{state[nump]}')

intra_val = dict.fromkeys(keys)
inter_val = dict.fromkeys(keys)
for ind in range(len(keys)):
    label = keys[ind]
    print(label)
    file_repro = os.path.join(root_data, f'Rmatch_{label}.p')
    R = pickle.load(open(file_repro, 'rb'))
    intra_tmp = np.array([])
    inter_tmp = np.array([])
    for sub1 in list_subject:
        for sub2 in list_subject:
            match_val = np.max(R[sub1][sub2], axis=1)
            if sub1 == sub2:
                intra_tmp = np.append(intra_tmp, match_val)
            else:
                inter_tmp = np.append(inter_tmp, match_val)
    intra_val[label] = intra_tmp
    inter_val[label] = inter_tmp
```

```{code-cell} ipython3
plt.plot(intra_val['fwhm-5_cluster-300_state-900'],'.')
```

```{code-cell} ipython3
list(intra_val.keys())
```

```{code-cell} ipython3
intra = np.array([])
inter = np.array([])
labels_intra = np.array([])
labels_inter = np.array([])
for key in list(intra_val.keys()):
    intra = np.append(intra, intra_val[key])
    labels_intra = np.append(labels_intra, np.repeat(key, intra_val[key].shape[0]))
    inter = np.append(inter, inter_val[key])
    labels_inter = np.append(labels_inter, np.repeat(key, inter_val[key].shape[0]))
```

```{code-cell} ipython3
labels_intra
```

```{code-cell} ipython3
sns.boxenplot?
```

```{code-cell} ipython3
sns.set_theme(style="whitegrid")
fig = plt.figure(figsize=(20, 15))
sns.boxenplot(x=labels_intra, y=intra, color='b', scale='area')
```

```{code-cell} ipython3
sns.set_theme(style="whitegrid")
fig = plt.figure(figsize=(20, 15))
sns.boxenplot(x=labels_inter, y=inter, color='b', scale='area')
```

```{code-cell} ipython3

```

```{code-cell} ipython3
diamonds
```

# fwhm-5 cluster-20 state-60

```{code-cell} ipython3
R = np.load(os.path.join(root_data,'Rmatch_fwhm-5_cluster-50_state-300.npy'))
```

```{code-cell} ipython3
root_dypac = '/data/cisl/pbellec/cneuromod_embeddings/xp_202011/'
model, mask_img = load_dypac(subject='sub-04', root_data=root_dypac, fwhm=5, cluster=50, state=300)
```

```{code-cell} ipython3
model.dwell_time.shape()
```

```{code-cell} ipython3
model.dwell_time_==0
```

```{code-cell} ipython3
val_measures = np.max(R[:, :, 4, 4], axis=1)
plt.plot(model.dwell_time_,val_measures,'.')
```

```{code-cell} ipython3
R = np.load(os.path.join(root_data,'Rmatch_fwhm-5_cluster-20_state-60.npy'))
visu_repro(R)
```

# fwhm-5 cluster-20 state-120

```{code-cell} ipython3
R = np.load('/data/cisl/pbellec/cneuromod_embeddings/xp_202012/friends-s01_reproducibility/Rmatch_fwhm-5_cluster-20_state-120.npy')
visu_repro(R)
```

# fwhm-5 cluster-50 state-150

```{code-cell} ipython3
R = np.load('/data/cisl/pbellec/cneuromod_embeddings/xp_202012/friends-s01_reproducibility/Rmatch_fwhm-5_cluster-50_state-150.npy')
visu_repro(R)
```

# fwhm-5 cluster-50 state-300

```{code-cell} ipython3
R = np.load('/data/cisl/pbellec/cneuromod_embeddings/xp_202012/friends-s01_reproducibility/Rmatch_fwhm-5_cluster-50_state-300.npy')
visu_repro(R)
```

# fwhm-5 cluster-30 state-900

```{code-cell} ipython3
R = np.load('/data/cisl/pbellec/cneuromod_embeddings/xp_202012/friends-s01_reproducibility/Rmatch_fwhm-5_cluster-300_state-900.npy')
visu_repro(R)
```
