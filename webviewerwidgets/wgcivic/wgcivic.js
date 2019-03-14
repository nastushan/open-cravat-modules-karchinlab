widgetGenerators['civic'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Clinical actionability score', 'civic__clinical_a_score', tabName);
			addInfoLine(div, row, 'Description', 'civic__description', tabName);
			addInfoLine(div, row, 'Diseases', 'civic__diseases', tabName);
		}
	}
}