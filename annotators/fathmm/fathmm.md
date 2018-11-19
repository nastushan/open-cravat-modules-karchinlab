# FATHMM: functional analysis through hidden markov models

NOTE: Data provided by [dbNSFP](https://sites.google.com/site/jpopgen/dbNSFP) version 3.5a

1. Ensembl Transcript ID: Multiple entries separated by ";"
2. Ensembl Protein ID: Multiple entries separated by ";" corresponding to Transcript IDs
3. FATHMM Score: FATHMM default score (weighted for human inherited-disease mutations with Disease Ontology) (FATHMMori). Scores range from -16.13 to 10.64. The smaller the score the more likely the SNP has damaging effect. Multiple scores separated by ";", corresponding to Protein ID.
4. FATHMM Converted Rank Score: FATHMMori scores were first converted to FATHMMnew=1-(FATHMMori+16.13)/26.77, then ranked among all FATHMMnew scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of FATHMMnew scores in dbNSFP. If there are multiple scores, only the most damaging (largest) rankscore is presented. The scores range from 0 to 1.
5. FATHMM Prediction: If a FATHMMori score is <=-1.5 (or rankscore >=0.81332) the corresponding nsSNV is predicted as "D(AMAGING)"; otherwise it is predicted as "T(OLERATED)". Multiple predictions separated by ";", corresponding to Protein ID.
