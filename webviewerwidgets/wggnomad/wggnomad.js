widgetGenerators['gnomad'] = {
	'variant': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			addBarComponent(div, row, 'Total', 'gnomad__af', tabName);
			addBarComponent(div, row, 'African', 'gnomad__af_afr', tabName);
			addBarComponent(div, row, 'American', 'gnomad__af_amr', tabName);
			addBarComponent(div, row, 'Ash Jew', 'gnomad__af_asj', tabName);
			addBarComponent(div, row, 'East Asn', 'gnomad__af_eas', tabName);
			addBarComponent(div, row, 'Finn', 'gnomad__af_fin', tabName);
			addBarComponent(div, row, 'Non-Finn Eur', 'gnomad__af_nfe', tabName);
			addBarComponent(div, row, 'Other', 'gnomad__af_oth', tabName);
			addBarComponent(div, row, 'South Asn', 'gnomad__af_sas', tabName);
		}
	}
}