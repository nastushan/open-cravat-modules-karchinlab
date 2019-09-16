widgetGenerators['pharmgkb'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Chemical', 'pharmgkb__chemical', tabName);
			addInfoLine(div, row, 'Description', 'pharmgkb__sentence', tabName);
		}
	}
}
