widgetGenerators['gwas_catalog'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Risk Allele', getWidgetData(tabName, 'gwas_catalog', row, 'risk_allele'), tabName);
			var riskAllele = getWidgetData(tabName, 'gwas_catalog', row, 'risk_allele');
			var altBase = getWidgetData(tabName, 'base', row, 'alt_base');
			var riskSpan = $(div).find('.detail-info-line-content')[0].children[0];
			if (riskAllele === altBase) {
				$(riskSpan).css('color','red');
			}
			addInfoLine(div, 'P-value', getWidgetData(tabName, 'gwas_catalog', row, 'pval'), tabName);
			addInfoLine(div, 'Initial Sample', getWidgetData(tabName, 'gwas_catalog', row, 'init_samp'), tabName);
			addInfoLine(div, 'Replication Sample', getWidgetData(tabName, 'gwas_catalog', row, 'rep_samp'), tabName);
			addInfoLine(div, 'Confidence Interval', getWidgetData(tabName, 'gwas_catalog', row, 'ci'), tabName);
		}
	}
}
