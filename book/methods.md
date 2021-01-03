# Methods
## Dypac 

Figure 1. Subject-specific dynamic parcellation approach at the full brain level (DYPAC2.0). A simple two level clustering is applied. The first level consists of running k-Means directly on the time series. Here, we generate a family of parcels represented with one-hot encoders. The second-level aggregation clustering procedure generates a set of state stability maps at the full brain level.

### Overview 
We implemented a new algorithm which identifies individual dynamic states of brain parcellation at the full brain, using a two-level ensemble clustering approach. This algorithm is an extension of the Dynamic Parcel Aggregation with Clustering (DYPAC2.0) algorithm proposed by Boukhdhir and colleagues [REF]. DYPAC2.0 uses a simple two level clustering, one on sliding time windows, and one-hot encoders aggregated over many windows.  A one-hot encoder is a binary vector of length V (number of voxels in a brain mask), in which each voxel has a value one if it is included in a given cluster, and zero otherwise. 

### First-level cluster analysis 
The first level clustering consists of replicating a k-Means analysis on R sliding windows of fixed size, uniformly distributed in a given fMRI time series. The k-Means algorithm has a parameter K which sets the number of clusters (parcels) in the brain. We generate an array of parcels represented with K one-hot encoders. K one-hot encoders of length V are generated for each sliding window, and one-hot vectors are aggregated over R replications, as well as B fMRI datasets (or runs) collected on the same individual (see Fig. 1). 

### Second-level cluster analysis 

The second-level aggregation clustering procedure groups the one-hot encoders into states. A traditional k-Means clustering with L states is again applied at this step. Note that this parameter is set globally, i.e. it indicates the overall number of possible states across all brain parcels. For each state cluster, the average of all one-hot encoders in that state is generated, producing a state stability map. Stability scores range from 0 to 1, with 0 indicating a voxel which was never associated with a brain parcel in that state, and 1 indicating a voxel always included in the parcels of that state (see Fig. 1). 

### State trimming 

Because we had observed in DYPAC1.0 that many dynamic states are noisy, and should not be included in a state, each state cluster is further “trimmed” using the following approach. For each one-hot vector in a state cluster, the average value of the stability map of that cluster is generated, over the voxels in the one-hot vector. Only one-hot vectors which achieve an average stability over a threshold t=0.3 are assigned to a state cluster. Final stability maps are generated after this trimming procedure, on the remaining one-hot vectors. Some state clusters may end up empty because of the trimming procedure, and will be excluded from further analysis, which means that the effective number of states after trimming may be less than the specified L.   

### Memory requirements 

Models were run using the following parameters: K=50 brain clusters, L=150 dynamic states and R=100 replications. Note that with the dataset we used, V~150k and B~60. In total, the array of one-hot encoders can reach a very large size, V x (K.R.B), but is tractable in memory because it is represented as a sparse boolean array. As K one-hot encoders coding for a given brain parcel have exactly V non-zero elements, the aggregated one-hot encoders use V.R.B bits of memory (independent of the number of clusters K). With the values listed above, the aggregated one-hot encoder array will have 150k.100.60=900M non-zero elements, which easily fits in memory even on commodity hardware. 

### Processing time 

We used the k-Means implementation of scikit-learn (REF) for both the first-level and second-level cluster analysis. This particular implementation supports sparse data, so the large number of features (V~150k) is handled efficiently, as each one-hot vector is very sparse, and the memory requirements are kept to a low level, as outlined in the preceding paragraph. This implementation still has a quadratic run-time complexity as a function of the number of measures to be clustered, which is here very large K.R.B=300k. In order to limit this computation time, we also implemented a version of DYPAC2.0 that relies on batches of fMRI  data. Additionally, we used the latest release of the k-Means implementation in scikit-learn which runs this algorithm in parallel on multiple cores. This further improves scalability on multiple cores. We rely on the parallel grid computing of compute canada which allows us to allocate up to 32 cores per node .  

### Batch processing 
To accommodate the large number of one-hot encoders size across multiple states at the full brain level, we subdivided the overall one-hot encoders into M batches (or subgroups) of one-hot encoders. Stability maps are generated independently in each batch, and then aggregated into an array of size V x (M.L). This array is entered into a third-level cluster analysis that groups the state stability maps into meta-states clusters. stability maps within a given meta-state are averaged to produce final stability maps. The batch size directly impacts the reliability of the estimation of the state stability maps. Therefore, there should be a compromise between the computational cost and the number of one-hot encoders. The higher the number of one-hot encoders are within the same batch, the better the state stability maps are. The lower the number of one-hot encoders is, the lower the computational cost is. In the application proposed here, as each subject had a large number of fMRI runs available (B~60), we used M=10.

### Code implementation

The code for DYPAC2.0 is available via github. The application program interface is inherited from the base linear decomposition class of the nilearn library [REF], and is using nilearn tools for loading preprocessed fMRIprep data and generating a brain mask. The codebase includes unit testing covering all key methods, and separates the ensemble clustering tools (bascpp.py), the fMRI interface (dypac.py) from the temporal embeddings tools (embeddings.py, see section on fMRI compression below). Nilearn and matplotlib [REF] were also used to generate all the figures in this paper. 

