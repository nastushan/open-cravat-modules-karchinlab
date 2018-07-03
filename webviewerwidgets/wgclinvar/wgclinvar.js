widgetGenerators['clinvar'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Significance', 'clinvar__sig', tabName);
			addInfoLine(div, row, 'Diseases', 'clinvar__diseases', tabName);
			addInfoLine(div, row, 'Ref. Nums', 'clinvar__refs', tabName);
		}
	}
}