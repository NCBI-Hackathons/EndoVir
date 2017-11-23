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
![Endovir diagram](doc/figs/workflow.small.png)
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
