import os
import h5py
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="Input directory.")
parser.add_argument("-f", "--fwhm", type=int, help="Smoothing parameter.")
parser.add_argument("-a", "--atlases", type=int, help="Atlas names, string with coma separated names.")
args = parser.parse_args()

atlases = args.atlases.split(",")

for file_ in os.listdir(args.dir):
    if os.path.splitext(file_)[1] == ".hdf5" and "sub-" in file_ and "fwhm{}".format(args.fwhm) in file_:
        atlas = file_.split("_")[0]
        if atlas in atlases:
            sub = file_.split("_")[1]
            in_f = h5py.File(os.path.join(args.dir, file_), "r")
            out_f = h5py.File(os.path.join(args.dir, atlas+"_fwhm-"+fwhm+"_r2_score.hdf5"), "a")
            out_grp = out_f.create_group(sub)
            in_grp = list(in_f.keys())[0]
            for key in list(in_f[in_grp].keys()):
                out_grp.create_dataset(key, data=in_f[in_grp][key][:])
            in_f.close()
            out_f.close()


