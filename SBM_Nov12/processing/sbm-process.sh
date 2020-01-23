# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q shortq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=02:00:00 
#PBS -l pmem=2500mb,pvmem=3gb
#PBS -N job_processing

cd $HOME/quoter-model-NEW/SBM_Nov12/processing
python sbm-process.py "$PBS_ARRAYID" "${n}"

