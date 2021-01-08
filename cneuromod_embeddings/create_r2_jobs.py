import os

cmds = []
model_paths = []

subjects = ["01","02","03","04","05","06"]
dataset = "data/cneuromod/friends"
bids_dir = "output/bids/friends_bids_cache"
tasks = "s01e"
group = "inter"
tag = "inter"
parcellations = ["dypac_clean"]#"difumo1024", "difumo512", "difumo256"]#"schaefer", "smith", "mist444", "mist197"]
out_dir = "output/s1_test_retest_clean_multi_fwhm"
fwhms = ["5"]
cluster = 20
states = 120

## Inter R2

for dir_ in os.listdir(out_dir):
    if "dataset" in dir_:# and "fwhm-"+fwhm in dir_:
        dirpath = os.path.join(out_dir, dir_)
        for file_ in os.listdir(dirpath):
            if ".pickle" in file_:
                model_paths.append(os.path.join(dirpath, file_))

for model_path in model_paths:
    sub = ""
    for s in subjects:
        if "sub-"+s not in model_path:
            sub = sub+s+","
    sub = sub[:-1]
    cmds.append("""python compute_r2.py -m {m} -d {d} -s {s} -t {t} -g {g} -tag {tag} -b {b}\n""".format(
        m=model_path, d=dataset, s=sub, t=tasks, g=group, tag=tag, b=bids_dir
        ))


## Other atlases

#for sub in subjects:
#    for fwhm in fwhms:
#        model_path = "output/dataset-friends_tasks-s01even_cluster-{}_states-{}_batches-1_reps-100_fwhm-{}/sub-{}_dataset-friends_tasks-s01even_cluster-{}_states-{}_batches-1_reps-100_fwhm-{}.pickle".format(cluster, states, fwhm, sub, cluster, states, fwhm)
#        for par in parcellations:
#            group = os.path.split(model_path)[1]
#            cmds.append("""python compute_r2.py -m {m} -d {d} -s {s} -t {t} -g {g} -a {a} -o {o} -b {b}\n""".format(
#                m=model_path, d=dataset, s=sub, t=tasks, g=group, a=par, o=out_dir,# p=par,
#                #tag="sub-"+sub+"_fwhm"+fwhm,
#                b=bids_dir
#                ))


with open("r2_jobs.sh", "w") as r2_job:
    for c in cmds:
        r2_job.write(c)

with open("r2_submit_jobs.sh", "r") as r2_sub:
    lines = r2_sub.readlines()

for i in range(len(lines)):
    if "#SBATCH --array=" in lines[i]:
        lines[i] = "#SBATCH --array=1-{}\n".format(len(cmds))

with open("r2_submit_jobs.sh", "w") as r2_sub:
    r2_sub.writelines(lines)
