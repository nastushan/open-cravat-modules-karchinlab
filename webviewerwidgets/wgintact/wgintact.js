widgetGenerators['intact'] = {
	'gene': {
		'width': 250, 
		'height': 250, 
		'function': function (div, row, tabName) {
			var acts = infomgr.getRowValue(tabName, row, 'intact__intact');
			var actsls = acts != null ? acts.split('|') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Gene Interaction', 'PubMed Link']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var j=0;j<actsls.length-1;j++){
				var gene = actsls[j].slice(0, actsls[j].indexOf('['));
				var pubid = actsls[j].slice(actsls[j].indexOf('[')+1,actsls[j].indexOf(']'));
				var pubidls = pubid.split(';');
				for(var i=0;i<pubidls.length;i++){
					var link = '';
					if (!pubidls[i].startsWith('unassigned')){
						link = 'https://www.ncbi.nlm.nih.gov/pubmed/'+pubidls[i];
					}
					else{
						link = pubidls[i];
					}
					var tr = getWidgetTableTr([gene, link]);
					addEl(tbody, tr);
				}
			addEl(div, addEl(table, tbody));
			}
		}
	}
}
