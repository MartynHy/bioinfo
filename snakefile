alleles, = glob_wildcards('/home/hymar/Pulpit/Hydzik_project-20240802T112315Z-001/Hydzik_project/project/input/{allele}.fna')

rule all:

    input:
        'outputs/mlst.tsv'
        

rule blastn:

    params:
        evalue = 0.01,
        subject = '/home/hymar/Pulpit/Hydzik_project-20240802T112315Z-001/Hydzik_project/project/genomes/GCA_001208825.1_genomic.fna.gz',
        cols = 'qseqid sseqid qcovs evalue'
        
    threads:
            1
    input: 
        '/home/hymar/Pulpit/Hydzik_project-20240802T112315Z-001/Hydzik_project/project/input/{allele}.fna'

    output:
        'outputs/blastn.tsv'

    log:
        'logs/blastn.log'
        
    shell:

        '''cat {input} | blastn -subject <(gunzip -c {params.subject}) -evalue {params.evalue} -outfmt '6 {params.cols}' -num_threads {threads} > {log} 2>&1'''


rule filter:

    params:
        cols = rules.blastn.cols,
        qcovs = 100

    threads:
            1
    
    input:
        rules.blastn.output

    output:
        'outputs/filtered.tsv'
    
    log:
        'logs/filtered.log'
        
    shell:
        '''scripts/filter.py --qcovs {params.qcovs} --cols {params.cols} --input {input} --output {output}>{log} 2>&1'''

    
rule filtered_modif:

    params:
        cols = rules.blastn.cols

    threads:
            1
    input:
        rules.filter.output
    
    output:
        'outputs/filtered_modif.tsv'
    
    log:
        'logs/filtered_modif'
    
    shell:
        '''scripts/filtered_modif.py --cols {params.cols} --input {input} --output {output}>{log} 2>&1'''


rule mlst:


    params:
        cols = 'qseqid sseqid qcovs evalue gene allele'

    threads:
            1
    input:
        first = rules.filtered_modif.output
        second = '/home/hymar/Pulpit/Hydzik_project-20240802T112315Z-001/Hydzik_project/project/input/bigsdb.tsv'
    
    output:
        'outputs/mlst.tsv'
    
    log:
        'logs/mlst'
    
    shell:
        '''scripts/mlst.py --cols {params.cols} --input {input.first} --input2 {input.second} --output {output}>{log} 2>&1'''
        

        
