# Endovir notes

## ngs-python

 - finicky to install as include:

### Issues
- LibManager.py:229

      `check_vers_res` calls external python interpreter to check Python
       version. The from import assumes global/local installed python-ngs
       and throws error below, but works.

```
        Traceback (most recent call last):
        File "<string>", line 1, in <module>
        ModuleNotFoundError: No module named 'ngs'

```

 - Threading in EndovirTools:
    Detect aborts in threaded processes

- Logging is still a nightmare. Need to add `logging` from `Python`.
## Remarks

 - The namespace `parser` cannot be used in own packages since
   it's used by python itself.

 - SRR5150787 is assembled into 4 contigs by megahit, but rpsblast (online
   against CDD and local against curated virus motifs) reports no hits. 
   blastx finds hits, will need to add diamond as well, I guess.

 - Need to find the way to use SRA reads form locally cached DB instead of writing reads to file
## Ideas:
- Status: use codes from /usr/include/sysexits.h?
  - Or use global error codes and not per tool (this sounds more sane)

- Adding a further complexity: use only a fraction of the flanks, e.g. 25%, in 
  mapping extensions