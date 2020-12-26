#!/usr/bin/python
import os
import pickle
import argparse
import numpy as np
import pandas as pd
from cneuromod_embeddings import dypac_utils as du 


root_data = '/data/cisl/pbellec/cneuromod_embeddings/xp_202012/'


def visu_repro(root_data, xp, fwhm, cluster, state, n_subject=6):
    R = np.load(os.path.join(root_data, xp, f'Rmatch_fwhm-{fwhm}_cluster-{cluster}_state-{state}.npy'))
    width_fig = 20
    n_comp = n_subject
    fig = plt.figure(figsize=(width_fig, n_comp * 3))
    for sub1 in range(n_subject):
        for sub2 in range(n_subject):
            plt.subplot(6, 6, 1 + sub1 + sub2 * 6)
            match_val = np.max(R[:, :, sub1, sub2], axis=1)
            plt.hist(match_val, bins=100, density=True, stacked=True)
            plt.axis((-0.05, 1.05, 0, 15))
            ax = plt.gca()
            if sub2 == 0:
                ax.set_title(f"match with sub-0{sub1+1}")
            if sub1 != 0:
                ax.tick_params(labelleft=False)
            else:
                ax.set_ylabel(f"sub-0{sub2+1} distribution")
            if sub2 != 5:
                ax.tick_params(labelbottom=False)
            else:
                ax.set_xlabel("spatial correlation")


def R_models(model1, model2, mask_img):
    xn = normalize_components(model1, mask_img)
    xn = xn[:, model1.dwell_time_ > 0]
    yn = normalize_components(model2, mask_img)
    yn = yn[:, model2.dwell_time_ > 0]
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


def load_repro(root_data, fwhm, cluster, state):
    key = f'fwhm-{fwhm}_cluster-{cluster}_state-{state}'
    print(key)
    file_repro = os.path.join(root_data, f'Rmatch_{key}.p')
    R = pickle.load(open(file_repro, 'rb'))
    return R


def repro_df(root_data):
    val = np.array([])
    all_label = np.array([])
    all_fwhm = np.array([])
    all_sub = np.array([])
    type_comp = np.array([])
    params = du.dypac_params()
    list_subject = du.
    du.subject_keys(n_subject=6)
    for fwhm in params['fwhm']:
        for ind, cluster in enumerate(params['cluster']):
            state = params['state'][ind]
            R = load_repro(root_data, fwhm, cluster, state)
            for sub1 in list_subject:
                for sub2 in list_subject:
                    match_val = np.max(R[sub1][sub2], axis=1)
                    val = np.append(val, match_val)
                    label = f'cluster-{cluster}_state-{state}'
                    all_label = np.append(all_label, np.repeat(label, match_val.shape[0]))
                    all_fwhm = np.append(all_fwhm, np.repeat(fwhm, match_val.shape[0]))
                    all_sub = np.append(all_sub, np.repeat(sub1, match_val.shape[0]))
                    if sub1 == sub2:
                        type_comp = np.append(type_comp, np.repeat('intra', match_val.shape[0]))
                    else:
                        type_comp = np.append(type_comp, np.repeat('inter', match_val.shape[0]))
    return pd.DataFrame({'spatial_r': val, 'params': all_label, 'subject': all_sub, 'fwhm': all_fwhm, 'type_comp': type_comp})


def save_matx(match_matx, path_results, fwhm, cluster, state):
    file_save = os.path.join(path_results, f'Rmatch_fwhm-{fwhm}_cluster-{cluster}_state-{state}.p')
    print(file_save)
    pickle.dump(match_matx, open(file_save, 'wb'))


def reproducibility(n_subject=6, fwhm=5, cluster=300, state=900):
    list_subject = du.subject_keys(n_subject)
    match_mtx = dict.fromkeys(list_subject)
    for sub in list_subject:
        match_mtx[sub] = dict.fromkeys(list_subject)

    for ind_sub1 in range(n_subject):
        sub1 = list_subject[ind_sub1]
        for ind_sub2 in range(ind_sub1, n_subject):
            sub2 = list_subject[ind_sub2]
            print(f'matching parcels - {sub1} with {sub2}')
            R = match_components(sub1=sub1, sub2=sub2, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state)
            match_mtx[sub1][sub2] = R
            match_mtx[sub2][sub1] = R.transpose()
    return match_mtx


def main(args):
    match_mtx = reproducibility(n_subject=6, fwhm=args.fwhm, cluster=args.cluster, state=args.state)
    save_matx(match_mtx, args.path_results, args.fwhm, args.cluster, args.state)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_parcels', help='Full path to the parcels.')
    parser.add_argument('path_results', help='Path to store the results.')
    parser.add_argument('--fwhm', type=int, help='smoothing parameter.')
    parser.add_argument('--cluster', type=int, help='number of clusters.')
    parser.add_argument('--state', type=int, help='number of states.')
    args = parser.parse_args()
    main(args)
