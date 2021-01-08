from dypac.embeddings import Embedding
from sklearn.preprocessing import OneHotEncoder
from nilearn.image import resample_to_img
from nilearn.input_data import NiftiMasker


class BaseMasker:

    def __init__(self):
        """
        Build a Dypac-like masker from labels.

        Parameters
        ----------
        masker:
            a nilearn NiftiMasker.

        Attributes
        ----------
        masker_:
            The nilearn masker
        """

    def _check_components_(self):
            """Check for presence of estimated components."""
            if not hasattr(self, "components_"):
                raise ValueError(
                    "Object has no components_ attribute. "
                    "This is probably because fit has not "
                    "been called."
                )


    def load_img(self, img, confound=None):
        """
        Load a 4D image using the same preprocessing as model fitting.

        Parameters
        ----------
        img : Niimg-like object.
            See http://nilearn.github.io/manipulating_images/input_output.html
            An fMRI dataset

        Returns
        -------
        img_p : Niimg-like object.
            Same as input, after the preprocessing step used in the model have
            been applied.
        """
        self._check_components_()
        tseries = self.masker_.transform([img], [confound])
        return self.masker_.inverse_transform(tseries[0])

    def transform(self, img, confound=None):
        """
        Transform a 4D dataset in a component space.

        Parameters
        ----------
        img : Niimg-like object.
            See http://nilearn.github.io/manipulating_images/input_output.html
            An fMRI dataset
        confound : CSV file or 2D matrix, optional.
            Confound parameters, to be passed to nilearn.signal.clean.

        Returns
        -------
        weights : numpy array of shape [n_samples, n_states + 1]
            The fMRI tseries after projection in the parcellation
            space. Note that the first coefficient corresponds to the intercept,
            and not one of the parcels.
        """
        self._check_components_()
        tseries = self.masker_.transform([img], [confound])
        del img
        return self.embedding_.transform(tseries[0])

    def inverse_transform(self, weights):
        """
        Transform component weights as a 4D dataset.

        Parameters
        ----------
        weights : numpy array of shape [n_samples, n_states + 1]
            The fMRI tseries after projection in the parcellation
            space. Note that the first coefficient corresponds to the intercept,
            and not one of the parcels.

        Returns
        -------
        img : Niimg-like object.
            The 4D fMRI dataset corresponding to the weights.
        """
        self._check_components_()
        return self.masker_.inverse_transform(self.embedding_.inverse_transform(weights))

    def compress(self, img, confound=None):
        """
        Provide the approximation of a 4D dataset after projection in parcellation space.

        Parameters
        ----------
        img : Niimg-like object.
            See http://nilearn.github.io/manipulating_images/input_output.html
            An fMRI dataset
        confound : CSV file or 2D matrix, optional.
            Confound parameters, to be passed to nilearn.signal.clean.

        Returns
        -------
        img_c : Niimg-like object.
            The 4D fMRI dataset corresponding to the input, compressed in the parcel space.
        """
        self._check_components_()
        tseries = self.masker_.transform([img], [confound])
        del img
        return self.masker_.inverse_transform(self.embedding_.compress(tseries[0]))

    def score(self, img, confound=None):
        """
        R2 map of the quality of the compression.

        Parameters
        ----------
        img : Niimg-like object.
            See http://nilearn.github.io/manipulating_images/input_output.html
            An fMRI dataset
        confound : CSV file or 2D matrix, optional.
            Confound parameters, to be passed to nilearn.signal.clean.

        Returns
        -------
        score : Niimg-like object.
            A 3D map of R2 score of the quality of the compression.

        Note
        ----
        The R2 score map is the fraction of the variance of fMRI time series captured
        by the parcels at each voxel. A score of 1 means perfect approximation.
        The score can be negative, in which case the parcellation approximation
        performs worst than the average of the signal.
        """
        self._check_components_()
        tseries = self.masker_.transform([img], [confound])
        del img
        return self.masker_.inverse_transform(self.embedding_.score(tseries[0]))


class LabelsMasker(BaseMasker):

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
        labels_mask = nifti_masker.fit_transform(labels_r)
        self.masker_ = model.masker_
        self.components_ = OneHotEncoder().fit_transform(labels_mask.transpose())
        self.embedding_ = Embedding(self.components_.todense().transpose())


class MapsMasker(BaseMasker):

    def __init__(self, model, maps):
        """
        Build a Dypac-like masker from a collection of brain maps.

        Parameters
        ----------
        model:
            a Dypac model.

        maps:  4D niimg-like object
            See http://nilearn.github.io/manipulating_images/input_output.html
            Set of continuous maps. One representative time course per map is
            extracted using least square regression.

        Attributes
        ----------
        components_:
            each column is brain map, after masking

        embedding_:
            see the class Embedding from Dypac.
        """
        maps_r = resample_to_img(source_img=maps,
            target_img=model.mask_img_, interpolation="continuous")
        nifti_masker = NiftiMasker(
            mask_img=model.mask_img_,
            standardize=False,
            smoothing_fwhm=None,
            detrend=False,
            memory="nilearn_cache",
            memory_level=1,
        )
        maps_mask = nifti_masker.fit_transform(maps_r)
        self.masker_ = model.masker_
        self.components_ = maps_mask.transpose()
        self.embedding_ = Embedding(self.components_.transpose())
