widgetGenerators['biogrid'] = {
	'gene': {
		'width': 250, 
		'height': 250, 
		'function': function (div, row, tabName) {
			var id = infomgr.getRowValue(tabName, row, 'biogrid__id');
			var hugo = infomgr.getRowValue(tabName, row, 'base__hugo');
			var head = hugo+' BioGRID'
			var link = '';
			if(id != null){
				link = 'https://thebiogrid.org/'+id;
			}
			else{
				id = '';
			}
			addInfoLineLink(div, head, id, link);
			var acts = infomgr.getRowValue(tabName, row, 'biogrid__acts');
			var actsls = acts != null ? acts.split(';') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Interactors']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var j=0;j<actsls.length;j++){
				var tr = getWidgetTableTr([actsls[j]]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}
