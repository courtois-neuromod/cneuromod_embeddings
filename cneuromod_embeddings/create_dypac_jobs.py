cmd = dict()
cmd["subject"] = ["01","02","03","04","05","06"]
cmd["dataset"] = ["friends"]
cmd["session"] = ["all"]
cmd["task"] = ["s01e.[02468]","s01e.[13579]"]
cmd["val_task"] = ["s01e.[13579]","s01e.[02468]"]
cmd["clusters"] = ["50"]
cmd["states"] = ["150", "300"]
cmd["batches"] = ["1"]
cmd["replication"] = ["100"]
cmd["fwhm"] = ["5","8"]

num = "_2"

cmds = []
for subject in cmd["subject"]:
    for dataset in cmd["dataset"]:
        for session in cmd["session"]:
            for i_task in range(len(cmd["task"])):
                for clusters in cmd["clusters"]:
                    for states in cmd["states"]:
                        for batches in cmd["batches"]:
                            for replications in cmd["replication"]:
                                for fwhm in cmd["fwhm"]:
                                    cmds.append(
                                        """python cneuromod_embeddings/generate_embeddings.py --subject={sub} --dataset={dat} --session={ses} --task={tas} --val={val} -n_clusters={cluster} -n_states={state} -n_batch={batch} -n_replications={replication} -fwhm={fwhm} \n""".format(
                                            sub=subject,
                                            dat=dataset,
                                            ses=session,
                                            tas=cmd["task"][i_task],
                                            val=cmd["val_task"][i_task],
                                            cluster=clusters,
                                            state=states,
                                            batch=batches,
                                            replication=replications,
                                            fwhm=fwhm
                                        )
                                    )

with open("cneuromod_embeddings/dypac_jobs{}.sh".format(num), "w") as dy_job:
    for c in cmds:
        dy_job.write(c)

with open("cneuromod_embeddings/dypac_submit_jobs{}.sh".format(num), "r") as dy_sub:
    lines = dy_sub.readlines()

for i in range(len(lines)):
    if "#SBATCH --array=" in lines[i]:
        lines[i] = "#SBATCH --array=1-{}\n".format(len(cmds))

with open("cneuromod_embeddings/dypac_submit_jobs{}.sh".format(num), "w") as dy_sub:
    dy_sub.writelines(lines)
