widgetGenerators['vcfinfo'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Phred', 'vcfinfo__phred', tabName);
			addInfoLine(div, row, 'Filter', 'vcfinfo__filter', tabName);
			addInfoLine(div, row, 'Zygosity', 'vcfinfo__zygosity', tabName);
			addInfoLine(div, row, 'Alt reads', 'vcfinfo__alt_reads', tabName);
			addInfoLine(div, row, 'Total reads', 'vcfinfo__tot_reads', tabName);
			addInfoLine(div, row, 'Allele frequency', 'vcfinfo__af', tabName);
		}
	}
}
