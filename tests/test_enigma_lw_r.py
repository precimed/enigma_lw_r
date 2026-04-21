# encoding: utf-8

"""
Test module for ``enigma_lw_r.sif`` singularity build
or ``enigma_lw_r`` dockerfile build

In case ``singularity`` is unavailable, the test function(s) should fall
back to ``docker``.
"""

import os
import subprocess
import tempfile

import pytest


# Check that (1) singularity or apptainer executables exist,
# and (2) if not, check for docker.
# If neither are found, tests will skip container runtime checks.
# This may be useful for testing on a local machine, but should
# be revised for the particular usecase.
cwd = os.getcwd()
EXPECTED_CONTAINER_BASE_IMAGE = 'ghcr.io/rocker-org/tidyverse:4.5.3'
EXPECTED_CRAN_REPOSITORY = (
    'https://packagemanager.posit.co/cran/__linux__/noble/2026-04-21'
)
EXPECTED_R_PACKAGES = [
    'fmsb',
    'glmnet',
    'PerformanceAnalytics',
    'caret',
    'tidymodels',
    'splitstackshape',
    'fastDummies',
    'pbapply',
    'lme4',
    'lmerTest',
    'kernlab',
]
try:
    pth = os.path.join('containers', 'enigma_lw_r.sif')
    try:
        runtime = 'apptainer'
        out = subprocess.run(runtime, check=False)
    except FileNotFoundError:
        try:
            runtime = 'singularity'
            out = subprocess.run(runtime, check=False)
        except FileNotFoundError as exc:
            raise FileNotFoundError from exc
    PREFIX = f'{runtime} run {pth}'
    PREFIX_MOUNT = f'{runtime} run --home={cwd}:/home/ {pth}'
    PREFIX_CUSTOM_MOUNT = f'{runtime} run --home={cwd}:/home/ ' + \
        '{custom_mount}' + f'{pth}'
except FileNotFoundError:
    try:
        runtime = 'docker'
        out = subprocess.run(runtime, check=False)
        PREFIX = (f'{runtime} run ' +
                  'ghcr.io/precimed/enigma_lw_r')
        PREFIX_MOUNT = (
            f'{runtime} run ' +
            f'--mount type=bind,source={cwd},target={cwd} ' +
            'ghcr.io/precimed/enigma_lw_r')
        PREFIX_CUSTOM_MOUNT = (
            f'{runtime} run ' +
            f'--mount type=bind,source={cwd},target={cwd} ' +
            '{custom_mount} ' +
            'ghcr.io/precimed/enigma_lw_r')
    except FileNotFoundError:
        # neither singularity nor docker found, skip runtime-dependent tests
        runtime = None
        PREFIX = ''
        PREFIX_MOUNT = ''
        PREFIX_CUSTOM_MOUNT = ''


def test_assert():
    """dummy test that should pass"""
    assert True


def test_enigma_lw_r_r():
    """test that the R installation works"""
    if runtime is None:
        pytest.skip('container runtime unavailable')
    call = f'{PREFIX} R --version'
    out = subprocess.run(call.split(' '), check=False)
    assert out.returncode == 0


def test_enigma_lw_r_r_script():
    '''test that R can run a script'''
    if runtime is None:
        pytest.skip('container runtime unavailable')
    call = f'{PREFIX} Rscript -e "cat(123)"'
    out = subprocess.run(call, shell=True, check=False)
    assert out.returncode == 0


def test_enigma_lw_r_dockerfile_base_image_and_r_packages_install():
    """test Dockerfile uses rocker tidyverse and installs required R pkgs"""
    dockerfile = os.path.join(
        cwd, 'docker', 'dockerfiles', 'enigma_lw_r', 'Dockerfile'
    )
    with open(dockerfile, 'r', encoding='utf-8') as f:
        content = f.read()

    assert f'FROM {EXPECTED_CONTAINER_BASE_IMAGE}' in content
    assert EXPECTED_CRAN_REPOSITORY in content
    assert 'install.packages(c(' in content
    for package in EXPECTED_R_PACKAGES:
        assert f"'{package}'" in content


def test_enigma_lw_r_r_script_from_tempdir():
    '''test that the tempdir is working'''
    if runtime is None:
        pytest.skip('container runtime unavailable')
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, 'hello.R'), 'w', encoding='utf-8') as f:
            f.write('cat("hello\\n")')
        if runtime == 'docker':
            custom_mount = f'--mount type=bind,source={d},target={d}'
        elif runtime in ['apptainer', 'singularity']:
            custom_mount = f'--bind {d}:{d} '
        else:
            custom_mount = ''
        call = f'{PREFIX_CUSTOM_MOUNT.format(custom_mount=custom_mount)} ' + \
            f'Rscript {d}/hello.R'
        out = subprocess.run(call, shell=True, check=False)
        assert out.returncode == 0


def test_enigma_lw_r_r_packages():
    '''test that the R packages are installed'''
    if runtime is None:
        pytest.skip('container runtime unavailable')
    packages = ', '.join(f"'{pkg}'" for pkg in EXPECTED_R_PACKAGES)
    call = (
        f'{PREFIX} Rscript -e '
        f'"for (p in c({packages})) library(p, character.only = TRUE)"'
    )
    out = subprocess.run(call, shell=True, check=False)
    assert out.returncode == 0
