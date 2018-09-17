# About MutPred

MutPred is a web application tool developed to classify an amino acid substitution (AAS) as disease-associated or neutral in human. In addition, it predicts molecular cause of disease/deleterious AAS. MutPred is based upon SIFT [1] and a gain/loss of 14 different structural and functional properties. For instance, gain of helical propensity or loss of a phosphorylation site. It was trained using the deleterious mutations from the Human Gene Mutation Database [2] and neutral polymorphisms from Swiss-Prot [3]. Current version of MutPred is 1.2. The update consists of replacing SIFT score by a more stable version of code that calculates evolutionary conservation. In addition, the I-mutant software was replaced by a more stable MUpro [4], by the Baldi group. The training data set was updated to contain 39,218 disease-associated mutations from HGMD and 26,439 putatively neutral substitutions from Swiss-Prot. 

## How do I interpret the results? 
The output of MutPred contains a general score (g), i.e., the probability that the amino acid substitution is deleterious/disease-associated, and top 5 property scores (p), where p is the P-value that certain structural and functional properties are impacted. 

Certain combinations of high values of general scores and low values of property scores are referred to as hypotheses.

- Scores with g > 0.5 and p < 0.05 are referred to as **actionable hypotheses**.
- Scores with g > 0.75 and p < 0.05 are referred to as **confident hypotheses**.
- Scores with g > 0.75 and p < 0.01 are referred to as **very confident hypotheses**.

MutPred is a collaborative effort between the Mooney group from the University of Washington and the Radivojac group from the School of Informatics and Computing, Indiana University. 

We welcome any suggestions and comments.

# Supported By

The work is funded by:
- NIH K22LM009135 (PI: Mooney)
- NIH 1R01LM009722 (PI: Mooney)
- NIH 5R01LM009722 (PI: Mooney)
- Indiana Genomics Initiative. The Indiana Genomics Initiative (INGEN) is supported in part by Lily Endowment.
- National Science Foundation, DBI-0644017 (PI: Predrag Radivojac)

# References

1. Ng, P.C. and Henikoff, S. (2003) SIFT: Predicting amino acid changes that affect protein function, Nucleic Acids Res, **31**, 3812-3814.

2. Stenson, P.D., et al. (2009) The Human Gene Mutation Database: 2008 update, Genome Med, **1**, 13.

3. Boeckmann, B., et al. (2003) The SWISS-PROT protein knowledgebase and its supplement TrEMBL in 2003, Nucleic Acids Res, **31**, 365-370.

4. Cheng, J., Randall. A. and Baldi, P. (2006) Prediction of Protein Stability Changes for Single-Site Mutations Using Support Vector Machines. Proteins: Structure, Function, Bioinformatics, **62**, 1125-1132.

# Contact Us

Prof. Predrag Radivojac
Department of Computer Science and Informatics
Indiana University
150 S. Woodlawn Avenue
Bloomington, IN 47405
Tel: (812) 856-1851
Web: www.cs.indiana.edu/~predrag 

Prof. Sean Mooney 
Department of Biomedical Informatics and Medical Education
Universiy of Washington
850 Republican Street
Seattle, WA 98109 
Tel: (206) 685-0249
Web: http://faculty.washington.edu/sdmooney 

# Disclaimer

The purpose of this resource is to distribute functional prediction of mutation data. The data is meant to be used for basic research. Do not use this data to make clinical decisions. 