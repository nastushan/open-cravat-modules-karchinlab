widgetGenerators['phdsnpg'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Prediction', 'phdsnpg__prediction', tabName);
			addBarComponent(div, row, 'Score', 'phdsnpg__score', tabName);
			addBarComponent(div, row, 'FDR', 'phdsnpg__fdr', tabName);
		}
	},
	'gene': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Max score', 'vest__max_score', tabName);
			addInfoLine(div, row, 'Mean score', 'vest__mean_score', tabName);
			addInfoLine(div, row, 'Gene p-value', 'vest__gene_pval', tabName);
		}
	}
}