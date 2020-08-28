import argparse
from load_confounds import Params24
from dypac import Dypac
import pickle
import glob as glob
import warnings

warnings.filterwarnings("ignore")


from fetch_cneuromod import fetch_cneuromod


def dypac_generate(
    func, prefix, gm_path, n_clusters=10, n_states=5, n_batch=1, n_replications=40
):
    print("Settings")
    print(
        "runs = %s, n_clusters = %s, n_states = %s, n_batches = %s, n_replcations = %s \n"
        % (len(func), n_clusters, n_states, n_batch, n_replications)
    )
    conf = Params24().load(func)

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
        smoothing_fwhm=8,
        standardize=True,
    )
    print("the length of confounds list", len(conf))

    model.fit(func, confounds=conf)

    if len(func) < 30:
        path = "output/second_run/" + prefix + ".pickle"

    else:
        path = "output/" + prefix + ".pickle"

    pickle.dump(model, open(path, "wb"))

    print(path)
    print("We are done.")

    return 0


def get_prefix(files, clusters, states, batches, replications):

    prefix = (
        prefix
        + "_cluster"
        + str(clusters)
        + "_states"
        + str(states)
        + "_batches"
        + str(batches)
        + "_reps"
        + str(replications)
    )

    return prefix


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", type=str, help="Specify the base path.")

    parser.add_argument("-s", "--subject", type=str, help="Specify the subject.")

    parser.add_argument(
        "-ses", "--session", type=str, help="Specify the session you want."
    )
    parser.add_argument("-r", "--runs", type=str, help="Specify the run.")

    parser.add_argument("-n_clusters", type=int, help="Specify the number of clusters.")

    parser.add_argument("-n_states", type=int, help="Specify the number of states.")

    parser.add_argument(
        "-n_replications", type=int, help="Specify the number of replications."
    )

    parser.add_argument("-n_batch", type=int, help="Specify the number of batches.")

    args = parser.parse_args()

    base_path = "/project/rrg-pbellec/datasets/cneuromod_new/movie10/derivatives/fmriprep-20.1.0/fmriprep/"

    subject = args.subject.split(",")

    ###Print the parameters.

    print("\n\n\nSubject: ", subject)
    session = args.session.split(",")
    print("Session: ", session)
    run = args.runs.split(",")
    print("Run: ", run)
    task = "bournesupremacy"
    print("Task:", task)
    print("\n")


###Get the paths for the data
func = fetch_cneuromod(subjects=subject,sessions=["all"], segments=["all"], runs=["run-1"],images=["bold"],datasets=["movie10"],tasks=["all"],list_out=True)["movie10"]

func = func[0:10]


##get the filename
prefix = (
    args.subject
    + "_runs"
    + str(len(func))
    + "_cluster"
    + str(args.n_clusters)
    + "_states"
    + str(args.n_states)
    + "_batches"
    + str(args.n_batch)
    + "_reps"
    + str(args.n_replications)
)
print(prefix)


##Get the path of the grey matter mask
gm_path = (
    base_path
    + subject[0]
    + "/anat/"
    + subject[0]
    + "_space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz"
)

print("gm_path = ", gm_path)


dypac_generate(
    func,
    prefix,
    gm_path,
    n_clusters=args.n_clusters,
    n_states=args.n_states,
    n_batch=args.n_batch,
    n_replications=args.n_replications,
)
