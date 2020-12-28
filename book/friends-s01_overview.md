friends-s01
===========

We first implemented a series of experiments to explore the impact of different parameters on the quality of embeddings in the `friends-s01` dataset. We ordered all fMRI runs for each subject by chronological order, and separated the `even` runs (training data) from the `odd` runs (validation data). We generated several dynamic parcellations using dypac independently on `friends-s01` training and validation datasets. We explored different parameters, both for the number of clusters and the number of states: `cluster-20_state-60`, `cluster-20_state120`, `cluster-50_state-150`, `cluster-50_state-300`and `cluster-300_state-900`. We also tested two different levels of spatial smoothing: `fwhm=5` and `fwhm=8`. 

The results of these experiments was that `cluster-20_state-60` was the most spatially subject-specific, while `cluster-300_state-900` provided the best approximation of voxel-level data. This approximation was near-perfect for `fwhm=8`, and good for `fwhm=5`. We thus decided to generate final parcellations using the entirety of `friends-s01` with `fwhm=5`, which offers a much better spatial resolution, and two different scales: `cluster-20_state-60`, as well as `cluster-300_state-900`. 

