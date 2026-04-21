all: enigma_lw_r.sif  # additional .sif files may be listed here for corresponding dockerfiles

%.sif: dockerfiles/%/Dockerfile
	docker build -t $* -f dockerfiles/$*/Dockerfile . && \
	scripts/convert_docker_image_to_singularity.sh $* && \
	scripts/move_singularity_file.sh $*

# Example commands executed by this make file
# 
# Running "make enigma_lw_r.sif" will issue the following commands:
# docker build -t enigma_lw_r -f dockerfiles/enigma_lw_r/Dockerfile . && \  # build docker container
#     scripts/convert_docker_image_to_singularity.sh enigma_lw_r && \         # produces enigma_lw_r.sif
#     scripts/move_singularity_file.sh.sh enigma_lw_r        # moves enigma_lw_r.sif to ../singularity/.
#  
# Running "make all" will build all singularity containers in this project
