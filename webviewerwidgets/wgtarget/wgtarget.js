widgetGenerators['target'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Therapy', getWidgetData(tabName, 'target', row, 'therapy'), tabName);
			addInfoLine(div, 'Rationale', getWidgetData(tabName, 'target', row, 'rationale'), tabName);
		}
	}
}
