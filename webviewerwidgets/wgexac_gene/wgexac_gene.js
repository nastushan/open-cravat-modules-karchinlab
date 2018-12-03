widgetGenerators['exac_gene'] = {
	'gene': {
		'width': 425, 
		'height': 280, 
		'function': function (div, row, tabName) {
			var noise = infomgr.getRowValue(tabName, row, 'exac_gene__exac_cnv_flag');
			if(noise === 'N'){
				noise ='No';
			}
			else if (noise === 'Y'){
				noise = 'Yes';
			}
			addInfoLine(div, row, 'Prob of LoF Intolerance (Homo & Hetero)', 'exac_gene__exac_pli', tabName);
			addInfoLine(div, row, 'Prob of LoF Intolerance (Homo)', 'exac_gene__exac_prec', tabName);
			addInfoLine(div, row, 'Prob of LoF Tolerance (Homo & Hetero)', 'exac_gene__exac_pnull', tabName);
			addInfoLine(div, row, 'Prob of LoF Intolerance (Homo & Hetero) NonTCGA', 'exac_gene__exac_nontcga_pli', tabName);
			addInfoLine(div, row, 'Prob of LoF Intolerance (Homo) NonTCGA', 'exac_gene__exac_nontcga_prec', tabName);
			addInfoLine(div, row, 'Prob of LoF Tolerance (Homo & Hetero) NonTCGA', 'exac_gene__exac_nontcga_pnull', tabName);
			addInfoLine(div, row, 'Prob of LoF Intolerance (Homo & Hetero) Nonpsych', 'exac_gene__exac_nonpsych_pli', tabName);
			addInfoLine(div, row, 'Prob of LoF Intolerance (Homo) Nonpsych', 'exac_gene__exac_nonpsych_prec', tabName);
			addInfoLine(div, row, 'Prob of LoF Tolerance (Homo & Hetero) Nonpsych', 'exac_gene__exac_nonpsych_pnull', tabName);
			addInfoLine(div, row, 'Winsorised Deletion Intolerance Z-Score', 'exac_gene__exac_del_score', tabName);
			addInfoLine(div, row, 'Winsorised Duplication Intolerance Z-Score', 'exac_gene__exac_dup_score', tabName);
			addInfoLine(div, row, 'Winsorised CNV Intolerance Z-Score', 'exac_gene__exac_cnv_score', tabName);
			addInfoLineText(div, 'Noisy/Biased', noise);
		}
	}
}