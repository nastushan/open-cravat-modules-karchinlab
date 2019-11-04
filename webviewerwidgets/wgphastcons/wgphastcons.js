widgetGenerators['phastcons'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Vertebrate Score', 'phastcons__phastcons100_vert', tabName);
			addInfoLine(div, row, 'Vertebrate Ranked Score', 'phastcons__phastcons100_vert_r', tabName);
			addInfoLine(div, row, 'Mammalian Score', 'phastcons__phastcons20_mamm', tabName);
			addInfoLine(div, row, 'Mammalian Ranked Score', 'phastcons__phastcons20_mamm_r', tabName);
		}
	}
}
