#!/usr/bin/python
import os
import pickle
import argparse
import numpy as np
import pandas as pd
from dypac_utils import subject_keys, load_dypac, load_r2_intra, load_r2_inter, load_r2_other
from cortical_segmentation import cortical_segmentation


def _save_r2_df(r2_df, path_results, fwhm, cluster, state):
    file_save = os.path.join(
        path_results, f"r2_fwhm-{fwhm}_cluster-{cluster}_state-{state}.p"
    )
    print(file_save)
    r2_df.to_pickl.(file_save)


def _load_mask(subject, root_data, type_mask, fwhm, cluster, state):
    model, mask_img = load_dypac(
        subject=subject, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state
    )
    img = cortical_segmentation(mask_img)
    mask = (mask_img.get_fdata() > 0) & (img[type_mask].get_fdata() > 0)
    return mask


def _r2_inter(root_data, n_subject=6, fwhm=5, cluster=300, state=900, type_mask='cortex'):
    list_subject = subject_keys(n_subject)
    val = np.array([])
    all_label = np.array([])
    type_comp = np.array([])
    for sub in list_subject:
        print(sub)
        mask = _load_mask(subject=sub, root_data=root_data,type_mask=type_mask, fwhm=fwhm, cluster=cluster, state=state)

        # inter-subject R2 maps
        hdf5_file = load_r2_inter(subject=sub, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state)
        list_sub2 = list(hdf5_file['inter'].keys())
        for sub2 in list_sub2:
            list_files2 = list(hdf5_file['inter'][sub2].keys())
            for file2 in list_files2:
                val = np.append(val, np.mean(np.squeeze(hdf5_file['inter'][sub2][file2])[mask[type_mask]]))
                type_comp = np.append(type_comp, 'inter')
                all_label = np.append(all_label, f'cluster{cluster}_state{state}')
    return pd.DataFrame("r2": val, "type": type_comp, "params": all_label)


def _r2_intra(root_data, n_subject=6, fwhm=5, cluster=300, state=900, type_mask='cortex'):
    list_subject = subject_keys(n_subject)
    val = np.array([])
    all_label = np.array([])
    type_comp = np.array([])
    for sub in list_subject:
        print(sub)
        mask = _load_mask(subject=sub, root_data=root_data,type_mask=type_mask, fwhm=fwhm, cluster=cluster, state=state)

        # intra-subject R2 maps
        hdf5_file = load_r2_intra(subject=sub, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state)
        list_files = list(hdf5_file['validation'].keys())

        for file in list_files:
            val = np.append(val, np.mean(np.squeeze(hdf5_file['validation'][file])[mask[type_mask]]))
            type_comp = np.append(type_comp, 'intra')
            all_label = np.append(all_label, f'cluster{cluster}_state{state}')
    return pd.DataFrame("r2": val, "type": type_comp, "params": all_label)


def _r2_other(root_data, atlas, n_subject=6, fwhm=5, type_mask='cortex'):
    list_subject = subject_keys(n_subject)
    val = np.array([])
    all_label = np.array([])
    for sub in list_subject:
        print(sub)
        mask = _load_mask(subject=sub, root_data=root_data,type_mask=type_mask, fwhm=fwhm, cluster=20, state=60)
        hdf5_file = load_r2_other(atlas=atlas, root_data=root_data, fwhm=fwhm)
        list_files = list(hdf5_file[sub].keys())
        for file in list_files:
            val = np.append(val, np.mean(np.squeeze(hdf5_file[sub][file])[mask]))
            all_label = np.append(all_label, atlas)
    return pd.DataFrame("r2": val, "params": all_label)


def main(args):
    val_intra = _r2_intra(
        root_data=args.path_r2,
        n_subject=6,
        fwhm=args.fwhm,
        cluster=args.cluster,
        state=args.state,
    )
    save_matx(r2_mtx, args.path_results, args.fwhm, args.cluster, args.state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_data", help="Full path to the data.")
    parser.add_argument("path_results", help="Path to store the summary results.")
    parser.add_argument("--fwhm", type=int, help="smoothing parameter.")
    parser.add_argument("--template", type=str, help="name of a parcellation template.")
    parser.add_argument("--cluster", type=int, help="number of clusters.")
    parser.add_argument("--state", type=int, help="number of states.")
    args = parser.parse_args()
    main(args)
