widgetGenerators['siphy'] = {
	'variant': {
		'width': 152, 
		'height': 210, 
		'word-break': 'normal',
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Score', 'siphy__logodds', tabName, 25);
			addGradientBarComponent(div, row, 'Rank Score', 'siphy__logodds_rank', tabName);
			var pis = infomgr.getRowValue(tabName, row, 'siphy__pi');
			var pils = pis != null ? pis.split(';') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Nucleobase', 'Stationary Distribution']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			var bases = ['A', 'C', 'G', 'T']
			for (var i =0; i<pils.length;i++){
				var pi = pils[i]
				var base = bases[i]
				var tr = getWidgetTableTr([base, pi]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}