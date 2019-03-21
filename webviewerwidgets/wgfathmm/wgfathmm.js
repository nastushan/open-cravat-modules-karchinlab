widgetGenerators['fathmm'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'FATHMM Converted Rank Score', 'fathmm__fathmm_rscore', tabName);
			var tid = infomgr.getRowValue(tabName, row, 'fathmm__ens_tid');
			var tidls = tid != null ? tid.split(';') : [];
			var pid = infomgr.getRowValue(tabName, row, 'fathmm__ens_pid');
			var pidls = pid != null ? pid.split(';') : [];
			var score = infomgr.getRowValue(tabName, row, 'fathmm__fathmm_score');
			var scorels = score != null ? score.split(';') : [];
			for (var i=0;i<scorels.length;i++){
				if (scorels[i] == '.'){
					scorels[i] = null;
				}
			}
			var pred = infomgr.getRowValue(tabName, row, 'fathmm__fathmm_pred');
			var predls = pred != null ? pred.split(';') : [];
			for(var i=0;i<predls.length;i++){
				if(predls[i] == '.'){
					predls[i] = null;
				}
			}
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Ensembl Transcript ID', 'Ensembl Protein ID', 'FATHMM Score', 'FATHMM Prediction']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var i =0; i<tidls.length;i++){
				var tiditr = tidls[i];
				var piditr = pidls[i];
				var sitr = scorels[i];
				var pitr = predls[i];
				var tr = getWidgetTableTr([tiditr, piditr, sitr, pitr]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}