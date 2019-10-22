widgetGenerators['haploreg_eur'] = {
	'variant': {
		'width': 380, 
		'height': 200, 
		'function': function (div, row, tabName) {
			if (infomgr.getColumnNo('variant', 'base__hugo')) {
				var snps = infomgr.getRowValue(tabName, row, 'haploreg_eur__snps').split(',');
				var r2s = infomgr.getRowValue(tabName, row, 'haploreg_eur__r2s').split(',').map(parseFloat);
				var dprimes = infomgr.getRowValue(tabName, row, 'haploreg_eur__dprimes').split(',').map(parseFloat);
				if (snps && r2s && dprimes) {
					var table = getWidgetTableFrame();
                    table.style.tableLayout = 'auto';
					table.style.width = '100%';
					var thead = getWidgetTableHead(['rsID', 'R\u00b2', 'D\''], ['50%', '25%', '25%']);
					addEl(table, thead);
					var tbody = getEl('tbody');
					for (var i=0; i<snps.length; i++) {
						var tr = getWidgetTableTr([snps[i], r2s[i], dprimes[i]]);
						addEl(tbody, tr);
					}
					addEl(div, addEl(table, tbody));
				}
			}
		}
	}
}
