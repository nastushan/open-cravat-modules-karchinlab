widgetGenerators['rvis'] = {
	'gene': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Residual Variation Intolerance Score', 'rvis__rvis_evs', tabName)
			addInfoLine(div, row, 'RVIS Percentile Rank', 'rvis__rvis_perc_evs', tabName)
			addInfoLine(div, row, 'ExAC-based RVIS', 'rvis__rvis_exac', tabName)
			addInfoLine(div, row, 'ExAC-based RVIS Percentile Rank', 'rvis__rvis_perc_exac', tabName)
			addInfoLine(div, row, 'FDR p-value', 'rvis__rvis_fdr_exac', tabName)
		}
	}
}