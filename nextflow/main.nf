#!/usr/bin/env nextflow
params.input_file = '../scripts/hello_world.py'
params.outdir = '.'

process HelloWorld {
    publishDir "$params.outdir"

    container 'ghcr.io/precimed/container_template'

    input:
    path input_file

    output:
    path "hello_world.txt"

    script:
    """
    python3 ${input_file} > hello_world.txt
    """
}

// Define workflow
workflow {
    HelloWorld(file(params.input_file))
}