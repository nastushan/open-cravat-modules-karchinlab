widgetGenerators['target'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Therapy', 'target__therapy', tabName);
			addInfoLine(div, row, 'Rationale', 'target__rationale', tabName);
		}
	}
}
