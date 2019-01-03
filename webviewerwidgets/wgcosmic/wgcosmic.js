widgetGenerators['cosmic'] = {
	'variant': {
		'width': 280, 
		'height': 220, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'ID', 'cosmic__cosmic_id', tabName, 4);
			addInfoLine(div, row, 'Variant Count', 'cosmic__variant_count', tabName);
			addInfoLine(div, row, 'Transcript', 'cosmic__transcript', tabName);
			addInfoLine(div, row, 'Protein Change', 'cosmic__protein_change', tabName);
			var vcTissue = infomgr.getRowValue(tabName, row, 'cosmic__variant_count_tissue');
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
						var tr = getWidgetTableTr([tissue, count]);
						addEl(tbody, tr);
					}
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}