import h5py
from bids import BIDSLayout
import os
import numpy as np
import argparse
from load_confounds import Params36
import pickle
import dypac_masker
from nilearn import datasets


def compute_r2(model, file_paths, confounds, prefix, out_dir, tag=None,
               group_name=None): 

    if tag:
        if tag[0] != "_":
            tag = "_" + tag
    else:
        tag = ""
    out_path = os.path.join(out_dir, prefix + tag + "_r2_scores.hdf5")
    
    for i in range(len(file_paths)):
        r2 = model.score(file_paths[i], confound=confounds[i]).dataobj
        h5_file = h5py.File(out_path, "a")
        grp = h5_file
        if group_name:
            groups = group_name.split("/") 
            for group in groups:
                if group not in list(grp.keys()):
                    grp = grp.create_group(group)
                else:
                    grp = grp[group]
        dset = grp.create_dataset(os.path.split(file_paths[i])[1], data=r2)
        h5_file.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, help="Path to the dypac model.")
    parser.add_argument("-d", "--dataset", type=str, help="Path to the dataset.")
    parser.add_argument("-b", "--bids_folder", type=str,
            help="Path to the bids folder of the saved layout of the dataset.", default=None)
    parser.add_argument("-der", "--derivatives", type=str, help="Specify the derivatives",
            default="fmriprep-20.1.0/fmriprep")
    parser.add_argument("--space", type=str, help="Specify the space of the bold files.",
            default="MNI152NLin2009cAsym")
    parser.add_argument("-s", "--subjects", type=str, default="all",
            help="Specify the subjects. String with coma separated subjects (regex accepted), or 'all'.")
    parser.add_argument("-ses", "--sessions", type=str, defaul="all",
            help="Specify the sessions. String with coma separated sessions (regex accepted), or 'all'.")
    parser.add_argument("-t", "--tasks", type=str, default="all",
            help="Specify the task.i String with coma separated tasks (regex accepted), or 'all'.")
    parser.add_argument("-g", "--group", type=str, default=None,
            help="Specify the name for the hdf5 file group (no group if None).")
    parser.add_argument("-tag", type=str, default=None,
            help="Tag to append at the end of the output files names.")
    parser.add_argument("-p", "--prefix", type=str, default=None,
            help="Prefix to use for the output file name, if None the file name of the model is used.")
    parser.add_argument("-o", "--out_dir", type=str, default=None,
            help="Path to the directory where to save the results. If None, the directory of the model is used.")
    parser.add_argument("-a", "--atlas", type=str, help="Name of atlas.", default=None)

    args = parser.parse_args()

    subjects = args.subjects.split(",")
    sessions = args.sessions.split(",")
    tasks = args.tasks.split(",")

    subjects = "" if subjects == ["all"] else subjects
    sessions = "" if sessions == ["all"] else sessions
    tasks = "" if tasks == ["all"] else tasks

    prefix = args.prefix if args.prefix else os.path.splitext(os.path.split(args.model)[1])[0]
    out_dir = args.out_dir if args.out_dir else os.path.split(args.model)[0] 
    tag = "_" + args.tag if args.tag else ""

    derivatives_path = os.path.join(args.dataset, "derivatives", args.derivatives)
    layout = BIDSLayout(args.dataset, derivatives=derivatives_path, database_path=args.bids_folder)
    with open(args.model, "rb") as pickle_in:
        model = pickle.load(pickle_in)

    if args.atlas:
        if args.atlas == "schaefer":
            atlas_path = "data/schaefer_2018/Schaefer2018_400Parcels_7Networks_order_FSLMNI152_1mm.nii.gz"
            model = dypac_masker.LabelsMasker(model=model, labels=atlas_path)
        elif args.atlas == "smith":
            atlas_path = "data/smith_2009/rsn70.nii.gz"
            model = dypac_masker.MapsMasker(model=model, maps=atlas_path)
        elif "mist" in args.atlas:
            scale = args.atlas[4:]
            atlas_path = "data/MIST/Parcellations/MIST_{}.nii.gz".format(scale)
            model = dypac_masker.LabelsMasker(model=model, labels=atlas_path)
        elif "difumo" in args.atlas:
            scale = args.atlas[6:]
            atlas_path = "data/DIFUMO/DIFUMO_{}.nii.gz".format(scale)
            model = dypac_masker.MapsMasker(model=model, maps=atlas_path)
        elif args.atlas == "dypac_clean":
            components = np.array(model.components_.todense())
            components[components<0.1] = 0
            mask = list(np.sum(components, axis=1)>0)
            components = components[mask, :]
            maps = model.masker_.inverse_transform(components)
            model = dypac_masker.MapsMasker(model=model, maps=maps)
            tag = "_clean"
        elif args.atlas == "dypac_clean_multi_fwhm":
            model_fwhm_5 = model
            path_model_fwhm_8 = args.model.replace("fwhm-5", "fwhm-8")
            with open(path_model_fwhm_8, "rb") as pickle_in:
                model_fwhm_8 = pickle.load(pickle_in)
            components = np.array(model_fwhm_8.components_.todense())
            components[components<0.1] = 0
            mask = list(np.sum(components, axis=1)>0)
            components = components[mask, :]
            maps = model_fwhm_5.masker_.inverse_transform(components)
            model = dypac_masker.MapsMasker(model=model_fwhm_5, maps=maps)
            tag = "_clean_multi_fwhm"
        out_path_model = os.path.join(out_dir, prefix+tag+".pickle")
        pickle.dump(model, open(out_path_model, "wb"))

    for sub in subjects:
        file_paths = layout.get(subject=sub, session=sessions, task=tasks, suffix="^bold$", space=args.space,
                                extension="nii.gz", scope="derivatives", regex_search=True, return_type="file")
        confounds = Params36().load(file_paths)
        group = args.group+"/sub-"+sub if len(subjects) > 1 else args.group
        compute_r2(model, file_paths, confounds, prefix, out_dir, tag, group)
        print("done with", sub)

