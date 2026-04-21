#!/bin/bash
version=24.7.1-2
curl -sSL https://github.com/conda-forge/miniforge/releases/download/$version/Miniforge3-$version-$(uname)-$(uname -m).sh -o /tmp/mambaforge.sh \
  && mkdir /root/.conda \
  && bash /tmp/mambaforge.sh -bfp /usr/local \
  && rm -rf /tmp/mambaforge.sh
