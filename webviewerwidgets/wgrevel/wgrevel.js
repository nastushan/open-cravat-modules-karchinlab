widgetGenerators['revel'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Score', getWidgetData(tabName, 'revel', row, 'score'), tabName);
		}
	}
}
