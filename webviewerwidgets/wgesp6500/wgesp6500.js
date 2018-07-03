widgetGenerators['esp6500'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addBarComponent(div, row, 'Eur. American', 'esp6500__ea_pop_af', tabName);
			addBarComponent(div, row, 'Afr. American', 'esp6500__aa_pop_af', tabName);
		}
	}
}