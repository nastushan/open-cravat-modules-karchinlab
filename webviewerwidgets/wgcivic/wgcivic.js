widgetGenerators['civic'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Clinical actionability score', getWidgetData(tabName, 'civic', row, 'clinical_a_score'), tabName);
			addInfoLine(div, 'Description', getWidgetData(tabName, 'civic', row, 'description'), tabName);
			addInfoLine(div, 'Diseases', getWidgetData(tabName, 'civic', row, 'diseases'), tabName);
		}
	}
}
