widgetGenerators['denovo'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'PubMed ID', getWidgetData(tabName, 'denovo', row, 'PubmedId'), tabName);
			addInfoLine(div, 'Primary phenotype', getWidgetData(tabName, 'denovo', row, 'PrimaryPhenotype'), tabName);
			addInfoLine(div, 'Validation', getWidgetData(tabName, 'denovo', row, 'Validation'), tabName);
		}
	}
}
