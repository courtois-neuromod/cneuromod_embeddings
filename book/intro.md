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

Validation of individual CNeuroMod embeddings  
=============================================

This jupyter book presents the validation of embedding quality of individual brain parcels generated using a scalable dynamic ensemble clustering method called DyPAC, in the Courtois NeuroMod 2020 dataset. The quality of the embedding is validated using measures of spatial reproducibility, and the fidelity of compression of voxel-level data. The generalizability of the parcellation is evaluated on large movie datasets with either homogeneous or heterogeneous content, as well as in a variety of controlled experimental conditions (the functional task localizer of the human connectome project). The individual DyPAC parcels are also compared to a series of publicly available, state-of-the-art group brain parcellations. 
