widgetGenerators['ncbigene'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			div.innerText = infomgr.getRowValue('gene',row,'ncbigene__ncbi_desc');
			div.style['word-break'] = 'break-word';
		}
	}
}