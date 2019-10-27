# This job needs 1 compute node with 1 processor per node:
#PBS -l nodes=1:ppn=1
# Run on shortq (if under 3 hours) else on workq:
#PBS -q workq
# How much time and computer memory will the job need:
# (Jobs run more quickly the less resources they require)
#PBS -l walltime=5:00:00 
#PBS -l pmem=1500mb,pvmem=2gb
#PBS -N job_processCSV

cd $HOME/quoter-model-NEW/real_networks/processing
python real_nonlinks.py 

