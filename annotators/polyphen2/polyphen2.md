PolyPhen-2 is a new development of the PolyPhen tool for annotating coding nonsynonymous SNPs. Some of the highlights of the new version are:

* High quality multiple sequence alignment pipeline
* Probabilistic classifier based on machine-learning method

## Overview

Most of human genetic variation is represented by SNPs (Single-Nucleotide Polymorphisms) and many of them are believed to cause phenotypic differences between human individuals.


We specifically focus on nonsynonymous SNPs (nsSNPs), i.e., SNPs located in coding regions and resulting in amino acid variation in protein products of genes. It was shown in several studies that impact of amino acid allelic variants on protein structure/function can be reliably predicted via analysis of multiple sequence alignments and protein 3D-structures. As we demonstrated in an earlier work, these predictions correlate with the effect of natural selection seen as an excess of rare alleles. Therefore, predictions at the molecular level reveal SNPs affecting actual phenotypes.


PolyPhen-2 is an automatic tool for prediction of possible impact of an amino acid substitution on the structure and function of a human protein. This prediction is based on a number of features comprising the sequence, phylogenetic and structural information characterizing the substitution.


For a given amino acid substitution in a protein, PolyPhen-2 extracts various sequence and structure-based features of the substitution site and feeds them to a probabilistic classifier.

__OpenCRAVAT PolyPhen2 scores are sourced from [dbNSFP](https://sites.google.com/site/jpopgen/dbNSFP)__