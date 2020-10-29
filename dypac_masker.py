from dypac.embeddings import Embedding
from sklearn.preprocessing import OneHotEncoder
from nilearn.image import resample_to_img

class DypacLabels:

    def __init__(self, model, labels):
        """
        Build a Dypac-like masker from labels.

        Parameters
        ----------
        model:
            a Dypac model.

        labels:
            a brain volumes with parcels (labels).

        Attributes
        ----------
        components_:
            each column is a onehot encoder for one of the parcels.

        embedding_:
            see the class Embedding from Dypac.
        """
        labels_r = resample_to_img(source_img=labels,
            target_img=model.mask_img_, interpolation="nearest")
        nifti_masker = NiftiMasker(
            mask_img=model.mask_img_,
            standardize=False,
            smoothing_fwhm=None,
            detrend=False,
            memory="nilearn_cache",
            memory_level=1,
        )
        labels_vox = nifti_masker.fit_transform(labels_r)
        self.masker_ = model.masker_
        self.components_ = OneHotEncoder().fit_transform(labels_vox.transpose())
        self.embedding_ = Embedding(basis.todense().transpose())


    def transform(self, img, confounds=None):
        """
        Transform a 4D nifti dataset into parcel-based time series.

        Parameters
        ----------
        img: Niimg-like object
            A 4D dataset.

        confounds: csv/tsv file, numpy array, or pandas dataframe

        Returns
        -------
        tseries: numpy array
            Size is number of time points x number of brain parcels.
        """
        tseries_voxel = self.masker_.transform([img], [confounds])
        return self.embedding_.transform(tseries_voxel)


    def inverse_transform(self, tseries):
        tseries_vox = self.embedding_.inverse_transform(tseries)
        return self.masker_.inverse_transform(tseries_vox)
