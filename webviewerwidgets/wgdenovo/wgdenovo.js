widgetGenerators['denovo'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'PubMed ID', 'denovo__PubmedId', tabName);
			addInfoLine(div, row, 'Primary phenotype', 'denovo__PrimaryPhenotype', tabName);
			addInfoLine(div, row, 'Validation', 'denovo__Validation', tabName);
		}
	}
}
