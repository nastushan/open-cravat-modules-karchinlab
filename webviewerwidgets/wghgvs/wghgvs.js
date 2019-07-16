widgetGenerators['hgvs'] = {
	'variant': {
		'width': 380, 
		'height': 280, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Genomic', 'hgvs__genomic', tabName);
			addInfoLine(div, row, 'RNA', 'hgvs__rna', tabName);
			addInfoLine(div, row, 'Protein', 'hgvs__protein', tabName);
			var rnaStr = infomgr.getRowValue(tabName, row, 'hgvs__all_rna');
			var rnaAll = rnaStr != null ? rnaStr.split(',') : [];
			var protStr = infomgr.getRowValue(tabName, row, 'hgvs__all_protein');
			var protAll = protStr != null ? protStr.split(',') : [];
			var prot2Hgvs = {}
			for (var i=0; i<protAll.length; i++) {
				var prot = protAll[i];
				var acc = prot.split(':')[0]
				prot2Hgvs[acc] = prot;
			}
			var allMappings = JSON.parse(infomgr.getRowValue(tabName, row, 'base__all_mappings'));
			var transc2Prot = {};
			for (var gene in allMappings) {
				var tlist = allMappings[gene];
				for (var i=0; i<tlist.length; i++) {
						var transc = tlist[i][3];
						var prot = tlist[i][0];
						transc2Prot[transc] = prot;
				}
			}
			if (rnaAll.length > 0) {
				var table = getWidgetTableFrame();
				addEl(div, table);
				var thead = getWidgetTableHead(['RNA', 'Protein'],['55%','45%']);
				addEl(table, thead);
				var tbody = getEl('tbody');
				addEl(table, tbody);
				for (var i = 0; i < rnaAll.length; i++) {
					var rna = rnaAll[i];
					var transc = rna.split(':')[0];
					var prot = prot2Hgvs[transc2Prot[transc]];
					var tr = getWidgetTableTr([rna, prot]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}