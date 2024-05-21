python3 ../convergence.py --cv FLC --temperature 323 --suffix FLC_323K --plotScale energy --xLo 0 --xUp 1 --yUp 5 --dat_files *.dat
python3 plot_fluxProfile.py --suffix DIPC_323K --dat_files *flux*.dat
