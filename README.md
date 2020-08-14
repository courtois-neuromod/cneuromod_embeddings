# Loading a parcellation model
At the moment, the individual cneuromod parcellations have been generated in the folder `/data/cisl/dypac_output/29062020/embeddings/first_run` on the `elm` server. Each parcellation model is relatively large (300 MB). The parcellations are saved in pickle files called `sub-{XX}_runs{NN}_cluster50_states150_batches10_reps100.pickle` where `XX` is the number of the subject `1` to `6`, and `NN` is the number of runs used to generate the parcels (typically around 40). To load a parcellation model, use the following instructions:
``` 
import pickle as pl
hf = open('sub-01_runs44_cluster50_states150_batches10_reps100.pickle', 'rb')
model = pl.load(hf)
hf.close()
```
These particular parcellations have 150 different brain parcels. See below for an explanation of the other parameters in the file name. 

# From 4D nifti fMRI run to a numpy array
Now, if you want to load a 4D imaging dataset and project it in the parcellation space, you will need to have `nilearn` and [load_confounds](https://github.com/SIMEXP/load_confounds) installed. The code will look like:
```
from load_confounds import Params24
file = `run.nii.gz`
conf = Params24(file)
tseries = model.transform(file, confounds=conf) 
``` 
This is going to load the 4D data using a `Params24` denoising strategy, as well as the same options used to generate the parcels (including an 8 mm isotropic smoothing). What you get is a `tseries` numpy ndarray of size `n_samples` (the number of time frames) times `n_parcels + 1`. The first column is the brain global signal, and each following row is the activity weight of a given parcel.

# From a numpy array to a 4D nifti fMRI run 
Now suppose that you have an array `maps_parcels` of size `[K, 1 + n_parcels]` where each row represents a brain map in the parcellation space. You can get back a 4D nifti volume where each time frame corresponds to one of the `K` rows, using the following code:
``` 
maps = model.inverse_transform(maps_parcels) 
``` 
For example, if you have a vector of values of brain decoding accuracy for each parcel, you can get a brain voxel wise map using the line above. Just make sure that the vector is shaped [1, 1 + n_parcels]). 

# Generation parameters 
The parcellations have been generated using the `cneuromod-2020-alpha` release. Specifically, it used the four first movies of `movie10` (`bourne`, `wolf`, `life` and `figures`), totalling about 40 runs per subject. Note that the repetition of `life` and `figures` were excluded from the generation process. The generation algorithm is summarized below:
* For each run, `100` sliding windows of fMRI data were selected, and a k-means clustering was applied to generate 50 clusters at each window. 
* The clusters were converted into one-hot encoding vectors, and concatenated across runs and windows, resulting into (50 clusters) x (100 windows) x (40 runs) = 200k distinct one hot vectors. 
* Those one hot vectors were split into 10 equal batches of size 20k, and a trimmed k-means clustring was applied to extract 150 states, which are characterized by the average of all one-hot vectors within a state (called stability map). 
* The 1500 state maps (150 states x 10 batches) were further clustered across the 10 batches into 150 final stability maps, which are stored in the model and used for data reduction.  
