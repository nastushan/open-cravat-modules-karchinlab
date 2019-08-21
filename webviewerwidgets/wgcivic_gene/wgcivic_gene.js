widgetGenerators['civic_gene'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			div.innerText = infomgr.getRowValue('gene',row,'civic_gene__description');
		}
	}
}
