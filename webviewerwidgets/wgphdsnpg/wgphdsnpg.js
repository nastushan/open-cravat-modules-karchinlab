widgetGenerators['phdsnpg'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Prediction', 'phdsnpg__prediction', tabName);
			addBarComponent(div, row, 'Score', 'phdsnpg__score', tabName);
			addBarComponent(div, row, 'FDR', 'phdsnpg__fdr', tabName);
		}
	}
}