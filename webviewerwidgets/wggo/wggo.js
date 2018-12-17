widgetGenerators['go'] = {
	'gene': {
		'width': 450, 
		'height': 200, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Gene Name', 'go__name', tabName)
			var goid = infomgr.getRowValue(tabName, row, 'go__id');
			var idls = goid != null ? goid.split(';') : [];
			var ontol = infomgr.getRowValue(tabName, row, 'go__aspect');
			var ontolls = ontol != null ? ontol.split(';') : [];
			var ref = infomgr.getRowValue(tabName, row, 'go__refer');
			var refls = ontol != null ? ref.split(';') : [];
			var evi = infomgr.getRowValue(tabName, row, 'go__evi');
			var evils = ontol != null ? evi.split(';') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['ID', 'Aspect', 'Reference', 'Evidence Code']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var i =0; i<idls.length;i++){
				var iditr = idls[i];
				var ontolitr = ontolls[i];
				var refitr = refls[i];
				var eviitr = evils[i];
				var tr = getWidgetTableTr([iditr, ontolitr, refitr, eviitr]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}