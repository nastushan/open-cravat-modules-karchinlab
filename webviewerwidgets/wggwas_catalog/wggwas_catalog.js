widgetGenerators['gwas_catalog'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Risk Allele', 'gwas_catalog__risk_allele', tabName);
			var riskAllele = infomgr.getRowValue('variant',row,'gwas_catalog__risk_allele');
			var altBase = infomgr.getRowValue('variant',row,'base__alt_base')
			var riskSpan = $(div).find('.detail-info-line-content')[0].children[0];
			if (riskAllele === altBase) {
				$(riskSpan).css('color','red');
			}
			addInfoLine(div, row, 'P-value', 'gwas_catalog__pval', tabName);
			addInfoLine(div, row, 'Initial Sample', 'gwas_catalog__init_samp', tabName);
			addInfoLine(div, row, 'Replication Sample', 'gwas_catalog__rep_samp', tabName);
			addInfoLine(div, row, 'Confidence Interval', 'gwas_catalog__ci', tabName);
		}
	}
}