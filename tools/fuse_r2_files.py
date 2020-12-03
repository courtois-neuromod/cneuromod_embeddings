import os
import h5py

in_dir = "output/other_atlases"
out_dir = "output/other_atlases"
atlases = ["mist444", "mist197", "schefer", "smith"]
fwhm = "8"

for file_ in os.listdir(in_dir):
    if os.path.splitext(file_)[1] == ".hdf5" and not "fwhm" in file_:
        atlas = file_.split("_")[0]
        sub = file_.split("_")[1]
        in_f = h5py.File(os.path.join(in_dir, file_), "r")
        out_f = h5py.File(os.path.join(out_dir, atlas+"_fwhm-"+fwhm+"_r2_score.hdf5"), "a")
        out_grp = out_f.create_group("sub-"+sub)
        in_grp = list(in_f.keys())[0]
        for key in list(in_f[in_grp].keys()):
            out_grp.create_dataset(key, data=in_f[in_grp][key][:])
        in_f.close()
        out_f.close()


