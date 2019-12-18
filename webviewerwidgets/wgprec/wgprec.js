widgetGenerators['prec'] = {
	'gene': {
		'width': 212, 
		'height': 100, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addGradientBarComponent(div, row, 'P(rec)', 'prec__prec', tabName, {'0.0':[255,255,255], '0.5':[255,255,0], '1.0':[255,0,0]});
			addInfoLine(div, 'Known Recessive Status', getWidgetData(tabName, 'prec', row, 'stat'), tabName);
		}
	}
}
