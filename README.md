# EndoVir
Discovery of Novel Endogenous Viruses

## Abstract
This project strives to  implement the BUD algorithm from
[ViruSpy](https://github.com/NCBI-Hackathons/ViruSpy)  in Python. In short,
reads from a Short Read Archive (SRA) are screened for putative virus
motifs/domains using known virus nucleotide an protein sequences. Sequences
containign such motifs or domains serve as queries in subsequent searches using
the same SRA to extend the initial sequence until non-virus sequences/domians are
encountered. This inidicates that either en exogenous virts has been identified
or an endogenosu virus within a the host genome.


### Setup
Setup analysis enviroment:
 - `git clone https://github.com/NCBI-Hackathons/EndoVir.git`
 - `cd Endovir`
 - `mkdir -p work/analysis/dbs`
 - `cd work/analysis/dbs`
 - `wget ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/little_endian/Cdd_LE.tar.gz`
 - `tar -xzvf Cdd_LE.tar.gz`

#### Install external tools:
All external tools have to be currentlyin `$PATH`. Please see the corresponding
README files for installation instructions.
  - cd ../../../ (should be in EndoVir/)
  - export ENDOVIR=`pwd`
  - mkdir tools
  - cd tools
  - [MagicBLAST 1.3.0](wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.3.0-x64-linux.tar.gz       [check for updates])
    tar -xvzf ncbi-magicblast-1.3.0-x64-linux.tar.gz
    export PATH=$PATH:$ENDOVIR/EndoVir/tools/ncbi-magicblast-1.3.0/bin/ >> ~/.bashrc (check to make sure this is the right path)
  - [sra-toolkit](wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2-1/sratoolkit.2.8.2-1-centos_linux64.tar.gz [check for updates; might also want to use ubuntu])
    tar -xvzf sratoolkit.2.8.2-1-centos_linux64.tar.gz
    export PATH=$PATH:$ENDOVIR/tools/sratoolkit.2.8.2-1-centos_linux64/bin/ >> ~/.bashrc (check to make sure this is the right path)
  - [MEGAHIT](https://github.com/voutcn/megahit)
     git clone https://github.com/voutcn/megahit.git 
     cd megahit
     make (-j n, where n is the # of cores you want to use)
     export PATH=$PATH:$ENDOVIR/tools/megahit >> ~/.bashrc (check to make sure this is the right path)
  *- [ABYSS2]
    wget http://www.bcgsc.ca/platform/bioinfo/software/abyss/releases/2.0.2/abyss-2.0.2.tar.gz
  - [SOAPdenovo]
  - [SPADES]*
    source ~/.bashrc
   
   

### Run
Change into your working directory `work`
 - `cd ../../work`
 - `python3.6 ../src/endovir.py`

### Design
The underlying design of `endovir` will facilitate the use of external tools, e.g.
assemblers or parser, without changing the BUD routine itself. Further, the
results of the intermediate steps can be parsed and used to set the parameters
for each subsequent step in the analysis pipeline.

The use of  STDIN and STDOUT is used were  possible to communicate
between the external tools, thereby reducing the usage of intermediate files as
much as possible. In addition, only the Python standard libraries should be
used.

## Diagram
![Endovir diagram](doc/figs/workflow/workflow.small.png)
## Pipeline approach

The pipline has three major steps (in `src`):
- `endovir.Endovir()`: creates the analysis environment and prepares the
screening.


- `screener.Screener()`: Initiates the screen and identifies the initial,
putative virus contigs.

- `viruscontig.VirusContig()`: Each putative virus contig is expanded and
analyzed independently.

external screening tools, e.g MagicBLAST, have wrappers and parser in their
corresponding namespace in `lib`.

## Dependencies
Only the Python standard  libraries are used. However, the pipeline depends on
several external tools which are called using the `subprocess` module:

- [MagicBLAST](ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast)
- [BLAST+](ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST)
- [sra-toolkit](https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=software)
- [MEGAHIT](https://github.com/voutcn/megahit)


# References:
 - [BLAST Command Line Manual](https://www.ncbi.nlm.nih.gov/books/NBK279690/)
 - [Magic-BLAST](https://github.com/boratyng/magicblast)
 - [NCBI Conserved Domain and Protein Classification](https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml)
 - [MEGAHIT Paper](https://www.ncbi.nlm.nih.gov/pubmed/25609793)
