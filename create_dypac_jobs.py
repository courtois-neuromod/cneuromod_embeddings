cmd = dict()
cmd["subject"] = ["05"]
cmd["dataset"] = ["friends"]
cmd["session"] = ["001"]
cmd["task"] = ["s01"]
cmd["clusters"] = ["5"]
cmd["states"] = ["5"]
cmd["batches"] = ["3"]
cmd["replication"] = ["1"]

cmds = []
for subject in cmd["subject"]:
    for dataset in cmd["dataset"]:
        for session in cmd["session"]:
            for task in cmd["task"]:
                for clusters in cmd["clusters"]:
                    for states in cmd["states"]:
                        for batches in cmd["batches"]:
                            for replications in cmd["replication"]:
                                cmds.append(
                                    """python generate_embeddings.py --subject={sub} --dataset={dat} --session={ses} --task={tas}  -n_clusters={cluster}  -n_states={state} -n_batch={batch} -n_replications={replication} \n""".format(
                                        sub=subject,
                                        dat=dataset,
                                        ses=session,
                                        tas=task,
                                        cluster=clusters,
                                        state=states,
                                        batch=batches,
                                        replication=replications
                                    )
                                )

with open("dypac_jobs.sh", "w") as dy_job:
    for c in cmds:
        dy_job.write(c)

with open("dypac_submit_jobs.sh", "r") as dy_sub:
    lines = dy_sub.readlines()

for i in range(len(lines)):
    if "#SBATCH --array=" in lines[i]:
        lines[i] = "#SBATCH --array=1-{}\n".format(len(cmds))

with open("dypac_submit_jobs.sh", "w") as dy_sub:
    dy_sub.writelines(lines)
