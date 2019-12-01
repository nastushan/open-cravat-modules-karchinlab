widgetGenerators['polyphen2'] = {
	'variant': {
		'width': 480, 
		'height': 180, 
		'default_hidden': false,
		'function': function (div, row, tabName) {
			let predMap = {
				'D': 'Probably damaging',
				'P': 'Possibly damaging',
				'B': 'Benign',
			}
			addInfoLine(div, row, 'HDIV Rank Score', 'polyphen2__hdiv_rank', tabName);
			addInfoLine(div, row, 'HVAR Rank Score', 'polyphen2__hvar_rank', tabName);
			let string_vals = {}
			string_vals.uniprot = infomgr.getRowValue(tabName, row, 'polyphen2__uniprot');
			string_vals.hdiv_score = infomgr.getRowValue(tabName, row, 'polyphen2__hdiv_score');
			string_vals.hvar_score = infomgr.getRowValue(tabName, row, 'polyphen2__hvar_score');
			string_vals.hdiv_pred = infomgr.getRowValue(tabName, row, 'polyphen2__hdiv_pred');
			string_vals.hvar_pred = infomgr.getRowValue(tabName, row, 'polyphen2__hvar_pred');
			if (string_vals.uniprot === null) return;
			let list_vals = {};
			for (let [n, sv] of Object.entries(string_vals)) {
				list_vals[n] = sv.split(';');
			}
			console.log(list_vals);
			let entries = [];
			for (let i=0; i<list_vals.uniprot.length; i++) {
				var entry = {}
				for (let [n,l] of Object.entries(list_vals)) {
					entry[n] = l[i];
				}
				entries.push(entry);
			}
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Uniprot', 'HDIV Score','HDIV Prediction','HVAR Score','HVAR Prediction'],['16%','16%','26%','16%','26%']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (let entry of entries) {
				var tr = getWidgetTableTr([entry.uniprot, entry.hdiv_score, predMap[entry.hdiv_pred], entry.hvar_score, predMap[entry.hvar_pred]]);
				addEl(tbody, tr);
			}
		}
	}
}