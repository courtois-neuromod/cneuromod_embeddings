import os
import argparse
import time
from load_confounds import Params36
from dypac import Dypac
from bids import BIDSLayout
import h5py
import numpy as np
import pickle
import glob as glob
import warnings

warnings.filterwarnings("ignore")



def dypac_generate(
    func, conf, gm_path, n_clusters=10, n_states=5, n_batch=1, n_replications=40, fwhm=8
):
    print("Settings")
    print(
        "runs = %s, n_clusters = %s, n_states = %s, n_batches = %s, n_replcations = %s \n"
        % (len(func), n_clusters, n_states, n_batch, n_replications)
    )

    model = Dypac(
        n_clusters=n_clusters,
        n_states=n_states,
        subsample_size=80,
        grey_matter=gm_path,
        verbose=1,
        n_init=1,
        n_batch=n_batch,
        n_replications=n_replications,
        n_init_aggregation=1,
        detrend=False,
        smoothing_fwhm=fwhm,
        standardize=True,
    )
    print("the length of confounds list", len(conf))

    model.fit(func, confounds=conf)
    return model

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="Specify the base path.", default="data/cneuromod")
    parser.add_argument("-d", "--datasets", type=str, help="Specify the dataset.")
    parser.add_argument("-der", "--derivatives", type=str, help="Specify the derivatives.", default="fmriprep-20.1.0/fmriprep")
    parser.add_argument("--space", type=str, help="Specify the space of the bold files.", default="MNI152NLin2009cAsym")
    parser.add_argument("-s", "--subjects", type=str, help="Specify the subject.")
    parser.add_argument("-ses", "--sessions", type=str, help="Specify the session you want.", default="all")
    parser.add_argument("-t", "--tasks", type=str, help="Specify the task.", default="all")
    parser.add_argument("--val", type=str, help="Specify the task for validation r2.")
    parser.add_argument("-n_clusters", type=int, help="Specify the number of clusters.")
    parser.add_argument("-n_states", type=int, help="Specify the number of states.")
    parser.add_argument("-n_replications", type=int, help="Specify the number of replications.")
    parser.add_argument("-n_batch", type=int, help="Specify the number of batches.")
    parser.add_argument("-fwhm", type=int, help="Specify the smoothing fwhm.", default=8) 

    args = parser.parse_args()

    datasets = args.datasets.split(",")
    subjects = args.subjects.split(",")
    sessions = args.sessions.split(",")
    tasks = args.tasks.split(",")
    val_tasks = args.val.split(",")

    ###Print the parameters.

    print("\n\n\nDataset:{}\nDerivatives:{}\nSpace: {}\nSubjects:{}\nSessions:{}\nTasks:{}\nVal:{}\n".format(
        datasets, args.derivatives, args.space, subjects, sessions, tasks, val_tasks))

    sessions = "" if sessions == ["all"] else sessions
    tasks = "" if tasks == ["all"] else tasks
    subjects = "" if subjects == ["all"] else subjects
    
    ###Get the paths for the data
    tng_paths = []
    val_paths = []
    for dataset in datasets:
        dataset_path = os.path.join(args.path, dataset)
        derivatives_path = os.path.join(dataset_path, "derivatives", args.derivatives)
        layout = BIDSLayout(dataset_path, derivatives=derivatives_path)
        tng_paths = tng_paths + layout.get(subject=subjects, session=sessions, task=tasks, suffix="^bold$",
                space=args.space, extension="nii.gz", scope="derivatives", regex_search=True, return_type="file")
        val_paths = val_paths + layout.get(subject=subjects, session=sessions, task=val_tasks, suffix="^bold$",
                space=args.space, extension="nii.gz", scope="derivatives", regex_search=True, return_type="file")

    print("Using {} files:".format(len(tng_paths)))
    print("--------------TNG--------------")
    print(tng_paths)
    print("--------------VAL--------------")
    print(val_paths)

    conf = Params36().load(tng_paths)
    val_conf = Params36().load(val_paths)

    ##get the filename
    task_str = args.tasks
    if "e.[02468]" in task_str:
        task_str = task_str.replace("e.[02468]", "even")
    elif "e.[13579]" in task_str:
        task_str = task_str.replace("e.[13579]", "odd")
    out_dir_name = ("dataset-"+args.datasets+"_tasks-"+task_str+"_cluster-"+str(args.n_clusters)
        +"_states-"+str(args.n_states)+"_batches-"+str(args.n_batch)+"_reps-"
        +str(args.n_replications)+"_fwhm-"+str(args.fwhm))
    prefix = "sub-"+args.subjects+"_"+out_dir_name
    print(prefix)


    ##Get the path of the grey matter mask
    anat_path = os.path.join(args.path, "anat")
    anat_derivatives_path = os.path.join(anat_path, "derivatives", args.derivatives)
    anat_layout = BIDSLayout(anat_path, derivatives=anat_derivatives_path)
    gm_path = anat_layout.get(subject=subjects, space=args.space, label="GM", scope="derivatives", return_type="file")[0]
    print("gm_path = ", gm_path)

    ## TODO: use default value for grey_matter if mutliple subjects
    wt_start = time.time()
    pt_start = time.process_time()
    model = dypac_generate(
        tng_paths,
        conf,
        gm_path,
        n_clusters=args.n_clusters,
        n_states=args.n_states,
        n_batch=args.n_batch,
        n_replications=args.n_replications,
        fwhm=args.fwhm
    )
    process_time = time.process_time() - pt_start
    wall_time = time.time() - wt_start
    out_dir = os.path.join("output", out_dir_name)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out_path = os.path.join(out_dir, prefix + ".pickle")
    pickle.dump(model, open(out_path, "wb"))
    np.save(os.path.join(out_dir, prefix+"_time.npy"), np.array([wall_time, process_time]))

    ## produce R2 maps on training and validation data 
    h5_file = h5py.File(os.path.join(out_dir, prefix + "_r2_scores.hdf5"), "w")
    tng_grp = h5_file.create_group("training")
    val_grp = h5_file.create_group("validation")
    for i in range(len(tng_paths)):
        tng_r2 = model.score(tng_paths[i], confound=conf[i]).dataobj
        tng_dset = tng_grp.create_dataset(os.path.split(tng_paths[i])[1], data=tng_r2)
    for i in range(len(val_paths)):
        val_r2 = model.score(val_paths[i], confound=val_conf[i]).dataobj
        val_dset = val_grp.create_dataset(os.path.split(val_paths[i])[1], data=val_r2)
    h5_file.close()

    ## allow other people from rrg-pbellec group to access generated files
    os.system("setfacl -R -m g:rrg-pbellec:rwx {}".format(out_dir)) 

    print("We are done. Model saved at {}".format(out_path))
