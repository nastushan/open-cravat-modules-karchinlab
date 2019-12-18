widgetGenerators['phylop'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Vertebrate Score', getWidgetData(tabName, 'phylop', row, 'phylop100_vert'), tabName);
			addInfoLine(div, 'Vertebrate Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop100_vert_r'), tabName);
			addInfoLine(div, 'Mammalian Score', getWidgetData(tabName, 'phylop', row, 'phylop20_mamm'), tabName);
			addInfoLine(div, 'Mammalian Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop20_mamm_r'), tabName);
		}
	}
}
