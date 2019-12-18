widgetGenerators['cgl'] = {
	'gene': {
		'width': 280, 
		'height': 180, 
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Class', getWidgetData(tabName, 'cgl', row, 'class'), tabName);
		}
	}
}
