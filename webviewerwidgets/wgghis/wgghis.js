widgetGenerators['ghis'] = {
	'gene': {
		'width': 280, 
		'height': 280, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addBarComponent(div, row, 'GHIS Score', 'ghis__ghis', tabName)
		}
	}
}
