widgetGenerators['cgc'] = {
	'gene': {
		'width': 280, 
		'height': 180, 
		'word-break':'normal',
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Class', 'cgc__class', tabName);
			addInfoLine(div, row, 'Inheritance', 'cgc__inheritance', tabName);
			addInfoLine(div, row, 'Somatic Types', 'cgc__tts', tabName);
			addInfoLine(div, row, 'Genomic Types', 'cgc__ttg', tabName);
		}
	}
}