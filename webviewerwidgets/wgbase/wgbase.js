widgetGenerators['base'] = {
	'variant': {
		'width': 480, 
		'height': 200, 
		'function': function (div, row, tabName) {
            var uid = getWidgetData(tabName, 'base', row, 'uid');
            if (uid != null && uid != '') {
                addInfoLine(div, 'UID', uid, tabName);
            }
            var hugo = getWidgetData(tabName, 'base', row, 'hugo');
            if (hugo != null) {
                addInfoLine(div, 'Gene', hugo, tabName);
            }
            addInfoLine(div, 'Chrom', getWidgetData(tabName, 'base', row, 'chrom'), tabName);
            addInfoLine(div, 'Position', getWidgetData(tabName, 'base', row, 'pos'), tabName);
            addInfoLine(div, 'Ref base(s)', getWidgetData(tabName, 'base', row, 'ref_base'), tabName);
            addInfoLine(div, 'Alt base(s)', getWidgetData(tabName, 'base', row, 'alt_base'), tabName);
            var sample = getWidgetData(tabName, 'base', row, 'sample_id');
            if (sample != null) {
                addInfoLine(div, 'Sample', sample, tabName);
            }
            var snp = row['snp'];
            if (snp != undefined) {
                var link = '';
                if(snp != null){
                    link = 'http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=' + snp;
                }
                else{
                    snp = '';
                }
                addInfoLineLink(div, 'dbSNP', snp, link, 30);
            }
            var allMappings = null;
            allMappings = getWidgetData(tabName, 'base', row, 'all_mappings');
            allMappings = JSON.parse(allMappings);
            if (hugo != null) {
				if (allMappings != {}) {
					var table = getWidgetTableFrame();
                    table.style.tableLayout = 'auto';
					table.style.width = '100%';
					var thead = getWidgetTableHead(['Gene', 'UniProt', 'Prot Chng', 
						'Seq Ont', 'Transcript'], ['10%', '15%', '18%', '33%', '24%']);
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
                            so = uniprot_d[2].split(',').join(', ');
							var transcript = uniprot_d[3];
							var tr = getWidgetTableTr([hugo, uniprot, aachange, so, transcript]);
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
		'height': 200,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Gene', 'base__hugo', tabName);
			addInfoLine(div, row, '# Coding Variants', 'base__num_coding_variants', tabName);
			addInfoLine(div, row, '# Non-coding Variants', 'base__num_noncoding_variants', tabName);
			addInfoLine(div, row, 'Most Severe Seq Ont', 'base__so', tabName);
            var allMappings = getWidgetData(tabName, 'base', row, 'all_so');
			if (allMappings != null && allMappings != '') {
				allMappings = allMappings.split(',');
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Seq On', '# transcript']);
				addEl(table, thead);
				var tbody = getEl('tbody');
				for (var i = 0; i < allMappings.length; i++) {
					var mapping = allMappings[i];
					var toks = mapping.split('(');
                    so = toks[0].split(',').join(', ');
					var numTranscript = toks[1].split(')')[0];
					var tr = getWidgetTableTr([so, numTranscript]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}
