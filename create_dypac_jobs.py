import subprocess as sp

cmd = dict()
cmd["subject"] = "sub-05"
cmd["session"] = "all"
cmd["runs"] = ["all"]
cmd["clusters"] = ["20"]
cmd["states"] = "60"
cmd["batches"] = "3"
cmd["replication"] = "100"

cmds = []
for r in cmd["runs"]:
    cmds.append(
        """python generate_embeddings.py --subject={sub} --session={ses} --runs={run}  -n_clusters={cluster}  -n_states={state} -n_batch={batch} -n_replications={replication} \n""".format(
            sub=cmd["subject"],
            ses=cmd["session"],
            run=r,
            cluster=cmd["clusters"][0],
            state=cmd["states"],
            batch=cmd["batches"],
            replication=cmd["replication"]
        )
    )

with open("dypac_jobs.sh", "w") as dy:
    for c in cmds:
        dy.write(c)

dy.close()
