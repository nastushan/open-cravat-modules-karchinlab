widgetGenerators['prec'] = {
	'gene': {
		'width': 280, 
		'height': 100, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Known Recessive Status', 'prec__stat', tabName);
			addGradientBarComponent(div, row, 'P(rec)', 'prec__prec', tabName, {'0.0':[255,255,255], '0.5':[255,255,0], '1.0':[255,0,0]});
		}
	}
}