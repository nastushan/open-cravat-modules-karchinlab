widgetGenerators['dbsnp'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
            var snp = getWidgetData(tabName, 'dbsnp', row, 'snp');
			var link = '';
			if(snp != null){
				link = 'http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=' + snp;
			}
			else{
				snp = '';
			}
            addInfoLineLink(div, 'dbSNP', snp, link, 30);
		}
	}
}
