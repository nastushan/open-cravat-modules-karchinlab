widgetGenerators['haplotypes'] = {
	'variant': {
		'width': 280, 
		'height': 180, 
		'word-break': 'break-word',
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Chromosome', 'base__chrom', tabName);
			addInfoLine(div, row, 'Haplotype Block ID', 'vcfinfo__hap_block', tabName);
			if (infomgr.getColumnNo(tabName, 'vcfinfo__hap_block')) {
				var rowBlock = infomgr.getRowValue(tabName, row, 'vcfinfo__hap_block');
				if (rowBlock != null){
					var rowChrom = infomgr.getRowValue(tabName, row, 'base__chrom');
					var allRows = infomgr.datas.variant;
					var table = getWidgetTableFrame(['10%', '10%', '10%', '10%', '10%', "40%", '10%']);
					addEl(div, table);
					var thead = getWidgetTableHead(['Chromosome', 'Position', 'Reference Allele', 'Alternate Allele', 
													'Haplotype Strand', 'Transcript', 'Amino Acid Change']);
					addEl(table, thead);
					var tbody = getEl('tbody');
					addEl(table, tbody);
					for (var i=0; i<allRows.length; i++){
						var block = infomgr.getRowValue(tabName, allRows[i], 'vcfinfo__hap_block');
						var chrom = infomgr.getRowValue(tabName, allRows[i], 'base__chrom');
						if (rowBlock == block && rowChrom == chrom){
							var pos = infomgr.getRowValue(tabName, allRows[i], 'base__pos');
							var ref = infomgr.getRowValue(tabName, allRows[i], 'base__ref_base');
							var alt = infomgr.getRowValue(tabName, allRows[i], 'base__alt_base');
							var hapStrand = infomgr.getRowValue(tabName, allRows[i], 'vcfinfo__hap_strand');
							var transcript = infomgr.getRowValue(tabName, allRows[i], 'base__transcript');
							var aaChange = infomgr.getRowValue(tabName, allRows[i], 'base__achange');
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