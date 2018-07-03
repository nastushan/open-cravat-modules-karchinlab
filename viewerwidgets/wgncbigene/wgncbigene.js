widgetGenerators['ncbigene'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Genomic', 'ncbigene__ncbi_desc', tabName);
		}
	}
}