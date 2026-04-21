version 1.0 

task hello_world { 
    input {
        File input_file
        String output_file_name
    }

    command {
        python3 ~{input_file} > ~{output_file_name} 
    }

    output {
        File output_file = output_file_name
    }

    runtime {
        docker: "ghcr.io/precimed/container_template" 
    }
}