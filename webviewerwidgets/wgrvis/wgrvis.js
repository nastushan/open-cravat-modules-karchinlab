widgetGenerators['rvis'] = {
	'gene': {
		'width': 280, 
		'height': 140, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Residual Variation Intolerance Score', getWidgetData(tabName, 'rvis', row, 'rvis_evs'), tabName)
			addInfoLine(div, 'RVIS Percentile Rank', getWidgetData(tabName, 'rvis', row, 'rvis_perc_evs'), tabName)
			addInfoLine(div, 'ExAC-based RVIS', getWidgetData(tabName, 'rvis', row, 'rvis_exac'), tabName)
			addInfoLine(div, 'ExAC-based RVIS Percentile Rank', getWidgetData(tabName, 'rvis', row, 'rvis_perc_exac'), tabName)
			addInfoLine(div, 'FDR p-value', getWidgetData(tabName, 'rvis', row, 'rvis_fdr_exac'), tabName)
		}
	}
}
