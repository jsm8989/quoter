# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=12:00:00 
#PBS -l pmem=700mb,pvmem=1500mb
#PBS -N jobfile_ER

cd $HOME/quoter-model-NEW/ER_BA_N1000/sims_scripts
python ER_sims.py "$PBS_ARRAYID" "${n}"