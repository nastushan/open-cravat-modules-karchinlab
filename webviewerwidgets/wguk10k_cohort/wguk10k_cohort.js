widgetGenerators['uk10k_cohort'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Twins Alternative Allele Count', getWidgetData(tabName, 'uk10k_cohort', row, 'uk10k_twins_ac'), tabName);
			addBarComponent(div, row, 'Twins Alternative Allele Frequency', 'uk10k_cohort__uk10k_twins_af', tabName);
			addInfoLine(div, 'ALSPAC Alternative Allele Count', getWidgetData(tabName, 'uk10k_cohort', row, 'uk10k_alspac_ac'), tabName);
			addBarComponent(div, row, 'ALSPAC Alternative Allele Frequency', 'uk10k_cohort__uk10k_alspac_af', tabName);
		}
	}
}
