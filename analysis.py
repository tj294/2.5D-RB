"""
Author: Tom Joshi-Cale
"""
# ====================
# IMPORTS
# ====================
import numpy as np
import h5py
import argparse
import matplotlib.pyplot as plt
import pathlib
import os
import shutil
import time
import imageio

from dedalus import public as de
from dedalus.tools import post

# ====================
# CLA PARSING
# ====================
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--input", help="Folder where the processing data is stored", required=True
)
parser.add_argument(
    "-t", "--heatmap", help="Plot a gif of the temperature heatmap", action="store_true"
)

args = parser.parse_args()

direc = os.path.normpath(args.input) + "/"


x = de.Fourier("x", 256, interval=(0, 3), dealias=3 / 2)
z = de.Chebyshev("z", 64, interval=(0, 1), dealias=3 / 2)
x = np.array(x.grid(1))
z = np.array(z.grid(1))

# ====================
# Plot heatmap
# ====================

if args.heatmap:
    filenames = []

    os.makedirs(direc + "figure", exist_ok=True)

    with h5py.File(direc + "snapshots/snapshots_s1/snapshots_s1_p0.h5", "r") as file:
        T = np.array(file["tasks"]["T"])
        u = np.array(file["tasks"]["u"])
        w = np.array(file["tasks"]["w"])
        snap_t = np.array(file["scales"]["sim_time"])
        snap_iter = np.array(file["scales"]["iteration"])

    xx, zz = np.meshgrid(x, z)

    maxT = np.max(T)
    maxU = np.max(u)
    maxW = np.max(w)

    n_iter = len(T[:, 0:, 0])
    start_time = time.time()
    print("Plotting {} graphs".format(n_iter))

    try:
        for i in range(0, int(n_iter)):
            fig = plt.figure(figsize=(8, 6))
            ax1 = fig.add_subplot(224)
            ax2 = fig.add_subplot(222)
            ax3 = fig.add_subplot(121)
            if (i % 50 == 0) and (i != 0):
                sec_per_frame = (time.time() - start_time) / i
                eta = sec_per_frame * (n_iter - i)
                print(
                    "Iteration {} reached after {:.2f} seconds".format(
                        i, time.time() - start_time
                    )
                )
                print("Current sec_per_frame is {:.2f} seconds".format(sec_per_frame))
                print("Estimated completion in {:.2f} seconds".format(eta))

            fig.suptitle(
                "Iteration: {}\n".format(snap_iter[i])
                + r"Sim Time: {:.2f} $\tau_\kappa$".format(snap_t[i])
            )
            c1 = ax1.contourf(
                xx,
                zz,
                np.transpose(u[i, :, :]),
                levels=np.linspace(np.min(u), maxU),
                cmap="coolwarm",
            )
            c1_bar = fig.colorbar(c1, ax=ax1)
            c1_bar.set_label("u", rotation=0)
            ax1.set_ylabel("z")
            ax1.set_xlabel("x")

            c2 = ax2.contourf(
                xx,
                zz,
                np.transpose(w[i, :, :]),
                levels=np.linspace(np.min(w), maxW),
                cmap="coolwarm",
            )
            c2_bar = fig.colorbar(c2, ax=ax2)
            c2_bar.set_label("w", rotation=90)
            ax2.set_ylabel("z")
            ax2.set_xlabel("x")

            c3 = ax3.contourf(
                xx,
                zz,
                np.transpose(T[i, :, :]),
                levels=np.linspace(0, maxT),
                cmap="coolwarm",
            )
            c3_bar = fig.colorbar(c3, ax=ax3)
            c3_bar.set_label("T")
            ax3.set_ylabel("z")
            ax3.set_xlabel("x")

            plt.tight_layout()
            plt.savefig(direc + "figure/fig_{:03d}.png".format(i))
            filenames.append(direc + "figure/fig_{:03d}.png".format(i))
            plt.close()
            plt.clf()
    except KeyboardInterrupt:
        print("ending loop")

    print("completed in {:.2f} sec".format(time.time() - start_time))

    print("Creating gif...")
    with imageio.get_writer(direc + "info.gif", mode="I") as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    print("Removing raw image files...")
    shutil.rmtree(direc + "figure")

print("done.")
