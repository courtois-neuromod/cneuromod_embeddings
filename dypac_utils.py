import os
import pickle as pk
import h5py

import numpy as np

from nibabel import nifti1

from sklearn.preprocessing import StandardScaler

from nilearn.image import mean_img
from nilearn.input_data import NiftiMasker
from nilearn.image import math_img


def normalize_components(model, mask_img):
    scaler = StandardScaler()
    x = model.components_.todense()
    img_parcels = model.masker_.inverse_transform(x)
    masker = NiftiMasker(standardize=False, detrend=False, mask_img=mask_img)
    xn = scaler.fit_transform(masker.fit_transform(img_parcels).transpose())
    return xn


def R_models(model1, model2, mask_img):
    xn = normalize_components(model1, mask_img)
    yn = normalize_components(model2, mask_img)
    R = np.matmul(xn.transpose(), yn) / yn.shape[0]
    return R


def match_components(sub1, sub2, root_data, fwhm, cluster, state):
    model, mask_img1 = load_dypac(
        subject=sub1,
        root_data=root_data,
        fwhm=fwhm,
        cluster=cluster,
        state=state,
        batch="even",
    )
    if sub2 == sub1:
        model2, mask_img2 = load_dypac(
            subject=sub2,
            root_data=root_data,
            fwhm=fwhm,
            cluster=cluster,
            state=state,
            batch="odd",
        )
    else:
        model2, mask_img2 = load_dypac(
            subject=sub2,
            root_data=root_data,
            fwhm=fwhm,
            cluster=cluster,
            state=state,
            batch="even",
        )
    mask_img = math_img(
        "img1 + img2 > 0", img1=model.masker_.mask_img, img2=model2.masker_.mask_img
    )
    return R_models(model, model2, mask_img)


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
