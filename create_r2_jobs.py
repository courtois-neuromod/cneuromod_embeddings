import os

cmds = []
model_paths = []

for dir_ in os.listdir("output"):
    if "even" in dir_ or "odd" in dir_:
        dirpath = os.path.join("output", dir_)
        for file_ in os.listdir(dirpath):
            if ".pickle" in file_:
                model_paths.append(os.path.join(dirpath, file_))

subjects = ["01","02","03","04","05","06"]
dataset = "data/cneuromod/friends"
tasks = "s01e"
group = "inter"
tag = "inter"

for model_path in model_paths:
    sub = ""
    for s in subjects:
        if "sub-"+s not in model_path:
            sub = sub+s+","
    sub = sub[:-1]
    cmds.append("""python compute_r2.py -m {m} -d {d} -s {s} -t {t} -g {g} -tag {tag} \n""".format(
        m=model_path, d=dataset, s=sub, t=tasks, g=group, tag=tag
        ))

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
