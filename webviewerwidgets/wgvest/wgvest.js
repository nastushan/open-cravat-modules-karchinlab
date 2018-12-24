widgetGenerators['vest'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'function': function (div, row, tabName) {
			if(typeof addGradientBarComponent == 'function'){
				addGradientBarComponent(div, row, 'VEST p-value', 'vest__pval', tabName, colors={'0.0':[255,0,0],'0.05':[255,230,230],'1.0':[255,255,255]});
			}
			else{
				addBarComponent(div, row, 'VEST p-value', 'vest__pval', tabName);
			}
			var allMappings = infomgr.getRowValue(tabName, row, 'vest__all_results');
			if (allMappings == null) {
				addEl(div, addEl(getEl('span'), getTn('N/A')));
			} else {
				allMappings = allMappings.split(',');
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Transcript', 'Score', 'P-value']);
				addEl(table, thead);
				var tbody = getEl('tbody');
				for (var i = 0; i < allMappings.length; i++) {
					var mapping = allMappings[i];
					var toks = mapping.split('(');
					var transcript = toks[0];
					var toks2 = toks[1].split(':');
					var score = parseFloat(toks2[0]).toFixed(3);
					var pvalue = parseFloat(toks2[1].split(')')[0]).toFixed(4);
					var tr = getWidgetTableTr([transcript, score, pvalue]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	},
	'gene': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Max score', 'vest__max_score', tabName);
			addInfoLine(div, row, 'Mean score', 'vest__mean_score', tabName);
			addInfoLine(div, row, 'Gene p-value', 'vest__gene_pval', tabName);
		}
	}
}
