widgetGenerators['phastcons'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'phastCons 100 Way Vertebrate Score', 'phastcons__phastcons100_vert', tabName);
			addInfoLine(div, row, 'phastCons 100 Way Vertebrate Ranked Score', 'phastcons__phastcons100_vert_r', tabName);
			addInfoLine(div, row, 'phastCons 20 Way Mammalian Score', 'phastcons__phastcons20_mamm', tabName);
			addInfoLine(div, row, 'phastCons 20 Way Mammalian Ranked Score', 'phastcons__phastcons20_mamm_r', tabName);
		}
	}
}