widgetGenerators['interpro'] = {
	'variant': {
		'width': 280, 
		'height': 100, 
		'word-break': 'normal',
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Domain', 'interpro__domain', tabName, 45);
		}
	}
}