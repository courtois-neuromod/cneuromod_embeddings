import os
import pickle as pk
import h5py
from nibabel import nifti1
from nilearn.image import mean_img


def load_model(pickle_in):
   model = pk.load(pickle_in)
   pickle_in.close()
   mask_img = model.mask_img_
   return model, mask_img


def load_dypac(subject, root_data, fwhm, cluster=50, state=150):
   """Load a dypac model."""
   path_data = os.path.join(root_data, f'dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}')
   file_model = os.path.join(path_data, f'{subject}_dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}.pickle')
   pickle_in = open(file_model, "rb")
   model, mask_img = load_model(pickle_in)
   return model, mask_img


def load_r2_intra(subject, root_data, fwhm, cluster=50, state=150):
    """Load a stack of r2 maps."""
    path_data = os.path.join(root_data, f'dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}')
    file_score = os.path.join(path_data, f'{subject}_dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}_r2_scores.hdf5')
    hdf5_file = h5py.File(file_score, 'r')
    return hdf5_file

def load_r2_inter(subject, root_data, fwhm, cluster=50, state=150):
    """Load a stack of r2 maps."""
    path_data = os.path.join(root_data, f'dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}')
    file_score = os.path.join(path_data, f'{subject}_dataset-friends_tasks-s01even_cluster-{cluster}_states-{state}_batches-1_reps-100_fwhm-{fwhm}_inter_r2_scores.hdf5')
    hdf5_file = h5py.File(file_score, 'r')
    return hdf5_file

def load_r2_other(atlas, root_data, fwhm):
    """Load a stack of r2 maps with other atlases."""
    path_data = os.path.join(root_data, 'other_atlases')
    file_score = os.path.join(path_data, f'{atlas}_fwhm-{fwhm}_r2_score.hdf5')
    hdf5_file = h5py.File(file_score, 'r')
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

