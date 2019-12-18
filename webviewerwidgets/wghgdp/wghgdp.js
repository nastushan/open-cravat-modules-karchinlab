widgetGenerators['hgdp'] = {
	'variant': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			addBarComponent(div, row, 'European AF', 'european_allele_freq', tabName);
			addBarComponent(div, row, 'African AF', 'african_allele_freq', tabName);
			addBarComponent(div, row, 'Mid. Eastern AF', 'middle_eastern_allele_freq', tabName);
			addBarComponent(div, row, 'East Asian AF', 'east_asian_allele_freq', tabName);
			addBarComponent(div, row, 'CS Asian AF', 'cs_asian_allele_freq', tabName);
			addBarComponent(div, row, 'Oceanian AF', 'oceanian_allele_freq', tabName);
			addBarComponent(div, row, 'Native Amer. AF', 'native_american_allele_freq', tabName);
		}
	}
}
