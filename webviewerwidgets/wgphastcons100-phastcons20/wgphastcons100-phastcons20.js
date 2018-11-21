widgetGenerators['phastcons100-phastcons20'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Phast Cons 100 Way Vertebrate Score', 'phastcons100-phastcons20__phastcons100_vert', tabName);
			addInfoLine(div, row, 'Phast Cons 100 Way Vertebrate Ranked Score', 'phastcons100-phastcons20__phastcons100_vert_r', tabName);
			addInfoLine(div, row, 'Phast Cons 20 Way Mammalian Score', 'phastcons100-phastcons20__phastcons20_mamm', tabName);
			addInfoLine(div, row, 'Phast Cons 20 Way Mammalian Ranked Score', 'phastcons100-phastcons20__phastcons20_mamm_r', tabName);
		}
	}
}