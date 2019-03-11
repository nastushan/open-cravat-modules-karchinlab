widgetGenerators['gtex'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			var genes = infomgr.getRowValue(tabName, row, 'gtex__gtex_gene');
			var genels = genes != null ? genes.split('|') : [];
			var tissues = infomgr.getRowValue(tabName, row, 'gtex__gtex_tissue');
			var tissuels = tissues != null ? tissues.split('|') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Target Gene', 'Tissue Type']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var i =0; i<genels.length;i++){
				var geneitr = genels[i];
				var tissueitr = tissuels[i];
				tissueitr = tissueitr.replace("_", " ")
				var ensLink = 'https://ensembl.org/Homo_sapiens/Gene/Summary?g='+geneitr;
				var tr = getWidgetTableTr([ensLink, tissueitr],[geneitr]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}
