widgetGenerators['civic_gene'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			div.innerText = getWidgetData('gene', 'civic_gene', row, 'description');
			div.style['word-break'] = 'break-word';
		}
	}
}
