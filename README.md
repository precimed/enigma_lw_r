# enigma_lw_r project

Lightweight R container build for Enigma work, based on the [Rocker project](https://rocker-project.org/images/versioned/rstudio.html) rocker/tidyverse:4.3.1 image, with some additional tools and packages added. 
Refer to the Rocker project for more information on the base image and included tools/packages, and to the [Dockerfile](./docker/dockerfiles/enigma_lw_r/Dockerfile) for the additional tools/packages included in this container build.

## Build status

[![License](http://img.shields.io/:license-GPLv3+-green.svg)](http://www.gnu.org/licenses/gpl-3.0.html)
[![Documentation Status](https://readthedocs.org/projects/container-template/badge/?version=latest)](https://container-template.readthedocs.io/en/latest/?badge=latest)
[![Flake8 lint](https://github.com/precimed/enigma_lw_r/actions/workflows/python.yml/badge.svg)](https://github.com/precimed/enigma_lw_r/actions/workflows/python.yml)
[![Dockerfile lint](https://github.com/precimed/enigma_lw_r/actions/workflows/docker.yml/badge.svg)](https://github.com/precimed/enigma_lw_r/actions/workflows/docker.yml)
[![Container build](https://github.com/precimed/enigma_lw_r/actions/workflows/container_build.yml/badge.svg)](https://github.com/precimed/enigma_lw_r/actions/workflows/container_build.yml)
[![Container build push](https://github.com/precimed/enigma_lw_r/actions/workflows/container_build_push.yml/badge.svg)](https://github.com/precimed/enigma_lw_r/actions/workflows/container_build_push.yml)

## Description of available containers

* ``enigma_lw_r`` - a R container setup

## Software versions

Below is the list of tools included in the different Dockerfile(s) and installer bash scripts for each container.
Please keep up to date (and update the main `<enigma_lw_r>/README.md` when pushing new container builds):

### Installation and set up

#### Dependencies on host system

In order to set up these resource, some software may be required

- [Singularity/SingularityCE](https://sylabs.io/singularity/) or [Apptainer](https://apptainer.org)
- [Git](https://git-scm.com/)
- [Git LFS](https://git-lfs.com)
- [ORAS CLI](https://oras.land)

#### Clone the repository

To download the last revision of this project, issue:

```bash
cd path/to/repositories
git clone --depth 1 https://github.com/precimed/enigma_lw_r.git
cd enigma_lw_r
git lfs pull  # pull "large" files
```

#### Update the `enigma_lw_r.sif` container

To obtain updated versions of the Singularity Image Format (.sif) container file `, issue

```bash
cd path/to/repositories/enigma_lw_r/containers
mv enigma_lw_r.sif enigma_lw_r.sif.old  # optional, just rename the old(er) file
apptainer pull enigma_lw_r.sif docker://ghcr.io/precimed/enigma_lw_r:<tag>  # or 
oras pull ghcr.io/precimed/enigma_lw_r_sif:<tag>
```

where `<tag>` corresponds to a tag listed under [packages](https://github.com/precimed/enigma_lw_r/pkgs/container/enigma_lw_r),
such as `latest`, `main`, or `sha_<GIT SHA>`. 
The `oras pull` statement pulls the `enigma_lw_r.sif` file from [ghcr.io](https://github.com/precimed/enigma_lw_r/pkgs/container/enigma_lw_r_sif) using the [ORAS](https://oras.land) registry, without the need to build the container locally.

#### Pulling and using Docker image

To pull the corresponding Docker image, issue:

```bash
docker pull ghcr.io/precimed/enigma_lw_r:<tag>
```

If working on recent Macs, add the `--platform=linux/amd64` after `docker pull`. 
This may allow replacing `singularity exec ...` or `apptainer exec ...` statements with appropriate `docker run ...` statements, 
on systems where Singularity or Apptainer is unavailable.
Functionally, the Docker image is equivalent to the Singularity container, but note that syntax for mounting volumes and invoking commands may differ.
Please refer to [docs.docker.com](https://docs.docker.com) for more information.

> [!NOTE] Note that the provided Docker image may not support all CPUs, and may not be able to run on all systems via CPU virtualization.
> An option may be to build the Docker image on the host machine (e.g., M1/M2 Macs, older Intel/AMD CPUs), as:
>
>```bash
>docker build --platform=linux/amd64 -t ghcr.io/precimed/enigma_lw_r -f dockerfiles/enigma_lw_r/Dockerfile .
>```

Example of using the Docker image:

```bash
#!/bin/bash
# define environment variables:
export IMAGE="ghcr.io/precimed/enigma_lw_r:latest"  # adapt as necessary
# shortcuts for R and interactive shell:
export R="docker run --platform=linux/amd64 --rm -v ${PWD}:/home -w/home --entrypoint=R ${IMAGE}"
export ISHELL="docker run --platform=linux/amd64 --rm -it -v ${PWD}:/home -w/home --entrypoint=bash ${IMAGE}"

# invoke R help/list local directory
$R --help
$R -e "list.files()"
```

### Systems without internet access

Some secure platforms do not have direct internet access, hence we recommend cloning/pulling all required files on a machine with internet access as explained above, and archive the `enigma_lw_r` directory with all files and moving it using whatever file uploader is available for the platform.

```bash
cd /path/to/enigma_lw_r
SHA=$(git rev-parse --short HEAD)
cd ..
tar --exclude=".git/*" -cvf enigma_lw_r_$SHA.tar enigma_lw_r
```

### enigma_lw_r.sif
  
| OS/tool             | Version               | License           | Source
| ------------------- | --------------------- | ----------------- | -------------
| ubuntu              | 24.04                 | [Creative Commons CC-BY-SA version 3.0 UK licence](https://ubuntu.com/legal/intellectual-property-policy) | [Ubuntu.com](https://ubuntu.com)
| R                   | 4.5.3                 | [Misc.](hhttps://www.r-project.org/Licenses/) | [R](https://www.r-project.org)

## Building/rebuilding containers

While we don't necessarily recommend building containers locally, it is possible.
For instructions on how to build or rebuild containers manually using [Docker](https://www.docker.com) and [Singularity](https://docs.sylabs.io) refer to [`<enigma_lw_r>/docker/README.md`](https://github.com/precimed/enigma_lw_r/blob/main/docker/README.md).

## Unit tests

Unit tests are available in the `<enigma_lw_r>/tests` directory. 
These are run using the [pytest](https://docs.pytest.org/en/stable/) framework, and part of the GitHub Actions workflow.
To run the tests locally, issue:

```bash
cd <enigma_lw_r>
(pip install pytest)  # if not already installed
py.test -v tests
```

## Build the documentation

Within this repository, the html-documentation can be built from source files put here using [Sphinx](https://www.sphinx-doc.org/en/master/index.html). 
To do so, install Sphinx and some additional packages in Python using [Conda](https://docs.conda.io/en/latest/) by issuing:

```
cd <enigma_lw_r>/docs/source
conda env create -f environment.yml  # creates environment "sphinx"
conda activate sphinx  # activates environment "sphinx
make html  # builds html documentation into _build/html/ subdirectory
```

The built documentation can be viewed locally in a web browser by opening the file 
`<enigma_lw_r>/docs/source/_build/html/index.html`

The documentation may also be hosted online on [readthedocs.org](https://readthedocs.org).

## SLURM jobscript example

A basic job script example for running a Singularity container in an HPC setting with the [SLURM](https://slurm.schedmd.com) job scheduler is provided in the file [singularity_slurm_job.sh](https://github.com/precimed/enigma_lw_r/blob/main/scripts/singularity_slurm_job.sh), and should be modified as needed.
It expects a few environment variables, and can be submitted as

```
export JOBNAME=enigma_lw_r
export ACCOUNT=<project allocation account name>
export WALLTIME="00:05:00"  # expected run time HH:MM:SS format
export CPUS_PER_TASK=1  # number of CPU cores
export MEM_PER_CPU=2000MB  # RAM per CPU
export SINGULARITY_MODULE=singularity/3.7.1  # name of Singularity module and version

sbatch singularity_slurm_job.sh  # submit job
```
The output of the job will be written to the text files `enigma_lw_r.out` (output) and `enigma_lw_r.err` (errors).


## Workflows

The following sections describe how to run the provided workflows using different workflow management systems.
The Docker container is assumed to be available and tagged as `ghcr.io/precimed/enigma_lw_r:latest`: 

```bash
# (optional) make sure that the container is available; tagged as "latest"
docker pull --platform=linux/amd64 ghcr.io/precimed/enigma_lw_r:<tag>
docker image tag ghcr.io/precimed/enigma_lw_r:0.1.0 ghcr.io/precimed/enigma_lw_r:latest
```

### WDL

The [Workflow Description Language](https://openwdl.org) (WDL) is a way to describe workflows in a way that is portable and reproducible.

We have included a basic WDL file and JSON file defining inputs in the `<enigma_lw_r>/wdl` directory.
To run the pipeline, you will need to install [miniwdl](https://github.com/chanzuckerberg/miniwdl?tab=readme-ov-file#miniwdl) or some other execution engine like [Cromwell](https://cromwell.readthedocs.io/en/stable/), and run the following command:

```bash
cd <enigma_lw_r>/wdl
# (optional) create a new conda environment and install miniwdl
conda create -n miniwdl -c conda-forge pip -y
conda activate miniwdl
pip install miniwdl

# run the WDL file
miniwdl run hello_world.wdl -i inputs.json
```

To check the output, see the file

```
<enigma_lw_r>/wdl/_LAST/out/output_file/<output_file_name>
```
### Nextflow

[Nextflow](https://www.nextflow.io) is a workflow manager that enables the development of portable and reproducible workflows.

We have provided a basic Nextflow script in the `<enigma_lw_r>/nextflow` directory. 
To execute the workflow, you will need to (optionally) install Nextflow and run the following command:

```bash
cd <enigma_lw_r>/nextflow
# (optional) download and install nextflow executable in the current directory
curl -s https://get.nextflow.io | bash

# run Snakemake
./nextflow run nextflow/main.nf
```

The output will be written to the `output_file` defined in the Nextflow script.

### Snakemake

[Snakemake](https://snakemake.github.io) is a workflow management system that aims to reduce the complexity of creating workflows by providing a fast and comfortable way to define them.

We have provided a basic Snakefile in the `<enigma_lw_r>/snakemake` directory.
To run the pipeline, you will need to install Snakemake and run the following command:

```bash
# (optional) create a new conda environment and install Snakemake
cd <enigma_lw_r>/snakemake
# (optional) create a new conda environment and install miniwdl
conda create -c conda-forge -c bioconda -n snakemake snakemake -y
conda activate snakemake

# run Snakemake
snakemake
```

The output will be written to the `output_file` defined in the Snakefile.

## Feedback

If you face any issues, or if you need additional software, please let us know by creating a new [issue](https://github.com/precimed/enigma_lw_r/issues/new).
