# FamilyTreeDNA Converter

Converts typical FamilyTreeDNA text output.

Files typically look like this:
```
RSID,CHROMOSOME,POSITION,RESULT
"rs3094315","1","752566","XX"
"rs3131972","1","752721","XY"
...
```

As of 2020/2/20, most FamilyTreeDNA files will be on the hg19/GRCh37 genome. Be sure to specify the correct genome when submitting a job. Use the `-l/--liftover hg19` option in the cmd line, or the "Genome" dropdown at the top of the submission section of the GUI.
