# RVIS: Residual variation intolerance scoring
RVIS is a database providing variation intolerance scoring that assesses whether genes have relatively more or less functional genetic variation than expected based on the apparently neutral variation found in the gene. Scores were developed using sequence data from 6503 whole exome sequences made available by the NHLBI Exome Sequencing Project (ESP).

NOTE: Data provided by [dbNSFP](https://sites.google.com/site/jpopgen/dbNSFP) version 3.5a

1. Score: A score measuring intolerance of mutational burden, the higher the score the more tolerant to mutational burden the gene is. Based on EVS (ESP6500) data.
2. Percentile Rank: The percentile rank of the gene based on RVIS, the higher the percentile the more tolerant to mutational burden the gene is. Based on EVS (ESP6500) data.
3. FDR p-value: "A gene's corresponding FDR p-value for preferential LoF depletion among the ExAC population. Lower FDR corresponds with genes that are increasingly depleted of LoF variants."
4. ExAC-Based RVIS: "Setting 'common' MAF filter at 0.05% in at least one of the six individual ethnic strata from ExAC."
5. ExAC-Based RVIS Percentile: "Genome-Wide percentile setting 'common' MAF filter at 0.05% in at least one of the six individual ethnic strata from ExAC."
