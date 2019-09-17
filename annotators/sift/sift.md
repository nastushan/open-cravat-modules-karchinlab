SIFT predicts whether an amino acid substitution affects protein function based on sequence homology and the physical properties of amino acids. SIFT can be applied to naturally occurring nonsynonymous polymorphisms and laboratory-induced missense mutations. It is widely used in bioinformatics, genetics, disease, and mutation studies. It annotates and provides damaging/tolerated predictions for single nucleotide variants.

## Brief Summary

SIFT takes a query sequence and uses multiple alignment information to predict tolerated and deleterious substitutions for every position of the query sequence.

SIFT is a multistep procedure that:

- searches for similar sequences,
- chooses closely related sequences that may share similar function to the query sequence ,
- obtains the alignment of these chosen sequences, and
- calculates normalized probabilities for all possible substitutions from the alignment.

## Interpreting Results

Positions with normalized probabilities less than 0.05 are predicted to be deleterious, those greater than or equal to 0.05 are predicted to be tolerated.