import os

from nilearn.image import load_img
from nilearn.input_data import NiftiMasker

from neuromaps.datasets import fetch_fslr
from surfplot.datasets import load_example_data
from neuromaps.transforms import mni152_to_fslr

from cneuromod_embeddings.dypac_utils import get_root_data
from surfplot import Plot
import argparse


def _load_components(subject, state, xp_type):

    # Set up file names... where to find the data.
    path_data = get_root_data("models")
    bg_img = os.path.join(
        path_data,
        xp_type,
        f"{subject}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz",
    )
    parcels = os.path.join(
        path_data,
        xp_type,
        f"{subject}_space-MNI152NLin2009cAsym_desc-dypac{state}_components.nii.gz",
    )
    mask = os.path.join(
        path_data, xp_type, f"{subject}_space-MNI152NLin2009cAsym_label-GM_mask.nii.gz"
    )

    # Load parcels
    masker = NiftiMasker(mask_img=mask, detrend=False, smoothing_fwhm=0)
    components = masker.fit_transform(parcels)
    return components


def _components2surface(components):
    # Get surface data
    surfaces = fetch_fslr()
    lh, rh = surfaces["inflated"]
    sulc_lh, sulc_rh = surfaces["sulc"]
    gii_lh, gii_rh = mni152_to_fslr(
        masker.inverse_transform(np.sum(components, axis=0))
    )

    # create surface plot
    plot_surface = Plot(lh, rh)
    plot_surface.add_layer(
        {"left": sulc_lh, "right": sulc_rh}, cmap="binary_r", cbar=False
    )
    plot_surface.add_layer(
        {"left": gii_lh, "right": gii_rh}, cmap="turbo", color_range=(0, 5)
    )
    return plot_surface


def _fig_n_states(plot_surface, subject):

    # Generate figure
    kws = dict(
        location="right", draw_border=False, aspect=10, shrink=0.2, decimals=0, pad=0
    )
    fig = plot_surface.build(cbar_kws=kws)
    fig.axes[0].set_title(f"n_states {subject}", pad=-3)


def generate_n_states_maps(subject, state, xp_type):
    components = _load_componenents(subject, state, xp_type)
    plot_surface = _load_surface_n_states(components)
    fig = _fig_n_states(plot_surface, subject)
    path_data = get_root_data("models")
    path_fig = os.path.join(path_data, xp_type, "figures_n_states")
    file_fig = os.path.join(
        path_fig,
        f"{subject}_space-MNI152NLin2009cAsym_desc-dypac{state}_components.nii.gz",
    )
    fig.savefig(file_fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--xp_type",
        help="The type of experiment [friends-s02 (default), movie10, hcptrt].",
    )
    parser.add_argument("--subject", type=int, help="subject ID")
    parser.add_argument("--state", type=int, help="number of states.")
    args = parser.parse_args()
    generate_n_states_maps(args)
