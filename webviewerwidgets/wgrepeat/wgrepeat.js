widgetGenerators['repeat'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Class', 'repeat__repeatclass', tabName);
			addInfoLine(div, row, 'Family', 'repeat__repeatclass', tabName);
			addInfoLine(div, row, 'Name', 'repeat__repeatname', tabName);
		}
	}
}
