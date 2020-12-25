#!/usr/bin/python
import os
import pickle
import argparse
import numpy as np
import pandas as pd
from cneuromod_embeddings.dypac_utils import dypac_params, subject_keys, key_params, match_components, subject_keys


root_data = '/data/cisl/pbellec/cneuromod_embeddings/xp_202012/'

def load_repro(root_data, fwhm, cluster, state):
    key = f'fwhm-{fwhm}_cluster-{cluster}_state-{state}'
    print(key)
    file_repro = os.path.join(root_data, f'Rmatch_{key}.p')
    R = pickle.load(open(file_repro, 'rb'))
    return R


def summary_repro(root_data):
    val = np.array([])
    all_label = np.array([])
    all_fwhm = np.array([])
    type_comp = np.array([])
    params = dypac_params()
    list_subject = subject_keys(n_subject=6)
    for fwhm in params['fwhm']:
        for ind, cluster in enumerate(params['cluster']):
            state = params['state'][ind]
            R = load_repro(root_data, fwhm, cluster, state)
            for sub1 in list_subject:
                for sub2 in list_subject:
                    match_val = np.max(R[sub1][sub2], axis=1
                    val = np.append(val, match_val)
                    label = f'cluster-{cluster}_state-{state}'
                    all_label = np.append(all_label, np.repeat(label, match_val.shape[0]))
                    all_fwhm = np.append(all_fwhm, np.repeat(fwhm, match_val.shape[0]))
                    if sub1 == sub2:
                        type_comp = np.append(type_comp, np.repeat('intra', match_val.shape[0]))
                    else:
                        type_comp = np.append(type_comp, np.repeat('inter', match_val.shape[0]))
    return pd.DataFrame({'spatial_r': val, 'params': all_label, 'fwhm': all_fwhm, 'type_comp': type_comp})


def save_matx(match_matx, path_results, fwhm, cluster, state):
    file_save = os.path.join(path_results, f'Rmatch_fwhm-{fwhm}_cluster-{cluster}_state-{state}.p')
    print(file_save)
    pickle.dump(match_matx, open(file_save, 'wb'))


def reproducibility(n_subject=6, fwhm=5, cluster=300, state=900):
    list_subject = subject_keys(n_subject)
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
