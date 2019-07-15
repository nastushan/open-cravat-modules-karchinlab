widgetGenerators['pubmed'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Count', 'pubmed__n', tabName);
			var searchLink = infomgr.getRowValue(tabName, row, 'pubmed__term');
			addInfoLineLink(div, 'Search', searchLink, searchLink, 25);
		}
	}
}