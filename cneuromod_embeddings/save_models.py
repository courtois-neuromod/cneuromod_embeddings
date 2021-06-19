import os
import numpy as np
from cneuromod_embeddings.dypac_utils import get_root_data, load_dypac
from cneuromod_embeddings.repro_summary import load_repro, visu_match
from dypac_utils import dypac_params, subject_keys

root_data = get_root_data('data/friends-s02')
root_models = get_root_data('models')
list_subject = subject_keys(6)
xp_type = 'friends-s02'
params = dypac_params(xp_type)
fwhm = 5

for subject in list_subject:
    print(f"\n{subject} state ")
    for num, state in enumerate(params["state"]):
        print(f"{state} ")
        cluster = params['cluster'][num]
        model, mask_img = load_dypac(
                subject=subject, 
                root_data=root_data, 
                fwhm=fwhm, 
                cluster=cluster, 
                state=state, 
                batch="training", 
                xp_type=xp_type
                )

        # Save mask only once
        if num == 0:
            file_mask = os.path.join(root_models, f"mask_{subject}.nii.gz")
            mask_img.to_filename(file_mask)

        # Save all models
        parcels = model.masker_.inverse_transform(model.components_)    
        file_parcels = os.path.join(root_models, f"dypac{state}_{subject}.nii.gz")
        parcels.to_filename(file_parcels)

