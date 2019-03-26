widgetGenerators['interpro'] = {
	'variant': {
		'width': 480, 
		'height': 140, 
		'word-break': 'normal',
		'function': function (div, row, tabName) {
			var acc = infomgr.getRowValue(tabName, row, 'interpro__uniprot_acc');
			var accls = acc != null ? acc.split(';') : [];
			var dom = infomgr.getRowValue(tabName, row, 'interpro__domain');
			var domls = dom != null ? dom.split(';') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['UniProt', 'Domain', 'Link'],['20%','70%','10%']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			var dups = [];
			for (var j=0;j<accls.length;j++){
				if(accls[j] !== '.' && domls[j] !== '.'){
					if(!dups.includes(accls[j]+domls[j])){
						var link = 'https://www.ebi.ac.uk/interpro/protein/'+accls[j];
						var tr = getWidgetTableTr([accls[j], domls[j], link]);
						addEl(tbody, tr);
						dups.push(accls[j]+domls[j]);
					}
				}
			}
			addEl(div, addEl(table, tbody));
		}
	}
}