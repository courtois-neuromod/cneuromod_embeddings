#!/usr/bin/python
import os
import argparse
import numpy as np
from dypac_utils import match_components


root_data = '/data/cisl/pbellec/cneuromod_embeddings/xp_202012/'


def save_matx(match_matx, path_results, fwhm, cluster, state):
    file_save = os.path.join(path_results, f'Rmatch_fwhm-{fwhm}_cluster-{cluster}_state-{state}.npy')
    print(file_save)
    np.save(file_save, match_matx)
    

def reproducibility(n_subject=7, fwhm=5, cluster=300, state=900):
    match_mtx = np.zeros([state, state, n_subject, n_subject])

    for ind_sub1 in range(1, n_subject):
        sub1 = f'sub-0{ind_sub1}'
        for ind_sub2 in range(ind_sub1, n_subject):
            sub2 = f'sub-0{ind_sub2}'
            print(f'matching parcels - {sub1} with {sub2}')
            R = match_components(sub1=sub1, sub2=sub2, root_data=root_data, fwhm=fwhm, cluster=cluster, state=state)
            match_mtx[:, :, ind_sub1-1, ind_sub2-1] = R
            match_mtx[:, :, ind_sub2-1, ind_sub1-1] = R
    return match_mtx


def main(args):
    match_mtx = reproducibility(n_subject=7, fwhm=args.fwhm, cluster=args.cluster, state=args.state)
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
