widgetGenerators['ncrna'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Class', 'ncrna__ncrnaclass', tabName);
			addInfoLine(div, row, 'Name', 'ncrna__ncrnaname', tabName);
		}
	}
}