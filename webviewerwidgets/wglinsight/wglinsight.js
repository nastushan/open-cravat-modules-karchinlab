widgetGenerators['linsight'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'LINSIGHT Score', 'linsight__value', tabName);
		}
	}
}
