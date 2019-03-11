widgetGenerators['loftool'] = {
	'gene': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			if(typeof addGradientBarComponent == 'function'){
				addGradientBarComponent(div, row, 'LoF Score', 'loftool__loftool_score', tabName, {'0.0':[255,0,0], '0.5':[255,255,0], '1.0':[0,255,0]})
			}
			else{
				addInfoLine(div, row, 'LoF Score', 'loftool__loftool_score', tabName)
			}
		}
	}
}
