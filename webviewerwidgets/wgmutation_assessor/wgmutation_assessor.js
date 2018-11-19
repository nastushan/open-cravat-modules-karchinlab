widgetGenerators['mutation_assessor'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Mutation Variant', 'mutation_assessor__mut_var', tabName);
			addInfoLine(div, row, 'Mutation Score', 'mutation_assessor__mut_score', tabName);
			addInfoLine(div, row, 'Mutation Rank Score', 'mutation_assessor__mut_rscore', tabName);
			addInfoLine(div, row, 'Mutation Functional Impact', 'mutation_assessor__mut_pred', tabName);
		}
	}
}