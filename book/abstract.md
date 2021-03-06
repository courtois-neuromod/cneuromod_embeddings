---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
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

Abstract  
========

This jupyter book presents the validation of embedding quality of individual brain parcels generated using a scalable dynamic ensemble clustering method called DyPAC, in the Courtois NeuroMod 2020 dataset. The quality of the embedding is validated using measures of spatial reproducibility, and the fidelity of compression of voxel-level data. The generalizability of the parcellation is evaluated on large movie datasets with either homogeneous or heterogeneous content, as well as in a variety of controlled experimental conditions (the functional task localizer of the human connectome project). The individual DyPAC parcels are also compared to a series of publicly available, state-of-the-art group brain parcellations.

Functional brain parcellations are intensively used to reduce the high dimensionality of functional MRI data into more compact representations. In the literature, there exists no consensus regarding the best approach to parcellate individual brain parcellations, despite more than two decades of investigation. The main limitation of previous approaches was that functional parcellations were not highly reproducible and there was loss of information between the original signal and the reduced data. Neglecting the dynamic reconfigurations of these brain regions was among the main reasons for this poor performance in some brain regions including, the heteromodal cortices. Some individual parcellation approaches have recently proposed to improve these performance measures. Still, these approaches were either not scalable enough to replicate on large longitudinal datasets, or it required terabytes of functional MRI data to generate brain parcels. In our previous work, we formalized the parcellation problem as a dynamic approach that identified different spatial reconfigurations or ‘dynamic states of parcellations’ for a  given seed subnetwork called DYPAC 1.0. The scalability of this cluster aggregation approach motivated us to extend it to a full brain implementation called DYPAC 2.0. We used ten hours per subject of training and test data from the cneuromod movie10 dataset. We found low information loss between the reduced and the original data throughout the cerebral cortices, i.e. only 20% information loss. We also found that average within-subject reproducibility reached high scores  for many dynamic states throughout the brain (over .9 training-test spatial correlation). This work opens new research directions to studying the brain dynamics often neglected by previous methods based on static parcellations, and may therefore improve the new clinical applications studying differences in brain interactions in both healthy brains and disease. 
 
