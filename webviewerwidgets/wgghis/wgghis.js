widgetGenerators['ghis'] = {
	'gene': {
		'width': 180, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addBarComponent(div, row, 'GHIS Score', 'ghis__ghis', tabName)
		}
	}
}
