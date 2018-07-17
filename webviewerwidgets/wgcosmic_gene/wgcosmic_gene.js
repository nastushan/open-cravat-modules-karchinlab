widgetGenerators['cosmic_gene'] = {
	'gene': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Variant Count', 'cosmic_gene__occurrences', tabName);
			var vcTissue = infomgr.getRowValue(tabName, row, 'cosmic_gene__gene_count');
			if (vcTissue !== null) {
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Tissue', 'Count']);
				addEl(table, thead);
				var tbody = getEl('tbody');
				var toks = vcTissue.split(';');
				var re = /(.*)\((.*)\)/
				for (var i = 0; i < toks.length; i++) {
					var tok = toks[i];
					var match = re.exec(tok);
					if (match !== null) {
						var tissue = match[1];
						var count = match[2];
						var tr = getWidgetTableTr([tissue, count], [150, 90]);
						addEl(tbody, tr);
					}
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}