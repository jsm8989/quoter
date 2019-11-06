# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=10:00:00 
#PBS -l pmem=512mb,pvmem=1gb
#PBS -N job_SBM40

cd $HOME/quoter-model-NEW/SBM-NEW/sims_scripts
python SBM_sims-p-mu-N40.py "$PBS_ARRAYID" "${n}"

