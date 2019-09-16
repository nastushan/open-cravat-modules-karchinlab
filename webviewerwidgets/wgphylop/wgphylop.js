widgetGenerators['phylop'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Vertebrate Score', 'phylop__phylop100_vert', tabName);
			addInfoLine(div, row, 'Vertebrate Ranked Score', 'phylop__phylop100_vert_r', tabName);
			addInfoLine(div, row, 'Mammalian Score', 'phylop__phylop20_mamm', tabName);
			addInfoLine(div, row, 'Mammalian Ranked Score', 'phylop__phylop20_mamm_r', tabName);
		}
	}
}