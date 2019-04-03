widgetGenerators['cgl'] = {
	'gene': {
		'width': 180, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Class', 'cgl__class', tabName);
		}
	}
}
