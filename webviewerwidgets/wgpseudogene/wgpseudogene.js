widgetGenerators['pseudogene'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Gene', 'pseudogene__pseudogene_hugo', tabName);
			addInfoLine(div, row, 'Transcript', 'pseudogene__pseudogene_transcript', tabName);
		}
	}
}
