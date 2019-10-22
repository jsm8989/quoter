# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=10:00:00 
#PBS -l pmem=2gb,pvmem=3gb
#PBS -N job_configSmall

cd $HOME/quoter-model-NEW/real_networks/sims_scripts
python configMod_sims_small.py "$PBS_ARRAYID" "${n}"

