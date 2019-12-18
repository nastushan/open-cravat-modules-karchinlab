widgetGenerators['hgvs'] = {
	'variant': {
		'width': 380, 
		'height': 180, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Genomic', getWidgetData(tabName, 'hgvs', row, 'genomic'), tabName);
			addInfoLine(div, 'Coding', getWidgetData(tabName, 'hgvs', row, 'coding'), tabName);
			addInfoLine(div, 'Protein', getWidgetData(tabName, 'hgvs', row, 'protein'), tabName);
			var codStr = getWidgetData(tabName, 'hgvs', row, 'all_coding');
			var codAll = codStr != null ? codStr.split(',') : [];
			var protStr = getWidgetData(tabName, 'hgvs', row, 'all_protein');
			var protAll = protStr != null ? protStr.split(',') : [];
			var prot2Hgvs = {}
			for (var i=0; i<protAll.length; i++) {
				var prot = protAll[i];
				var acc = prot.split(':')[0]
				prot2Hgvs[acc] = prot;
			}
			var allMappings = JSON.parse(getWidgetData(tabName, 'base', row, 'all_mappings'));
			var transc2Prot = {};
			for (var gene in allMappings) {
				var tlist = allMappings[gene];
				for (var i=0; i<tlist.length; i++) {
						var transc = tlist[i][3];
						var prot = tlist[i][0];
						transc2Prot[transc] = prot;
				}
			}
			if (codAll.length > 0) {
				var table = getWidgetTableFrame();
				addEl(div, table);
				var thead = getWidgetTableHead(['Coding', 'Protein'],['55%','45%']);
				addEl(table, thead);
				var tbody = getEl('tbody');
				addEl(table, tbody);
				for (var i = 0; i < codAll.length; i++) {
					var cod = codAll[i];
					var transc = cod.split(':')[0];
					var prot = prot2Hgvs[transc2Prot[transc]];
					var tr = getWidgetTableTr([cod, prot]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}
