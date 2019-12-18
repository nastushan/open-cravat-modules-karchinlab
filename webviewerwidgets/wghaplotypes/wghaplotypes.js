widgetGenerators['haplotypes'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'word-break': 'break-word',
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Chromosome', 'base__chrom', tabName);
			addInfoLine(div, row, 'Haplotype Block ID', 'vcfinfo__hap_block', tabName);
			if (infomgr.getColumnNo(tabName, 'vcfinfo__hap_block')) {
				var rowBlock = getWidgetData(tabName, 'vcfinfo', row, 'hap_block');
				if (rowBlock != null){
					var rowChrom = getWidgetData(tabName, 'base', row, 'chrom');
					var allRows = infomgr.datas.variant;
					var table = getWidgetTableFrame(['10%', '10%', '10%', '10%', '10%', "40%", '10%']);
					addEl(div, table);
					var thead = getWidgetTableHead(['Chromosome', 'Position', 'Reference Allele', 'Alternate Allele', 
													'Haplotype Strand', 'Transcript', 'Amino Acid Change']);
					addEl(table, thead);
					var tbody = getEl('tbody');
					addEl(table, tbody);
					for (var i=0; i<allRows.length; i++){
						var block = getWidgetData(tabName, 'vcfinfo', allRows[i], 'hap_block');
						var chrom = getWidgetData(tabName, 'base', allRows[i], 'chrom');
						if (rowBlock == block && rowChrom == chrom){
							var pos = getWidgetData(tabName, 'base', allRows[i], 'pos');
							var ref = getWidgetData(tabName, 'base', allRows[i], 'ref_base');
							var alt = getWidgetData(tabName, 'base', allRows[i], 'alt_base');
							var hapStrand = getWidgetData(tabName, 'vcfinfo', allRows[i], 'hap_strand');
							var transcript = getWidgetData(tabName, 'base', allRows[i], 'transcript');
							var aaChange = getWidgetData(tabName, 'base', allRows[i], 'achange');
							var tr = getWidgetTableTr([chrom, pos, ref, alt, hapStrand, transcript, aaChange]);
							addEl(tbody, tr);
						}
					}
					addEl(div, addEl(table, tbody));
				}
			}
		}
	}
}