## Dataset and preprocessing 
The cneuromod movie10 dataset included about ten hours of functional data per participant. Six participants were included (female=3, male=3, their age ranges between X-XX years old. Informed consent was obtained from all participants (https://www.cneuromod.ca/). Each participant watched four different movies in the MRI scanner, including Bourne supremacy movie (~100 minutes duration), Wolf of wall street movie (~170 minutes duration), Hidden figures movie (~120 minutes duration, presented twice) and Life movie (~100 minutes duration, presented twice). Each movie was cut into roughly ten minute segments presented in a separate run. Exact cutting points were manually selected to not interrupt the narrative flow. 
For each functional MRI run, different steps of the fMRIPrep v20.1.1 preprocessing pipeline were applied (Esteban et al. 2019). First, a reference volume and its skull-stripped version were generated. To correct for susceptibility distortions, a deformation field was estimated using 3dQwarp AFNI (Esteban et al. 2019). Using the susceptibility distortion, an upwarped functional MRI reference run was computed to have a better co-registration with the anatomical reference. The functional MRI reference run was then co-registered to the T1w reference using flirt (i.e.; FSL 5.0.9). To correct the remaining distortions in the functional MRI reference runs, we configured co-registration with nine degrees of freedom. Head-motion parameters were also estimated before spatiotemporal filtering using mcflirt (i.e.; FSL 5.0.9, (Esteban et al. 2019)). Each functional MRI run was resampled into standard space, to generate a preprocessed functional BOLD signal the ‘MNI152NLin2009cAsym’ space. We computed several confounds based on the preprocessed functional BOLD signal, including framewise displacement (FD), DVARS and three regions-wise global signals using Nipype (Esteban et al. 2019). Moreover, we estimated a set of physiological regressors to correct for noise in the data, including principal components after high-pass filtering. Components were also calculated separately within the WM and CSF masks. We kept only the components that were sufficient to explain 50 percent of variance across the nuisance mask (CSF, WM, combined, or temporal). The remaining components were dropped from consideration. The 36P denoising strategy of ciric et al. 2017 was adapted for our preprocessing.  Head motion estimates, WM/CSF signals, and global signals were expanded with the inclusion of temporal derivatives, squares and squared derivatives (Ciric et al 2017). We excluded the frames that exceeded a threshold of 0.5 mm FD or 1.5 standardised DVARS. Volumetric resamplings were performed using antsApplyTransforms (ANTs), configured with Lanczos interpolation to minimize the smoothing effects of other kernels (lanczos). 
The load_confounds library is used to import confound factors generated by fmriprep in nilearn, following the Params36 strategy. These confounds were regressed out of individual fMRI time series, which were further standardized to a zero mean and unit variance and spatially smoothed with an 8 mm smoothing kernel using nilearn MultiNiftiMasker method. Dypac2.0 analyses were restricted to an individual-specific segmentation of the grey matter generated using freesurfer [REF] as part of the fmriprep preprocessing pipeline. 


## Functional MRI loss of information analysis after compression
We aimed to quantify the quality of the compressed functional MRI data and whether it was representative of these raw data. We separated the cneuromod movie10 into training and test sets. The training set was composed of 44 runs (~10 minutes each) from four different movies, including Life (5 runs), Bourne supremacy (10 runs), Hidden figures (12 runs), Wolf of wall street (17 runs). The test set was composed of only 17 runs (~10 minutes each) from two different movies, including Life (5 runs) and Hidden figures (12 runs).  We generated subject-specific parcellations on the training set, and then evaluated  compression quality on the test set. To quantify the compression quality of the functional MRI, we computed the R-squared measure between the preprocessed time series at each voxel, and the compressed time series using the DYPAC2.0 stability maps. Specifically, the fMRI time series were projected in the vector basis of stability maps using an ordinary least-squares linear projection. This resulted into a reduced set of time series, one per stability map. Then, the reduced time series were multiplied with the stability maps, in order to generate a linear mixture of parcels with same dimensionality as the original time series. The R-squared coefficient expressed the percentage of variance of the original time series effectively captured by the compressed time series. Note that the compression factor is very high (approximately 1000), as there are originally about 150k voxels, which get projected into a space of dimension lower than L=150 (the number of stability maps generated by DYPAC2.0). A higher R-squared score indicated a better explained variance in the functional MRI signal, or in other words lower information loss between the original signal and the compressed state stability map. We compared the R-squared measure both at the within- and the between-subjects level. At the within-subjects level, we computed the R-squared scores between each functional MRI run and all its corresponding state stability maps from the same subject. At the between-subjects level, the functional MRI runs were compressed using state stability maps associated with different subjects. We reported the results in Fig. 2 and Fig. 3. 

## Reproducibility analysis
We also aimed to evaluate the reproducibility of the dynamic states of parcellations at the full brain level. To this end, we conducted a quantitative consistency analysis both at the within- and the between-subject levels in the context of movie data. This allowed us to quantify and identify similarities and variations in the spatial reconfigurations of the dynamic states. We compared the spatial reproducibility at the within-subjects and the between-subjects levels in terms of the Pearson correlation measure of spatial stability maps. We matched the training set maps to the maps from the second set using the Hungarian method (REF: Kuhn, 2005).  A higher correlation showed a stronger linear relationship between two state stability maps. This indicated high spatial consistency between the dynamic states of parcellations from the two sets of independent data. We repeated these analyses at the full brain level (here, 150 states) and the six subjects of the cneuromod movie10 dataset. We reported the results in Fig. 4, 5, 6, 7, 8, 9 and 10. 