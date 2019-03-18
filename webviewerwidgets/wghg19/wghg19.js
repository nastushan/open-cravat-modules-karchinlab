widgetGenerators['hg19'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Chromosome', 'hg19__chrom', tabName);
			addInfoLine(div, row, 'Position', 'hg19__pos', tabName);
		}
	}
}
