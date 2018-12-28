widgetGenerators['civic_gene'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			var link = infomgr.getRowValue(tabName, row, 'civic_gene__link');
			if (link == null) {
				link = 'None';
				addInfoLineText(div, 'Link', link);
			} else {
				addInfoLineLink(div, 'Link', link, link, -1);
			}
			addInfoLine(div, row, 'Description', 'civic_gene__description', tabName, 70);
		}
	}
}
