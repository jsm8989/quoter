# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=18:00:00 
#PBS -l pmem=3gb,pvmem=4gb
#PBS -N job_SBM

cd $HOME/quoter-model-NEW/SBM_Vocab/sims_scripts
python SBM_sims.py "$PBS_ARRAYID" "${n}"
