import os
import pickle as pk
import h5py

import numpy as np
import matplotlib.pyplot as plt

from nibabel import nifti1

from sklearn.preprocessing import StandardScaler

from nilearn.image import mean_img
from nilearn.input_data import NiftiMasker


def get_root_data(xp_name):
    root_path, basename = os.path.split(__file__)
    root_data = os.path.join(root_path, xp_name)
    return root_data


def dypac_params(xp_type="friends-s01"):
    if xp_type == "friends-s01":
        params = dict.fromkeys(["fwhm", "cluster", "state"])
        params["fwhm"] = (5, 8)
        params["cluster"] = (20, 20, 50, 50, 300)
        params["state"] = (60, 120, 150, 300, 900)
    else:
        params = dict.fromkeys(["fwhm", "cluster", "state"])
        params["fwhm"] = [5]
        params["cluster"] = (64, 64, 256)
        params["state"] = (256, 512, 1024)
    return params


def atlas_params(xp_type):
    params_d = dypac_params(xp_type)
    params = {}
    params['dypac'] = []
    for num, state in enumerate(params_d['state']):
        cluster = params_d['cluster'][num]
        params['dypac'].append(f"cluster-{cluster}_state-{state}")
    params['other'] = ['difumo256', 'difumo512', 'difumo1024', 'mist197', 'mist444', 'schaefer', 'smith']
    return params


def key_params(atlas, fwhm, cluster, state):
    if (atlas == "intra") | (atlas == "inter") | (atlas=="training"):
        params = f"{atlas}_fwhm-{fwhm}_cluster-{cluster}_state-{state}"
    else:
        params = f"{atlas}_fwhm-{fwhm}"
    return params


def subject_keys(n_subject):
    list_subject = []
    for ind in range(1, n_subject + 1):
        list_subject.append(f"sub-0{ind}")
    return list_subject


def normalize_components(model, mask_img):
    scaler = StandardScaler()
    x = model.components_
    img_parcels = model.masker_.inverse_transform(x)
    masker = NiftiMasker(standardize=False, detrend=False, mask_img=mask_img)
    xn = scaler.fit_transform(masker.fit_transform(img_parcels).transpose())
    return xn


def load_model(pickle_in):
    model = pk.load(pickle_in)
    pickle_in.close()
    mask_img = model.masker_.mask_img_
    # if the model is generated directly by dypac, it is a sparce scipy array
    # otherwise it is a ndarray
    if not isinstance(model.components_, np.ndarray):
        model.components_ = model.components_.todense()
    else:
        model.components_ = model.components_.transpose()

    return model, mask_img


def _get_suffix(xp_type, batch="training", output_type="model"):
    if xp_type == "friends-s01_clean":
        if output_type == "r2_other":
            suffix = "score"
        else:
            suffix = "_clean"
        if batch == "training":
            data = "friends"
            task = "s01even"
        else:
            data = "friends"
            task = "s01odd"
    elif xp_type == "friends-s01_clean_multi_fwhm":
        if output_type == "r2_other":
            suffix = "score"
        else:
            suffix = "_clean_multi_fwhm"
        if batch == "training":
            data = "friends"
            task = "s01even"
        else:
            data = "friends"
            task = "s01odd"
    elif xp_type == "friends-s02":
        if batch == "training":
            data = "friends"
            task = "s01"
        else:
            data = "friends"
            task = "s02"
        if output_type == "model":
            suffix = "_clean_multi_fwhm"
        elif output_type == "r2_other":
            suffix = "scores"
        else:
            suffix = ""
    elif xp_type == "movie10":
        if batch == "training":
            data = "friends"
            task = "s01"
        else:
            data = "movie10"
            task = "all"
        if output_type == "model":
            suffix = "_clean_multi_fwhm"
        elif output_type == "r2_other":
            suffix = "scores"
        else:
            suffix = ""
    elif xp_type == "hcptrt":
        if batch == "training":
            data = "friends"
            task = "s01"
        else:
            data = "hcptrt"
            task = "all"
        if output_type == "model":
            suffix = "_clean_multi_fwhm"
        elif output_type == "r2_other":
            suffix = "scores"
        else:
            suffix = ""
    else:
        data = "friends"
        task = f"s01{batch}"
        suffix = ""
    return suffix, task, data


def load_dypac(
    subject,
    root_data,
    fwhm=5,
    cluster=50,
    state=150,
    batch="training",
    xp_type="friends-s01",
):
    """Load a dypac model."""
    suffix, task, data = _get_suffix(xp_type, batch=batch, output_type="model")
    path_data = os.path.join(
        root_data,
        f"dataset-{data}_tasks-{task}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}",
    )
    file_model = os.path.join(
        path_data,
        f"{subject}_dataset-{data}_tasks-{task}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}{suffix}.pickle",
    )
    pickle_in = open(file_model, "rb")
    model, mask_img = load_model(pickle_in)
    # in early iterations of the project, models were generated by dypac and included empty states
    # the two next lines eliminates those states
    # in latter iterations, "clean" models were prepared and generated with dypac_masker
    if hasattr(model, "dwell_time_"):
        model.components_ = model.components_[model.dwell_time_ > 0, :]
    return model, mask_img


def load_r2_intra(
    subject, root_data, fwhm=5, cluster=50, state=150, xp_type="friends-s01"
):
    """Load a stack of r2 maps."""
    suffix, task, data = _get_suffix(xp_type, batch="training", output_type="r2_intra")
    path_data = os.path.join(
        root_data,
        f"dataset-{data}_tasks-{task}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}",
    )
    file_score = os.path.join(
        path_data,
        f"{subject}_dataset-{data}_tasks-{task}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}{suffix}_r2_scores.hdf5",
    )
    hdf5_file = h5py.File(file_score, "r")
    return hdf5_file


def load_r2_inter(
    subject, root_data, fwhm, cluster=50, state=150, xp_type="friends-s01"
):
    """Load a stack of r2 maps."""
    suffix, task, data = _get_suffix(xp_type, batch="training", output_type="r2_inter")
    path_data = os.path.join(
        root_data,
        f"dataset-{data}_tasks-{task}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}",
    )
    file_score = os.path.join(
        path_data,
        f"{subject}_dataset-{data}_tasks-{task}_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}{suffix}_inter_r2_scores.hdf5",
    )
    hdf5_file = h5py.File(file_score, "r")
    return hdf5_file


def load_r2_other(atlas, root_data, fwhm, xp_type="friends-s01"):
    """Load a stack of r2 maps with other atlases."""
    path_data = os.path.join(root_data, "other_atlases")
    suffix, task, data = _get_suffix(xp_type, batch="training", output_type="r2_other")
    file_score = os.path.join(path_data, f"{atlas}_fwhm-{fwhm}_r2_{suffix}.hdf5")
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
