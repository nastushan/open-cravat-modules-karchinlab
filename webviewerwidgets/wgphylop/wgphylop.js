widgetGenerators['phylop'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Phylo P 100 Way Vertebrate Score', 'phylop__phylop100_vert', tabName);
			addInfoLine(div, row, 'Phylo P 100 Way Vertebrate Ranked Score', 'phylop__phylop100_vert_r', tabName);
			addInfoLine(div, row, 'Phylo P 20 Way Mammalian Score', 'phylop__phylop20_mamm', tabName);
			addInfoLine(div, row, 'Phylo P 20 Way Mammalian Ranked Score', 'phylop__phylop20_mamm_r', tabName);
		}
	}
}