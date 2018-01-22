#!/bin/bash
#  setup.sh
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0

esearch=$(which esearch)
efetch=$(which efetch)
xtract=$(which xtract)

endovir_pssms='endovir.pn'


export ENDOVIR=$(pwd)
endovir_dbs="$ENDOVIR/work/analysis/dbs"
endovir_tools="$ENDOVIR/tools"
mkdir -p $endovir_tools
mkdir -p $endovir_dbs

function setup_magicblast()
{
  wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.3.0-x64-linux.tar.gz -P $endovir_tools -0 "magicblast.tar.gz"
  tar  -C magicblast -xvf "$endovir_tools/magicblast.tar.gz"
  export PATH=$PATH:$endovir_tools/magicblast/bin
}

function make_virus_db()
{
  virus_genome_db="viral.genomic.refseq.fna"
  wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz -O - | gzip -dc  > $endovir_dbs/$virus_genome_db
  wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.2.1.genomic.fna.gz -O - | gzip -dc >> $endovir_dbs/$virus_genome_db
  local makeblastdb=$(which makeblastdb)
  $makeblastdb -in     $endovir_dbs/$virus_genome_db  \
               -dbtype 'nucl'                         \
               -title 'virusdb'                       \
               -parse_seqids                          \
               -hash_index                            \
               -out "$endovir_dbs/$virus_genome_db"

}

function make_endovir_cdd()
{
  local makeprofiledb=$(which makeprofiledb)
  echo "" > "$endovir_dbs/$endovir_pssms"
  local qry="txid10239[Organism:exp] NOT (predicted OR putative)"
  for i in $($esearch -db  cdd -query "$qry"                      | \
             $efetch -format docsum                               | \
             $xtract -pattern DocumentSummary -element Accession  | \
             grep -v cl)
    do
      echo $i".smp" >> "$endovir_dbs/$endovir_pssms"
    done

  local cdd_ftp='ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'
  wget $cdd_ftp -O - | tar -C "$endovir_dbs/" -xzvT "$endovir_dbs/$endovir_pssms"
  cd $endovir_dbs
  $makeprofiledb -title "endovir"                    \
                 -in "$endovir_dbs/$endovir_pssms"   \
                 -out "$endovir_dbs/endovir_cdd"     \
                 -threshold 9.82                     \
                 -scale 100                          \
                 -dbtype rps                         \
                 -index true
  cd $ENDOVIR
}

#make_endovir_cdd
make_virus_db
