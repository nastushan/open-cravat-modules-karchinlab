widgetGenerators['ncbigene'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			var value = getWidgetData(tabName, 'ncbigene', row, 'ncbi_desc');
            if (value == undefined) {
                value = 'No data';
            }
			div.innerText = value;
			div.style['word-break'] = 'break-word';
		}
	}
}
