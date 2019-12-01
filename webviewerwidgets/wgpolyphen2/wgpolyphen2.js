widgetGenerators['polyphen2'] = {
	'variant': {
		'width': 380, 
		'height': 180, 
		'default_hidden': false,
		'function': function (div, row, tabName) {
			console.log('polyphen2');
			addInfoLine(div, row, 'HDIV Rank Score', 'polyphen2__hdiv_rank', tabName);
			addInfoLine(div, row, 'HVAR Rank Score', 'polyphen2__hvar_rank', tabName);
			var string_vals = {}
			string_vals.uniprot = infomgr.getRowValue(tabName, row, 'polyphen2__uniprot');
			string_vals.hdiv_score = infomgr.getRowValue(tabName, row, 'polyphen2__hdiv_score');
			string_vals.hvar_score = infomgr.getRowValue(tabName, row, 'polyphen2__hvar_score');
			string_vals.hdiv_pred = infomgr.getRowValue(tabName, row, 'polyphen2__hdiv_pred');
			string_vals.hvar_pred = infomgr.getRowValue(tabName, row, 'polyphen2__hvar_pred');
			if (string_vals.uniprot === null) return;
			var list_vals = {};
			for (var [n, sv] of Object.entries(string_vals)) {
				list_vals[n] = sv.split(';');
			}
			console.log(list_vals);
			var entries = [];
			for (var [n, lv] of Object.entries(list_vals.entries)) {
				var entry = []
				for (var v of lv) {
					entry[n] = v;
				}
				entries.push(entry);
			}
			for (var entry of entries) {
				console.log(entry);
			}
			// var codAll = codStr != null ? codStr.split(',') : [];
			// var protStr = infomgr.getRowValue(tabName, row, 'hgvs__all_protein');
			// var protAll = protStr != null ? protStr.split(',') : [];
			// var prot2Hgvs = {}
			// for (var i=0; i<protAll.length; i++) {
			// 	var prot = protAll[i];
			// 	var acc = prot.split(':')[0]
			// 	prot2Hgvs[acc] = prot;
			// }
			// var allMappings = JSON.parse(infomgr.getRowValue(tabName, row, 'base__all_mappings'));
			// var transc2Prot = {};
			// for (var gene in allMappings) {
			// 	var tlist = allMappings[gene];
			// 	for (var i=0; i<tlist.length; i++) {
			// 			var transc = tlist[i][3];
			// 			var prot = tlist[i][0];
			// 			transc2Prot[transc] = prot;
			// 	}
			// }
			// if (codAll.length > 0) {
			// 	var table = getWidgetTableFrame();
			// 	addEl(div, table);
			// 	var thead = getWidgetTableHead(['Coding', 'Protein'],['55%','45%']);
			// 	addEl(table, thead);
			// 	var tbody = getEl('tbody');
			// 	addEl(table, tbody);
			// 	for (var i = 0; i < codAll.length; i++) {
			// 		var cod = codAll[i];
			// 		var transc = cod.split(':')[0];
			// 		var prot = prot2Hgvs[transc2Prot[transc]];
			// 		var tr = getWidgetTableTr([cod, prot]);
			// 		addEl(tbody, tr);
			// 	}
			// 	addEl(div, addEl(table, tbody));
			// }
		}
	}
}