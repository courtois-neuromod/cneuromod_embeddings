#!/usr/bin/python
import os
import pickle
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from nilearn import plotting
from nilearn.image import math_img
from cneuromod_embeddings import dypac_utils as du


def visu_match(start, n_comp, model1, model2, order, match_pair, match_val):
    width_fig = 20
    fig = plt.figure(figsize=(width_fig, n_comp * 3))
    for num in range(n_comp):
        ind1 = order[num + start]
        ind2 = match_pair[order[num + start]]
        map1 = model1.masker_.inverse_transform(model1.components_[ind1, :])
        map2 = model2.masker_.inverse_transform(model2.components_[ind2, :])
        cut_coords = plotting.find_xyz_cut_coords(map1, activation_threshold=0.1)
        plotting.plot_stat_map(
            map1,
            display_mode="ortho",
            axes=plt.subplot(n_comp, 2, 2 * num + 1),
            threshold=0.1,
            vmax=1,
            colorbar=False,
            draw_cross=False,
            title=f"test",
            cmap="bwr",
            cut_coords=cut_coords,
        )
        plotting.plot_stat_map(
            map2,
            display_mode="ortho",
            axes=plt.subplot(n_comp, 2, 2 * (num + 1)),
            threshold=0.1,
            vmax=1,
            colorbar=False,
            draw_cross=False,
            title=f"retest (match {match_val[ind1]:0.2f})",
            cmap="bwr",
            cut_coords=cut_coords,
        )


def R_models(model1, model2, mask_img):
    xn = du.normalize_components(model1, mask_img)
    yn = du.normalize_components(model2, mask_img)
    R = np.matmul(xn.transpose(), yn) / yn.shape[0]
    return R


def match_components(sub1, sub2, root_data, fwhm, cluster, state, xp_type):
    model1, mask_img1 = du.load_dypac(
        subject=sub1,
        root_data=root_data,
        fwhm=fwhm,
        cluster=cluster,
        state=state,
        batch="training",
        xp_type=xp_type
    )
    if sub2 == sub1:
        batch = "test"
    else:
        batch = "training"
    model2, mask_img2 = du.load_dypac(
        subject=sub2,
        root_data=root_data,
        fwhm=fwhm,
        cluster=cluster,
        state=state,
        batch=batch,
        xp_type=xp_type
    )
    mask_img = math_img(
        "img1 + img2 > 0", img1=model1.masker_.mask_img, img2=model2.masker_.mask_img
    )
    return R_models(model1, model2, mask_img)


def load_repro(root_data, fwhm, cluster, state):
    key = f"fwhm-{fwhm}_cluster-{cluster}_state-{state}"
    file_repro = os.path.join(root_data, f"Rmatch_{key}.p")
    R = pickle.load(open(file_repro, "rb"))
    return R


def repro_df(root_data, xp_type="friends-s01"):
    val = np.array([])
    all_label = np.array([])
    all_fwhm = np.array([])
    all_sub = np.array([])
    type_comp = np.array([])
    params = du.dypac_params(xp_type)
    list_subject = du.subject_keys(n_subject=6)
    for fwhm in params["fwhm"]:
        for ind, cluster in enumerate(params["cluster"]):
            state = params["state"][ind]
            R = load_repro(root_data, fwhm, cluster, state)
            for sub1 in list_subject:
                for sub2 in list_subject:
                    match_val = np.max(R[sub1][sub2], axis=1)
                    val = np.append(val, match_val)
                    label = f"cluster-{cluster}_state-{state}"
                    all_label = np.append(
                        all_label, np.repeat(label, match_val.shape[0])
                    )
                    all_fwhm = np.append(all_fwhm, np.repeat(fwhm, match_val.shape[0]))
                    all_sub = np.append(all_sub, np.repeat(sub1, match_val.shape[0]))
                    if sub1 == sub2:
                        type_comp = np.append(
                            type_comp, np.repeat("intra", match_val.shape[0])
                        )
                    else:
                        type_comp = np.append(
                            type_comp, np.repeat("inter", match_val.shape[0])
                        )
    return pd.DataFrame(
        {
            "spatial_r": val,
            "params": all_label,
            "subject": all_sub,
            "fwhm": all_fwhm,
            "type_comp": type_comp,
        }
    )


def save_matx(match_matx, path_results, fwhm, cluster, state):
    file_save = os.path.join(
        path_results, f"Rmatch_fwhm-{fwhm}_cluster-{cluster}_state-{state}.p"
    )
    print(file_save)
    pickle.dump(match_matx, open(file_save, "wb"))


def reproducibility(root_data, n_subject=6, fwhm=5, cluster=300, state=900, xp_type='friends-s01'):
    list_subject = du.subject_keys(n_subject)
    match_mtx = dict.fromkeys(list_subject)
    for sub in list_subject:
        match_mtx[sub] = dict.fromkeys(list_subject)

    for ind_sub1 in range(n_subject):
        sub1 = list_subject[ind_sub1]
        for ind_sub2 in range(ind_sub1, n_subject):
            sub2 = list_subject[ind_sub2]
            print(f"matching parcels - {sub1} with {sub2}")
            R = match_components(
                sub1=sub1,
                sub2=sub2,
                root_data=root_data,
                fwhm=fwhm,
                cluster=cluster,
                state=state,
                xp_type=xp_type
            )
            match_mtx[sub1][sub2] = R
            match_mtx[sub2][sub1] = R.transpose()
    return match_mtx


def main(args):
    match_mtx = reproducibility(
        root_data=args.path_parcels, n_subject=6, fwhm=args.fwhm, cluster=args.cluster, state=args.state, xp_type=args.xp_type
    )
    save_matx(match_mtx, args.path_results, args.fwhm, args.cluster, args.state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_parcels", help="Full path to the parcels.")
    parser.add_argument("path_results", help="Path to store the results.")
    parser.add_argument("--xp_type", help="The type of experiment [friends-s01 (default), friends-s01_clean, friends-s01_clean_multi_fwhm].")
    parser.add_argument("--fwhm", type=int, help="smoothing parameter.")
    parser.add_argument("--cluster", type=int, help="number of clusters.")
    parser.add_argument("--state", type=int, help="number of states.")
    args = parser.parse_args()
    main(args)
