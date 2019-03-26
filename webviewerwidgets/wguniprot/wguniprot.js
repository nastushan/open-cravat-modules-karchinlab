widgetGenerators['uniprot'] = {
	'gene': {
		'width': 185, 
		'height': 120, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			var accs = infomgr.getRowValue(tabName, row, 'uniprot__acc');
			var accsls = accs != null ? accs.split(';') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Acc Number', 'Hyperlink']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var j=0;j<accsls.length;j++){
				var link = 'https://www.uniprot.org/uniprot/'+accsls[j];
				var tr = getWidgetTableTr([accsls[j], link]);
				addEl(tbody, tr);
			addEl(div, addEl(table, tbody));
			}
		}
	}
}
