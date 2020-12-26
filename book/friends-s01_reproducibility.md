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

# Test-retest reproducibility (friends-s01 split-half)

```{code-cell} ipython3
import os
from cneuromod_embeddings import dypac_utils
from cneuromod_embeddings.repro_summary import repro_df
import seaborn as sns
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
root_path, basename = os.path.split(dypac_utils.__file__)
root_data = os.path.join(root_path, 'friends-s01', 'repro_friends-s01')
val_repro = repro_df(root_data)
params = dypac_utils.dypac_params()
sns.set_theme(style="whitegrid")
sns.set(font_scale=1.5)
```

## Intra- vs inter-subject, `fwhm=5`, all subjects

```{code-cell} ipython3
fwhm=5
fig = plt.figure(figsize=(20, 15))
data = val_repro[val_repro['fwhm']==fwhm]
sns.boxenplot(data=data, x='params', y='spatial_r', hue='type_comp', scale='area')
plt.ylabel('Parcel reproducibility (even vs odd runs friends-s01)')
plt.title(f'FWHM={fwhm} all subjects pooled')
```

## Intra- vs inter-subject, `fwhm=8`, all subjects

```{code-cell} ipython3
fwhm=8
fig = plt.figure(figsize=(20, 15))
data = val_repro[val_repro['fwhm']==fwhm]
sns.boxenplot(data=data, x='params', y='spatial_r', hue='type_comp', scale='area')
plt.ylabel('Parcel reproducibility (even vs odd runs friends-s01)')
plt.title(f'FWHM={fwhm} all subjects pooled')
```

## Intra- vs inter-subject, `fwhm=5`, per subject

```{code-cell} ipython3
fwhm=5
for ind, cluster in enumerate(params['cluster']):
    state = params['state'][ind]
    key = f'cluster-{cluster}_state-{state}' 
    fig = plt.figure(figsize=(20, 15))
    data = val_repro[val_repro['fwhm']==fwhm][val_repro['params']==key]
    sns.boxenplot(data=data, x='subject', y='spatial_r', hue='type_comp', scale='area')
    plt.ylabel('Parcel reproducibility (even vs odd runs friends-s01)')
    plt.title(f'FWHM={fwhm} params={key}')
```

## Intra- vs inter-subject, `fwhm=8`, per subject

```{code-cell} ipython3
fwhm=8
for ind, cluster in enumerate(params['cluster']):
    state = params['state'][ind]
    key = f'cluster-{cluster}_state-{state}' 
    fig = plt.figure(figsize=(20, 15))
    data = val_repro[val_repro['fwhm']==fwhm][val_repro['params']==key]
    sns.boxenplot(data=data, x='subject', y='spatial_r', hue='type_comp', scale='area')
    plt.ylabel('Parcel reproducibility (even vs odd runs friends-s01)')
    plt.title(f'FWHM={fwhm} params={key}')
```
