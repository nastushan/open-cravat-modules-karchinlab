widgetGenerators['intact'] = {
	'gene': {
		'width': 162, 
		'height': 250, 
		'function': function (div, row, tabName) {
			var hugo = infomgr.getRowValue(tabName, row, 'base__hugo');
			var head = hugo+' IntAct';
			var link = 'https://www.ebi.ac.uk/intact/query/geneName:'+hugo;
			addInfoLineLink(div, head, 'Link', link);
			var acts = infomgr.getRowValue(tabName, row, 'intact__acts');
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
