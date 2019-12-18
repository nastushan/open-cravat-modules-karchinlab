widgetGenerators['exac_gene'] = {
	'gene': {
		'width': 330, 
		'height': 100, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			var gene = getWidgetData(tabName, 'ess_gene', row, 'ess_gene');
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
