widgetGenerators['pseudogene'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Gene', getWidgetData(tabName, 'pseudogene', row, 'pseudogene_hugo'), tabName);
			addInfoLine(div, 'Transcript', getWidgetData(tabName, 'pseudogene', row, 'pseudogene_transcript'), tabName);
		}
	}
}
