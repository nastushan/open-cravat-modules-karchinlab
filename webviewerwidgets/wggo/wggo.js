widgetGenerators['go'] = {
	'gene': {
		'width': 450, 
		'height': 200, 
		'function': function (div, row, tabName) {
			var go_name = infomgr.getRowValue(tabName, row, 'go__name');
			var name_ls = go_name != null ? go_name.split(';') : [];
			var goid = infomgr.getRowValue(tabName, row, 'go__id');
			var idls = goid != null ? goid.split(';') : [];
			var ontol = infomgr.getRowValue(tabName, row, 'go__aspect');
			var ontolls = ontol != null ? ontol.split(';') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Term', 'ID', 'Ontology']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var i =0; i<name_ls.length;i++){
				var nameitr = name_ls[i];
				var iditr = idls[i];
				var ontolitr = ontolls[i];
				var tr = getWidgetTableTr([nameitr, iditr, ontolitr]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}