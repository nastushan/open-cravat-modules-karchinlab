widgetGenerators['gnomad3'] = {
	'variant': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			addBarComponent(div, row, 'Total', 'gnomad3__af', tabName);
			addBarComponent(div, row, 'African', 'gnomad3__af_afr', tabName);
			addBarComponent(div, row, 'Ashkenazi', 'gnomad3__af_asj', tabName);
			addBarComponent(div, row, 'East Asn', 'gnomad3__af_eas', tabName);
			addBarComponent(div, row, 'Finn', 'gnomad3__af_fin', tabName);
			addBarComponent(div, row, 'Latino', 'gnomad3__af_lat', tabName);
			addBarComponent(div, row, 'Non-Finn Eur', 'gnomad3__af_nfe', tabName);
			addBarComponent(div, row, 'Other', 'gnomad3__af_oth', tabName);
			addBarComponent(div, row, 'South Asn', 'gnomad3__af_sas', tabName);
		}
	}
}