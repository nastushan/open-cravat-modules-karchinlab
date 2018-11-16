widgetGenerators['brca1_func_assay'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Function Score Mean', 'brca1_func_assay__score', tabName);
			addInfoLine(div, row, 'Function Class', 'brca1_func_assay__class', tabName);
		}
	}
}