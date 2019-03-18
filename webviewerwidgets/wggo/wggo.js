widgetGenerators['go'] = {
	'gene': {
		'width': 450, 
		'height': 200, 
		'word-break':'normal',
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Gene Name', 'go__dname', tabName, 66)
			var goid = infomgr.getRowValue(tabName, row, 'go__id');
			var idls = goid != null ? goid.split(';') : [];
			var goname = infomgr.getRowValue(tabName, row, 'go__name');
			var namels = goname != null ? goname.split(';') : [];
			var ontol = infomgr.getRowValue(tabName, row, 'go__aspect');
			var ontolls = ontol != null ? ontol.split(';') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['ID', 'GO Name', 'Aspect']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			var inTable = [];
			for (var i =0; i<idls.length;i++){
				var iditr = idls[i];
				var nameitr = namels[i];
				var ontolitr = ontolls[i];
				var link = 'http://amigo.geneontology.org/amigo/term/'+iditr;
				if(!inTable.includes(iditr)){
					var tr = getWidgetTableTr([link, nameitr, ontolitr],[iditr]);
					addEl(tbody, tr);
					inTable.push(iditr);
				}
			}
			addEl(div, addEl(table, tbody));
		}
	}
}