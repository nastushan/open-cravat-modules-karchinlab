widgetGenerators['cgc'] = {
	'gene': {
		'width': 280, 
		'height': 180, 
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Class', getWidgetData(tabName, 'cgc', row, 'class'), tabName);
			addInfoLine(div, 'Inheritance', getWidgetData(tabName, 'cgc', row, 'inheritance'), tabName);
			addInfoLine(div, 'Somatic Types', getWidgetData(tabName, 'cgc', row, 'tts'), tabName);
			addInfoLine(div, 'Genomic Types', getWidgetData(tabName, 'cgc', row, 'ttg'), tabName);
		}
	}
}
