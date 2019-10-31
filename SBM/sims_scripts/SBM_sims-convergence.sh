# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=14:00:00 
#PBS -l pmem=3500mb,pvmem=4gb
#PBS -N jobfile_SBM-conv

cd $HOME/quoter-model-NEW/SBM/sims_scripts
python SBM_sims-convergence.py "$PBS_ARRAYID" "${n}"

