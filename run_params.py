"""
Parameters for rb_convect.py
"""
import numpy as np

a = 3
Ny, Nz = 256, 64
Pr = 0.8
Ra = 1e6
Ta = 5e6
phi = np.radians(45)  # latitude of box in radians


dt = 3e-6
max_dt = 1e-3

end_sim_time = 0.8
end_wall_time = np.inf
end_iteration = np.inf

snapshot_iter = 10
analysis_iter = 10
