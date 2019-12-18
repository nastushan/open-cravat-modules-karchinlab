widgetGenerators['mutation_assessor'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			var value = getWidgetData(tabName, 'mutation_assessor', row, 'mut_var');
			if (value == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			addInfoLine(div, 'Mutation Variant', getWidgetData(tabName, 'mutation_assessor', row, 'mut_var'), tabName);
			addInfoLine(div, 'Mutation Score', getWidgetData(tabName, 'mutation_assessor', row, 'mut_score'), tabName);
			addInfoLine(div, 'Mutation Rank Score', getWidgetData(tabName, 'mutation_assessor', row, 'mut_rscore'), tabName);
			addInfoLine(div, 'Mutation Functional Impact', getWidgetData(tabName, 'mutation_assessor', row, 'mut_pred'), tabName);
		}
	}
}
