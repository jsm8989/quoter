# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=12:00:00 
#PBS -l pmem=1500mb,pvmem=1800mb
#PBS -N job_small-clust

cd $HOME/quoter-model-NEW/small_world/sims_scripts
python small_world_clustering_sims.py "$PBS_ARRAYID" "${n}"