widgetGenerators['biogrid'] = {
	'gene': {
		'width': 192, 
		'height': 250, 
		'function': function (div, row, tabName) {
			var value = getWidgetData(tabName, 'biogrid', row, 'id');
			if (value == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
            var id = getWidgetData(tabName, 'biogrid', row, 'id');
            var hugo = getWidgetData(tabName, 'base', row, 'hugo');
            var acts = getWidgetData(tabName, 'biogrid', row, 'acts');
            var head = 'BioGRID';
            if (hugo != null) {
                var head = hugo+' BioGRID'
            }
			var link = '';
			if(id != null) {
				link = 'https://thebiogrid.org/'+id;
			}
			else {
				id = '';
			}
			addInfoLineLink(div, head, id, link);
			var actsls = acts != null ? acts.split(';') : [];
            if (actsls.length > 0) {
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
}
