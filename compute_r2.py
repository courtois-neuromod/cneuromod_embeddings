import h5py
from bids import BIDSLayout
import os
import argparse
from load_confounds import Params36
import pickle

def compute_r2(model_path, file_paths, confounds, prefix=None, tag=None, out_dir=None,
               group_name=None, derivatives="fmriprep-20.1.0/fmriprep", space="MNI152NLin2009cAsym"): 

    prefix = prefix if prefix else os.path.splitext(os.path.split(model_path)[1])[0]
    out_dir = out_dir if out_dir else os.path.split(model_path)[0] 
    tag = "_" + tag if tag else ""
    out_path = os.path.join(out_dir, prefix + tag + "_r2_scores.hdf5")
    with open(model_path, "rb") as pickle_in:
        model = pickle.load(pickle_in)

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
#    os.system("setfacl -m g:rrg-pbellec:rwx {}".format(out_path))


if __name__ == "__main__":

    print("hello")
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, help="Path to the dypac model.")
    parser.add_argument("-d", "--dataset", type=str, help="Path to the dataset.")
    parser.add_argument("-der", "--derivatives", type=str, help="Specify the derivatives", default="fmriprep-20.1.0/fmriprep")
    parser.add_argument("--space", type=str, help="Specify the space of the bold files.", default="MNI152NLin2009cAsym")
    parser.add_argument("-s", "--subjects", type=str, help="Specify the subject.", default="all")
    parser.add_argument("-ses", "--sessions", type=str, help="Specify the session you want.", default="all")
    parser.add_argument("-t", "--tasks", type=str, help="Specify the task.", default="all")
    parser.add_argument("-g", "--group", type=str, help="Specify the name for the hdf5 file group (no group if the name is None).", default=None)
    parser.add_argument("-tag", type=str, help="Tag to append at the end of the file name.", default=None)
    parser.add_argument("-p", "--prefix", type=str,
            help="Prefix to use for the output file name, if None the file name of the model is used.", default=None)
    parser.add_argument("-o", "--out_dir", type=str,
            help="Path to the directory where to save the results. If None, the directory of the model is used.", default=None)

    args = parser.parse_args()

    subjects = args.subjects.split(",")
    sessions = args.sessions.split(",")
    tasks = args.tasks.split(",")

    subjects = "" if subjects == ["all"] else subjects
    sessions = "" if sessions == ["all"] else sessions
    tasks = "" if tasks == ["all"] else tasks

    derivatives_path = os.path.join(args.dataset, "derivatives", args.derivatives)
    layout = BIDSLayout(args.dataset, derivatives=derivatives_path)

    if len(subjects) > 1:
        for sub in subjects:
            file_paths = layout.get(subject=sub, session=sessions, task=tasks, suffix="^bold$", space=args.space,
                                    extension="nii.gz", scope="derivatives", regex_search=True, return_type="file")
            confounds = Params36().load(file_paths)
            compute_r2(args.model, file_paths, confounds, args.prefix,
                       args.tag, args.out_dir, args.group+"/sub-"+sub, args.derivatives, args.space)
            print("done with", sub)
    else:
        file_paths = layout.get(subject=subjects, session=sessions, task=tasks, suffix="^bold$", space=args.space,
                                extension="nii.gz", scope="derivatives", regex_search=True, return_type="file")
        confounds = Params36().load(file_paths)
        compute_r2(args.model, args.dataset, subjects, sessions, tasks, args.prefix,
                   args.tag, args.out_dir, args.group, args.derivatives, args.space)
