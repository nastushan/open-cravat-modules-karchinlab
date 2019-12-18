widgetGenerators['linsight'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'LINSIGHT Score', getWidgetData(tabName, 'linsight', row, 'value'), tabName);
		}
	}
}
