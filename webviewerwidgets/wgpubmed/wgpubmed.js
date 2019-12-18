widgetGenerators['pubmed'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Count', getWidgetData(tabName, 'pubmed', row, 'n'), tabName);
			var searchLink = getWidgetData(tabName, 'pubmed', row, 'term');
			addInfoLineLink(div, 'Search', searchLink, searchLink, 25);
		}
	}
}
