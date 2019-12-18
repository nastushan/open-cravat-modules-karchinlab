widgetGenerators['intact'] = {
	'gene': {
		'width': 162, 
		'height': 250, 
		'function': function (div, row, tabName) {
			var value = getWidgetData(tabName, 'intact', row, 'acts');
			if (value == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			var hugo = getWidgetData(tabName, 'base', row, 'hugo');
			if (hugo) {
				var a = getEl('a');
				a.text = hugo+' IntAct';
				a.href = 'https://www.ebi.ac.uk/intact/query/geneName:'+hugo;
				addEl(div, a);
				addEl(div, getEl('br'));
			}
			var acts = getWidgetData(tabName, 'intact', row, 'acts');
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
