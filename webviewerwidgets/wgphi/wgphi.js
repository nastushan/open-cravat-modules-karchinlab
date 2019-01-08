widgetGenerators['phi'] = {
	'gene': {
		'width': 182, 
		'height': 90, 
		'function': function (div, row, tabName) {
			addGradientBarComponent(div, row, 'P(HI)', 'phi__phi', tabName, {'0.0':[255,255,255], '0.5':[255,255,0], '1.0':[255,0,0]})
		}
	}
}