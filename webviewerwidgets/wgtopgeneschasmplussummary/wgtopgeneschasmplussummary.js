widgetGenerators['topgeneschasmplussummary'] = {
	'info': {
		'name': 'Top Genes by CHASMplus',
		'width': 280, 
		'height': 220, 
		'callserver': false,
        'variables': {},
        'init': function () {
			var extracted = [];
            var pvalCutoff = 0.08;
			var geneRows = infomgr.getData('gene');
			for (var i = 0; i < geneRows.length; i++) {
				var row = geneRows[i];
				var hugo = infomgr.getRowValue('gene', row, 'base__hugo');
				var pval = infomgr.getRowValue('gene', row, 'chasmplus__gene_pval');
				if (pval == undefined) {
					continue;
				}
                if (pval <= pvalCutoff) {
                    extracted.push([hugo, pval]);
                }
			}
			var numGeneToExtract = 10;
            for (var i = 0; i < extracted.length - 1; i++) {
                for (var j = i + 1; j < extracted.length; j++) {
                    if (extracted[j][1] < extracted[i][1]) {
                        var tmp = extracted[i];
                        extracted[i] = extracted[j];
                        extracted[j] = tmp;
                    }
                }
            }
            if (extracted.length > numGeneToExtract) {
                extracted.splice(numGeneToExtract, extracted.length - numGeneToExtract);
            }
            this['variables']['extracted'] = extracted;
        },
        'shoulddraw': function () {
            if (this['variables']['extracted'].length == 0) {
                return false;
            } else {
                return true;
            }
        },
		'function': function (div) {
			if (div != null) {
				emptyElement(div);
			}
            var extracted = this['variables']['extracted'];
			var table = getEl('table');
			table.style.fontSize = '13px';
			table.style.borderCollapse = 'collapse';
			var thead = getEl('thead');
			var tr = getEl('tr');
			tr.style.borderBottom = '1px solid black';
			addEl(tr, addEl(getEl('th'), getTn('Gene')));
			addEl(tr, addEl(getEl('th'), getTn('CHASM Composite p-value')));
			addEl(table, addEl(thead, tr));
			var tbody = getEl('tbody');
			for (var i = 0; i < extracted.length; i++) {
				var row = extracted[i];;
				var tr = getEl('tr');
				var td = getEl('td');
				td.style.borderRight = '1px solid black';
                var hugo = row[0];
                if (hugo == '') {
                    continue;
                }
				addEl(tr, addEl(td, getTn(hugo)));
				addEl(tr, addEl(getEl('td'), getTn(row[1])));
				addEl(tbody, tr);
			}
			addEl(table, tbody);
			addEl(div, table);
		}
	}
};
