widgetGenerators['ess_gene'] = {
	'gene': {
		'width': 330, 
		'height': 100, 
		'function': function (div, row, tabName) {
			var gene = infomgr.getRowValue(tabName, row, 'ess_gene__ess_gene');
			if(gene === 'N'){
				gene ='Non-essential';
			}
			else if (gene === 'E'){
				gene = 'Essential';
			}
			addInfoLineText(div, 'Essential/Non-essential Phenotype-Changing', gene);
		}
	}
}