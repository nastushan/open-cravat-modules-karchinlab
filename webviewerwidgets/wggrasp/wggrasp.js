widgetGenerators['grasp'] = {
	'variant': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Pval', 'Phenotype','NHLBI', 'PubMed']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);

			var nhlbiStr = infomgr.getRowValue(tabName, row, 'grasp__nhlbi');
			var nhlbis = nhlbiStr != null ? nhlbiStr.split('|') : [];
			var pmidStr = infomgr.getRowValue(tabName, row, 'grasp__pmid');
			var pmids = pmidStr != null ? pmidStr.split('|') : [];
			var phenoValStr = infomgr.getRowValue(tabName, row, 'grasp__phenotype');
			var phenoVals = phenoValStr != null ? phenoValStr.split('|') : [];
			
			var re = /(.*)\((.*)\)/
			for (var i = 0; i < phenoVals.length; i++) {
				var phenoVal = phenoVals[i];
				var match = re.exec(phenoVal);
				if (match !== null) {
					var pheno = match[1];
					var pval = match[2];
					var nhlbi = nhlbis[i];
					var pmid = pmids[i];
					var tr = getWidgetTableTr([pval, pheno, nhlbi, pmid], ['40px', '70px', '70px', '60px']);
					addEl(tbody, tr);
				}
			}
		}
	}
}