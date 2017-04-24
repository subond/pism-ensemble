#!/bin/bash

#SBATCH --qos={{submit_class}}
#SBATCH --time={{cluster_runtime}}
#SBATCH --job-name={{ensemble_name}}
#SBATCH --account=anthroia
#SBATCH --output=./log/slurm_out.out
#SBATCH --error=./log/slurm_error.err
#SBATCH --ntasks={{number_of_cores}}
#SBATCH --tasks-per-node=16
#SBATCH --profile=energy
#SBATCH --acctg-freq=energy=5
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user={{username}}@pik-potsdam.de

# get user and platform-specific variables like working_dir, pismcodedir,
# pism_exec and mpi command
source set_environment.sh

runname=`echo $PWD | awk -F/ '{print $NF}'`
outdir=$working_dir/$runname

module purge
module load pism/stable08_srunpetsc

# needed for srun
export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

export PISM_ON_CLUSTER=1
./run_smoothing_nomass.sh $SLURM_NTASKS > $outdir/log/pism.out
./run_full_physics.sh $SLURM_NTASKS >> $outdir/log/pism.out
echo run finished at `date`                     >> ./log/srunInfo


