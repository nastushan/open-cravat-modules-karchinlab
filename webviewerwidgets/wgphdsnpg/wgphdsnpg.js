widgetGenerators['phdsnpg'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			var value = getWidgetData(tabName, 'phdsnpg', row, 'prediction');
			if (value == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			addInfoLine(div, 'Prediction', getWidgetData(tabName, 'phdsnpg', row, 'prediction'), tabName);
			addBarComponent(div, row, 'Score', 'phdsnpg__score', tabName);
			addBarComponent(div, row, 'FDR', 'phdsnpg__fdr', tabName);
		}
	}
}
