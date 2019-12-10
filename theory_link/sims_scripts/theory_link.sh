# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=05:00:00
#PBS -l pmem=400mb,pvmem=600mb
#PBS -N job_theory

cd $HOME/quoter-model-NEW/theory_link/sims_scripts
python theory_link.py "$PBS_ARRAYID" "${n}"