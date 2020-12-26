import os
import pickle as pk
import h5py

import numpy as np
import matplotlib.pyplot as plt

from nibabel import nifti1

from sklearn.preprocessing import StandardScaler

from nilearn.image import mean_img
from nilearn.input_data import NiftiMasker
from nilearn.image import math_img

def get_root_data(xp_name):
    root_path, basename = os.path.split(__file__)
    root_data = os.path.join(root_path, xp_name)
    return root_data


def dypac_params():
    params = dict.fromkeys(['fwhm', 'cluster', 'state'])
    params['fwhm'] = (5, 8)
    params['cluster'] = (20, 20, 50, 50, 300)
    params['state'] = (60, 120, 150, 300, 900)
    return params


def key_params(atlas, fwhm, cluster, state):
    if (atlas=='intra') | (atlas=='inter'):
        params = f'{atlas}_fwhm-{fwhm}_cluster-{cluster}_state-{state}'
    else:
        params = f'{atlas}_fwhm-{fwhm}'
    return params


def subject_keys(n_subject):
    list_subject = []
    for ind in range(1, n_subject+1):
        list_subject.append(f'sub-0{ind}')
    return list_subject


def normalize_components(model, mask_img):
    scaler = StandardScaler()
    x = model.components_.todense()
    img_parcels = model.masker_.inverse_transform(x)
    masker = NiftiMasker(standardize=False, detrend=False, mask_img=mask_img)
    xn = scaler.fit_transform(masker.fit_transform(img_parcels).transpose())
    return xn


def load_model(pickle_in):
    model = pk.load(pickle_in)
    pickle_in.close()
    mask_img = model.mask_img_
    return model, mask_img


def load_dypac(subject, root_data, fwhm=5, cluster=50, state=150, batch="even"):
    """Load a dypac model."""
    path_data = os.path.join(
        root_data,
        f"dataset-friends_tasks-s01{batch}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}",
    )
    file_model = os.path.join(
        path_data,
        f"{subject}_dataset-friends_tasks-s01{batch}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}.pickle",
    )
    pickle_in = open(file_model, "rb")
    model, mask_img = load_model(pickle_in)
    return model, mask_img


def load_r2_intra(subject, root_data, fwhm=5, cluster=50, state=150):
    """Load a stack of r2 maps."""
    path_data = os.path.join(
        root_data,
        f"dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}",
    )
    file_score = os.path.join(
        path_data,
        f"{subject}_dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}_r2_scores.hdf5",
    )
    hdf5_file = h5py.File(file_score, "r")
    return hdf5_file


def load_r2_inter(subject, root_data, fwhm, cluster=50, state=150):
    """Load a stack of r2 maps."""
    path_data = os.path.join(
        root_data,
        f"dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}",
    )
    file_score = os.path.join(
        path_data,
        f"{subject}_dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}_inter_r2_scores.hdf5",
    )
    hdf5_file = h5py.File(file_score, "r")
    return hdf5_file


def load_r2_other(atlas, root_data, fwhm):
    """Load a stack of r2 maps with other atlases."""
    path_data = os.path.join(root_data, "other_atlases")
    file_score = os.path.join(path_data, f"{atlas}_fwhm-{fwhm}_r2_score.hdf5")
    hdf5_file = h5py.File(file_score, "r")
    return hdf5_file


def mean_r2(hdf5_file, ref_img):
    vols = []
    list_files = hdf5_file.keys()
    for file in list_files:
        vols.append(nifti1.Nifti1Image(hdf5_file[file], ref_img.affine))
    return mean_img(vols)


def mean_inter_r2(hdf5_file, ref_img):
    vols = []
    for subject in hdf5_file.keys():
        list_files = hdf5_file[subject]
        for file in list_files:
            vols.append(nifti1.Nifti1Image(hdf5_file[subject][file], ref_img.affine))
    return mean_img(vols)
