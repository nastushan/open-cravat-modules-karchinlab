widgetGenerators['thousandgenomes'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addBarComponent(div, row, 'Allele Frequency', 'thousandgenomes__af', tabName);
		}
	}
}