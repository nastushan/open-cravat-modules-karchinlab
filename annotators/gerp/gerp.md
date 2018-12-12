# GERP++: Genomic Evolutionary Rate Profiling
GERP++ identifies constrained elements in multiple alignments by quantifying substitution deficits. These deficits represent substitutions that would have occurred if the element were neutral DNA, but did not occur because the element has been under functional constraint. We refer to these deficits as "Rejected Substitutions" (RS).

NOTE: Data provided by [dbNSFP](https://sites.google.com/site/jpopgen/dbNSFP) version 3.5a

1. Neutral Rate: Neutral rate of substitution.
2. RS Score: Rejected substitution score, the larger the score, the more conserved the site. Scores range from -12.3 to 6.17.
3. RS Ranked Score: RS scores were ranked among all GERP++ RS scores in the database. The rankscore is the ratio of the rank of the score over the total number of GERP++ RS scores in the database.