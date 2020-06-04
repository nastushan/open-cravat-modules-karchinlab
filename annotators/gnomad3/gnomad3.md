# gnomAD - genome Aggregation Database

The Genome Aggregation Database is a resource developed by an international coalition of investigators, with the goal of aggregating and harmonizing both exome and genome sequencing data from a wide variety of large-scale sequencing projects, and making summary data available for the wider scientific community.

The v3 short variant data set provided on this website spans 71,702 genomes from unrelated individuals sequenced as part of various disease-specific and population genetic studies, and is aligned against the GRCh38 reference.

We have removed individuals known to be affected by severe pediatric disease, as well as their first-degree relatives, so these data sets should serve as useful reference sets of allele frequencies for severe pediatric disease studies - however, note that some individuals with severe disease may still be included in the data sets, albeit likely at a frequency equivalent to or lower than that seen in the general population.

## OpenCRAVAT specifics

OpenCRAVAT does not include variants which do not meet the gnomAD3 quality control process.

Additionally, in some cases, and variant will have an allele frequency of 0 for some populations, and empty or null for other populations. An AF of 0 means that there the population included individuals with high quality enough reads to make a call at this position, and none of those individuals had the alternate allele. An AF of empty/null means that there were no variants calls made for individuals in this population due to quality control filters.

![Screenshot](gnomad_screenshot_1.png)

![Screenshot](gnomad_screenshot_2.png)

![Screenshot](gnomad_screenshot_3.png)
