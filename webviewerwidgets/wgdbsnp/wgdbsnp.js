widgetGenerators['dbsnp'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'dbSNP', 'dbsnp__snp', tabName);
		}
	}
}