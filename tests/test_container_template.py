# encoding: utf-8

"""
Test module for ``container_template.sif`` singularity build
or ``container_template`` dockerfile build

In case ``singularity`` is unavailable, the test function(s) should fall
back to ``docker``.
"""

import os
import subprocess
import tempfile


# Check that (1) singularity or apptainer executables exist,
# and (2) if not, check for docker.
# If neither are found, tests will fall back to plain python.
# This may be useful for testing on a local machine, but should
# be revised for the particular usecase.
cwd = os.getcwd()
EXPECTED_CONTAINER_BASE_IMAGE = 'quay.io/condaforge/miniforge3:26.1.1-3'
try:
    pth = os.path.join('containers', 'container_template.sif')
    try:
        runtime = 'apptainer'
        out = subprocess.run(runtime, check=False)
    except FileNotFoundError:
        try:
            runtime = 'singularity'
            out = subprocess.run(runtime, check=False)
        except FileNotFoundError as exc:
            raise FileNotFoundError from exc
    PREFIX = f'{runtime} run {pth} python'
    PREFIX_MOUNT = f'{runtime} run --home={cwd}:/home/ {pth} python'
    PREFIX_CUSTOM_MOUNT = f'{runtime} run --home={cwd}:/home/ ' + \
        '{custom_mount}' + f'{pth} python'
except FileNotFoundError:
    try:
        runtime = 'docker'
        out = subprocess.run(runtime, check=False)
        PREFIX = (f'{runtime} run ' +
                  'ghcr.io/precimed/container_template python')
        PREFIX_MOUNT = (
            f'{runtime} run ' +
            f'--mount type=bind,source={cwd},target={cwd} ' +
            'ghcr.io/precimed/container_template python')
        PREFIX_CUSTOM_MOUNT = (
            f'{runtime} run ' +
            f'--mount type=bind,source={cwd},target={cwd} ' +
            '{custom_mount} ' +
            'ghcr.io/precimed/container_template python')
    except FileNotFoundError:
        # neither singularity nor docker found, fall back to plain python
        runtime = None
        PREFIX = 'python'
        PREFIX_MOUNT = 'python'
        PREFIX_CUSTOM_MOUNT = 'python'


def test_assert():
    """dummy test that should pass"""
    assert True


def test_container_template_python():
    """test that the Python installation works"""
    call = f'{PREFIX} --version'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0


def test_container_template_python_script():
    '''test that Python can run a script'''
    cwd = os.getcwd() if runtime == 'docker' else '.'
    call = f'''{PREFIX_MOUNT} {cwd}/tests/extras/hello.py'''
    out = subprocess.run(call.split(' '), capture_output=True)
    assert out.returncode == 0


def test_container_template_dockerfile_base_image_and_env_install():
    """test that Dockerfile uses miniforge base image and environment.yml"""
    dockerfile = os.path.join(
        cwd, 'docker', 'dockerfiles', 'container_template', 'Dockerfile'
    )
    with open(dockerfile, 'r', encoding='utf-8') as f:
        content = f.read()

    assert f'FROM {EXPECTED_CONTAINER_BASE_IMAGE}' in content
    assert 'mamba env update --name base --file environment.yml' in content


def test_container_template_python_script_from_tempdir():
    '''test that the tempdir is working'''
    with tempfile.TemporaryDirectory() as d:
        os.system(f'cp {cwd}/tests/extras/hello.py {d}/')
        if runtime == 'docker':
            custom_mount = f'--mount type=bind,source={d},target={d}'
        elif runtime in ['apptainer', 'singularity']:
            custom_mount = f'--bind {d}:{d} '
        else:
            custom_mount = ''
        call = f'{PREFIX_CUSTOM_MOUNT.format(custom_mount=custom_mount)} ' + \
            f'{d}/hello.py'
        out = subprocess.run(call, shell=True, check=False)
        assert out.returncode == 0


def test_container_template_python_packages():
    '''test that the Python packages are installed'''
    packages = [
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
        'seaborn',
        'sklearn',
        'pytest',
        'jupyterlab',
    ]
    importstr = 'import ' + ', '.join(packages)
    call = f"{PREFIX} -c '{importstr}'"
    out = subprocess.run(call, shell=True)
    assert out.returncode == 0
