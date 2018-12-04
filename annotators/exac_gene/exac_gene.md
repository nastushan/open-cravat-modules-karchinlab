# ExAC Functional Gene Constraint & CNV Scores: probability of LoF tolerance/intolerance
The ExAC database provided in this module contains the probability of a gene being loss-of-function (LoF) intolerant of both heterozygous & homzygous LoF variants as well as intolerant of only homozygous variants. Also provided is the probability of being tolerant of both heterozygous & homozygous LoF variants. Tolerance/Intolerance probabilities are also separated into additonal subsets of nonTCGA and nonpsych. Z scores for the deviation of observation from expectation are also included. Higher Z scores indicate the transcript is more intolerant of variation (more constrained).

NOTE: Data provided by [dbNSFP](https://sites.google.com/site/jpopgen/dbNSFP) version 3.5a

1. Prob of LoF Intolerance (Homo & Hetero): The probability of being LoF intolerant of both homozygous & heterozygous LoF variants.
2. Prob of LoF Intolerance (Homo): The probability of being LoF intolerant of homozygous, but not heterozygous LoF variants.
3. Prob of LoF Tolerance (Homo & Hetero): The probability of being tolerant of both homozygous & heterozygous LoF variants.
4. Prob of LoF Intolerance (Homo & Hetero) NonTCGA: The probability of being LoF intolerant of both homozygous & heterozygous LoF variants on the nonTCGA subset.
5. Prob of LoF Intolerance (Homo) NonTCGA: The probability of being LoF intolerant of homozygous, but not heterozygous LoF variants on the nonTCGA subset.
6. Prob of LoF Tolerance (Homo & Hetero) NonTCGA: The probability of being tolerant of both homozygous & heterozygous LoF variants on the nonTCGA subset.
7. Prob of LoF Intolerance (Homo & Hetero) Nonpsych: The probability of being LoF intolerant of both homozygous & heterozygous LoF variants on the nonpsych subset.
8. Prob of LoF Intolerance (Homo) Nonpsych: The probability of being LoF intolerant of homozygous, but not heterozygous LoF variants on the nonpsych subset.
9. Prob of LoF Tolerance (Homo & Hetero) Nonpsych: The probability of being tolerant of both homozygous & heterozygous LoF variants on the nonpsych subset.
10. Deletion Intolerance Z-Score: Winsorized deletion intolerance z-score based on CNV data.
11. Duplication Intolerance Z-Score: Winsorized duplication intolerance z-score based on CNV data.
12. CNV Intolerance Z-Score: Winsorized CNV intolerance z-score based on CNV data.
13. CNV Bias/Noise: (Y)es or (N)o depending on if the gene is in a known region of recurrent CNVs mediated by tandem segmental duplications and intolerance scores are more likely to be biased or noisy.
