# Dedalus code for 2.5D rotating Boussinesq Rayleigh Bérnard Convection

rb_convect.py is a Dedalus code that runs a 2.5D simulation in the x-z plane (so $\frac{d}{dy} = 0$), and in which quantities have been non-dimensionalised using the viscous time.

## For single-core (local sims)
1. Run the simulation
```bash
python3 rb_convect.py -o results/FOLDERNAME
```
2. plot heatmap and KE.
```bash
python3 analysis.py -i results/FOLDERNAME -t
```
3. See at what time-scales KE levels off and change `avg_t_start` and `avg_t_stop` in `analysis.py` accordingly.

4. Plot the horizontally averaged fluxes
```bash
python3 analysis.py -i results/FOLDERNAME -f
```

## For multi-core sims (Carpathia)
1. Edit `run_params.py` to set up the simulation as required.

2. Run the simulation and specify number of cores
```bash
mpiexec -n [NUMBER OF CORES] python3 rb_convect.py -o results/FOLDERNAME
```
3. Merge the outputted analysis and snapshot folders respectively:
```bash
python3 merge.py results/FOLDERNAME/analysis --cleanup
python3 merge.py results/FOLDERNAME/snapshots --cleanup
```

4. Continue as step3 from single core sims.
