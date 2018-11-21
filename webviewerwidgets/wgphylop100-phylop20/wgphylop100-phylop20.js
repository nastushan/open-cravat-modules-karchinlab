widgetGenerators['phylop100-phylop20'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Phylo P 100 Way Vertebrate Score', 'phylop100-phylop20__phylop100_vert', tabName);
			addInfoLine(div, row, 'Phylo P 100 Way Vertebrate Ranked Score', 'phylop100-phylop20__phylop100_vert_r', tabName);
			addInfoLine(div, row, 'Phylo P 20 Way Mammalian Score', 'phylop100-phylop20__phylop20_mamm', tabName);
			addInfoLine(div, row, 'Phylo P 20 Way Mammalian Ranked Score', 'phylop100-phylop20__phylop20_mamm_r', tabName);
		}
	}
}