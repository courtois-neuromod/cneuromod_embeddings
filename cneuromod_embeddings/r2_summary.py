#!/usr/bin/python
import os
import pickle
import argparse
import numpy as np
import pandas as pd
from cneuromod_embeddings.dypac_utils import (
    subject_keys,
    load_dypac,
    load_r2_intra,
    load_r2_inter,
    load_r2_other,
    key_params,
)
from cneuromod_embeddings.cortical_segmentation import cortical_segmentation


def _save_r2(r2_df, path_results, atlas, fwhm, cluster, state):
    params = key_params(atlas, fwhm, cluster, state)
    file_save = os.path.join(path_results, f"r2_fwhm-{params}.p")
    print(file_save)
    r2_df.to_pickle(file_save)


def _load_mask(subject, root_data, type_mask, fwhm, cluster, state, xp_type):
    model, mask_img = load_dypac(
        subject=subject,
        root_data=root_data,
        fwhm=fwhm,
        cluster=cluster,
        state=state,
        xp_type=xp_type,
    )
    img = cortical_segmentation(mask_img)
    mask = (mask_img.get_fdata() > 0) & (img[type_mask].get_fdata() > 0)
    return mask


def _r2_inter(
    root_data,
    n_subject=6,
    fwhm=5,
    cluster=300,
    state=900,
    type_mask="cortex",
    xp_type="friends-s01",
):
    list_subject = subject_keys(n_subject)
    val = np.array([])
    all_label = np.array([])
    all_sub = np.array([])
    type_comp = np.array([])
    for sub in list_subject:
        print(sub)
        mask = _load_mask(
            subject=sub,
            root_data=root_data,
            type_mask=type_mask,
            fwhm=fwhm,
            cluster=cluster,
            state=state,
            xp_type=xp_type,
        )

        # inter-subject R2 maps
        hdf5_file = load_r2_inter(
            subject=sub,
            root_data=root_data,
            fwhm=fwhm,
            cluster=cluster,
            state=state,
            xp_type=xp_type,
        )
        list_sub2 = list(hdf5_file["inter"].keys())
        for sub2 in list_sub2:
            list_files2 = list(hdf5_file["inter"][sub2].keys())
            for file2 in list_files2:
                val = np.append(
                    val, np.mean(np.squeeze(hdf5_file["inter"][sub2][file2])[mask])
                )
                type_comp = np.append(type_comp, "inter")
                all_sub = np.append(all_sub, sub)
                all_label = np.append(all_label, f"cluster{cluster}_state{state}")
    return pd.DataFrame(
        data={"r2": val, "type": type_comp, "params": all_label, "subject": all_sub}
    )


def _r2_intra(
    root_data,
    n_subject=6,
    fwhm=5,
    cluster=300,
    state=900,
    type_mask="cortex",
    xp_type="friends-s01",
):
    list_subject = subject_keys(n_subject)
    val = np.array([])
    all_sub = np.array([])
    all_label = np.array([])
    type_comp = np.array([])
    for sub in list_subject:
        print(sub)
        mask = _load_mask(
            subject=sub,
            root_data=root_data,
            type_mask=type_mask,
            fwhm=fwhm,
            cluster=cluster,
            state=state,
            xp_type=xp_type,
        )

        # intra-subject R2 maps
        hdf5_file = load_r2_intra(
            subject=sub,
            root_data=root_data,
            fwhm=fwhm,
            cluster=cluster,
            state=state,
            xp_type=xp_type,
        )
        list_files = list(hdf5_file["validation"].keys())

        for file in list_files:
            val = np.append(
                val, np.mean(np.squeeze(hdf5_file["validation"][file])[mask])
            )
            type_comp = np.append(type_comp, "intra")
            all_sub = np.append(all_sub, sub)
            all_label = np.append(all_label, f"cluster{cluster}_state{state}")
    return pd.DataFrame(
        data={"r2": val, "type": type_comp, "params": all_label, "subject": all_sub}
    )


def _r2_other(
    root_data, atlas, n_subject=6, fwhm=5, type_mask="cortex", xp_type="friends-s01"
):
    list_subject = subject_keys(n_subject)
    params = dypac_params(xp_type)
    val = np.array([])
    all_sub = np.array([])
    all_label = np.array([])
    for sub in list_subject:
        print(sub)
        mask = _load_mask(
            subject=sub,
            root_data=root_data,
            type_mask=type_mask,
            fwhm=fwhm,
            cluster=params["cluster"][0],
            state=params["state"][0],
            xp_type=xp_type,
        )
        hdf5_file = load_r2_other(
            atlas=atlas, root_data=root_data, fwhm=fwhm, xp_type=xp_type
        )
        list_files = list(hdf5_file[sub].keys())
        for file in list_files:
            val = np.append(val, np.mean(np.squeeze(hdf5_file[sub][file])[mask]))
            all_sub = np.append(all_sub, sub)
            all_label = np.append(all_label, atlas)
    return pd.DataFrame(data={"r2": val, "params": all_label, "subject": all_sub})


def main(args):
    if args.atlas == "intra":
        val_r2 = _r2_intra(
            root_data=args.root_data,
            n_subject=6,
            fwhm=args.fwhm,
            cluster=args.cluster,
            state=args.state,
            type_mask=args.type_mask,
            xp_type=args.xp_type,
        )
        _save_r2(
            val_r2, args.path_results, args.atlas, args.fwhm, args.cluster, args.state
        )

    elif args.atlas == "inter":
        val_r2 = _r2_inter(
            root_data=args.root_data,
            n_subject=6,
            fwhm=args.fwhm,
            cluster=args.cluster,
            state=args.state,
            type_mask=args.type_mask,
            xp_type=args.xp_type,
        )
        _save_r2(
            val_r2, args.path_results, args.atlas, args.fwhm, args.cluster, args.state
        )

    else:
        val_r2 = _r2_other(
            root_data=args.root_data,
            atlas=args.atlas,
            n_subject=6,
            fwhm=args.fwhm,
            type_mask=args.type_mask,
            xp_type=args.xp_type,
        )
        _save_r2(
            val_r2, args.path_results, args.atlas, args.fwhm, args.cluster, args.state
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_data", help="Full path to the data.")
    parser.add_argument("path_results", help="Path to store the summary results.")
    parser.add_argument("--fwhm", type=int, help="smoothing parameter.")
    parser.add_argument(
        "--atlas",
        type=str,
        help="name of a parcellation atlas. Use intra for dypac within-subject, and inter for dypac between-subject",
    )
    parser.add_argument(
        "--type_mask",
        type=str,
        help="type of grey matter mask (cortex, central, cerebellum).",
    )
    parser.add_argument(
        "--xp_type",
        type=str,
        default="friends-s01",
        help="The type of experiment [friends-s01 (default), friends-s01_clean, friends-s01_clean_multi_fwhm].",
    )
    parser.add_argument("--cluster", type=int, default=0, help="number of clusters.")
    parser.add_argument("--state", type=int, default=0, help="number of states.")
    args = parser.parse_args()
    main(args)
