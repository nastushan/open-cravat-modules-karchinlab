widgetGenerators['ncrna'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Class', getWidgetData(tabName, 'ncrna', row, 'ncrnaclass'), tabName);
			addInfoLine(div, 'Name', getWidgetData(tabName, 'ncrna', row, 'ncrnaname'), tabName);
		}
	}
}
