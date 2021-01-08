from bids import BIDSLayout
import os

dataset = "data/cneuromod/friends"
derivatives = "fmriprep-20.1.0/fmriprep"
out_path = "output/bids/friends_bids_cache"

derivatives_path = os.path.join(dataset, "derivatives", derivatives)

layout = BIDSLayout(dataset, derivatives=derivatives_path)
layout.save(out_path)
