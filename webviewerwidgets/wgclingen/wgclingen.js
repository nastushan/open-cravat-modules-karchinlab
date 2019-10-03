widgetGenerators['clingen'] = {
	'gene': {
		'width': 380,
		'height': 200,
		'function': function (div, row, tabName) {
			if (infomgr.getRowValue(tabName, row, 'clingen__disease') !== null) {
				var diseases = infomgr.getRowValue(tabName, row, 'clingen__disease').split(';');
				var classifications = infomgr.getRowValue(tabName, row, 'clingen__classification').split(';');
				var links = infomgr.getRowValue(tabName, row, 'clingen__link').split(';');
				var mondos = infomgr.getRowValue(tabName, row, 'clingen__mondo').split(';');
				var table = getWidgetTableFrame();
				addEl(div, table);
				var thead = getWidgetTableHead(['Disease', 'Classification','ClinGen','Monarch'],[180,110,45,45]);
				addEl(table, thead);
				var tbody = getEl('tbody');
				addEl(table, tbody);
				for (var i = 0; i < diseases.length; i++) {
					var disease = diseases[i];
					var classification = classifications[i];
					var mondo = mondos[i];
					var mondo_link = `https://monarchinitiative.org/disease/${mondo}`
					var link = links[i]
					var tr = getWidgetTableTr([disease, classification, link, mondo_link]);
					addEl(tbody, tr);
				}
			}
		}
	}
}
