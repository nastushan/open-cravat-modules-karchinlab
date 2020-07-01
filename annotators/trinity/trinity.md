# Trinity

Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads. Trinity partitions the sequence data into many individual de Bruijn graphs, each representing the transcriptional complexity at a given gene or locus, and then processes each graph independently to extract full-length splicing isoforms and to tease apart transcripts derived from paralogous genes.

## Trinity Cancer Transcriptome Analysis Toolkit (CTAT)

The Trinity Cancer Transcriptome Analysis Toolkit (CTAT) aims to provide tools for leveraging RNA-Seq to gain insights into the biology of cancer transcriptomes. Bioinformatics tool support is provided for mutation detection, fusion transcript identification, de novo transcript assembly of cancer-specific transcripts, lncRNA classification, and foreign transcript detection (viruses, microbes). CTAT is funded by the National Cancer Institute Informatics Technology for Cancer Research (NCI ITCR) program. Software tools and pipelines developed as components of Trinity CTAT are described below with links to the corresponding open source software, documentation, and tutorials.

## CTAT-Mutations Pipeline Overview

CTAT-Mutations Pipeline is a variant calling pipeline focussed on detecting mutations from RNA sequencing (RNA-seq) data. It integrates GATK Best Practices along with downstream steps to annotate, filter, and prioritize cancer mutations. This includes leveraging the RADAR and RediPortal databases for identifying likely RNA-editing events, dbSNP for excluding common variants, and COSMIC to highlight known cancer mutations. Finally, CRAVAT is leveraged to annotate and prioritize variants according to likely biological impact and relevance to cancer.

The CTAT Mutations pipeline is one of the components of the Trinity Cancer Transcriptome Analysis Toolkit (CTAT), complementing other functionality that leverages RNA-Seq data for characterizing cancer transcriptomes, including identification of fusion transcripts, copy number variations from tumor single cell transcriptomes, among other analyses.

Our CTAT-Mutation pipeline aims to make mutation discovery from rna-seq data as easy as possible, requiring only the rna-seq reads as input, and generating summary reports and visualizations to help guide you to the most meaningful findings.

Information from https://github.com/NCIP/Trinity_CTAT/wiki

