widgetGenerators['base'] = {
	'variant': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'UID', 'base__uid', tabName);
			if (infomgr.getColumnNo('variant', 'base__hugo')) {
				addInfoLine(div, row, 'Gene', 'base__hugo', tabName);
			}
			addInfoLine(div, row, 'Chromosome', 'base__chrom', tabName);
			addInfoLine(div, row, 'Position', 'base__pos', tabName);
			addInfoLine(div, row, 'Ref base(s)', 'base__ref_base', tabName);
			addInfoLine(div, row, 'Alt base(s)', 'base__alt_base', tabName);
			if (infomgr.getColumnNo('variant', 'base__sample_id')) {
				addInfoLine(div, row, 'Sample', 'base__sample_id', tabName);
			}
			if (infomgr.getColumnNo('variant', 'base__hugo')) {
				var allMappings = JSON.parse(infomgr.getRowValue(tabName, row, 'base__all_mappings'));
				if (allMappings != {}) {
					var table = getWidgetTableFrame();
					var thead = getWidgetTableHead(['UniProt', 'Prot Chng', 
						'Seq Ont', 'Transcript']);
					addEl(table, thead);
					var tbody = getEl('tbody');
					var hugos = Object.keys(allMappings);
					for (var i = 0; i < hugos.length; i++) {
						var hugo = hugos[i];
						var uniprot_ds = allMappings[hugo];
						for (var j = 0; j < uniprot_ds.length; j++) {
							var uniprot_d = uniprot_ds[j];
							var uniprot = uniprot_d[0];
							var aachange = uniprot_d[1];
							var so = uniprot_d[2];
							var transcript = uniprot_d[3];
							var tr = getWidgetTableTr(
								[uniprot, aachange, so, transcript], 
								[40, 40, 40, 80]);
							addEl(tbody, tr);
						}
					}
					addEl(div, addEl(table, tbody));
				}
			}
		}
	},
	'gene': {
		'width': 280,
		'height': 280,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Gene', 'base__hugo', tabName);
			addInfoLine(div, row, '# Variants', 'base__num_variants', tabName);
			addInfoLine(div, row, 'Most Severe Seq Ont', 'base__so', tabName);
			var allMappings = infomgr.getRowValue(tabName, row, 'base__all_so');
			if (allMappings != null && allMappings != '') {
				allMappings = allMappings.split(',');
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Seq On', '# transcript']);
				addEl(table, thead);
				var tbody = getEl('tbody');
				for (var i = 0; i < allMappings.length; i++) {
					var mapping = allMappings[i];
					var toks = mapping.split('(');
					var so = toks[0];
					var numTranscript = toks[1].split(')')[0];
					var tr = getWidgetTableTr([so, numTranscript]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}