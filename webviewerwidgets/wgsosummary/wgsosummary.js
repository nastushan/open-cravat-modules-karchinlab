var widgetName = 'sosummary';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'Sequence Ontology',
		'width': 380, 
		'height': 380, 
		'callserver': false,
		'function': function (div) {
			if (div != null) {
				emptyElement(div);
			}
			var so_dic = {
                null: 'Intergenic',
		        '':'Intergenic',
		        'missense':'Missense',
		        'synonymous':'Synonymous',
		        'frameshift insertion':'Frameshift insertion',
		        'frameshift insertion by 1':'Frameshift insertion',
		        'frameshift insertion by 2':'Frameshift insertion',
		        'frameshift deletion':'Frameshift deletion',
		        'frameshift deletion by 1':'Frameshift deletion',
		        'frameshift deletion by 2':'Frameshift deletion',
		        'inframe insertion':'Inframe insertion',
		        'inframe deletion':'Inframe deletion',
		        'complex substitution':'Complex substitution',
		        'stop gained':'Stopgain',
		        'stop lost':'Stoploss',
		        'splice site':'Splice site',
		        '2kb upstream':'2k upstream',
		        '2kb downstream':'2k downstream',
		        '3-prime utr':'3\' UTR',
		        '5-prime utr':'5\' UTR',
		        'intron':'Intron',
		        'unknown':'Unknown',
				'MIS':'Missense',
				'SYN':'Synonymous',
				'FSI':'Frameshift insertion',
				'FI1':'Frameshift insertion',
				'FI2':'Frameshift insertion',
				'FSD':'Frameshift deletion',
				'FD1':'Frameshift deletion',
				'FD2':'Frameshift deletion',
				'IIV':'Inframe insertion',
				'INI':'Inframe insertion',
				'IDV':'Inframe deletion',
				'IND':'Inframe deletion',
				'CSS':'Complex substitution',
				'STG':'Stopgain',
				'STL':'Stoploss',
				'SPL':'Splice site',
				'2KU':'2k upstream',
				'2KD':'2k downstream',
				'UT3':'3\' UTR',
				'UT5':'5\' UTR',
				'INT':'Intron',
				'UNK':'Unknown'
		    };
			var colors = [
				'#008080', // teal
				'#ffd700', // gold
				'#00ff00', // lime
				'#ff0000', // red
				'#dc143c', // crimson
				'#d2691e', // chocolate
				'#8b4513', // saddle brown
				'#0000ff', // blue
				'#ff4500', // orange red
				'#ffa500', // orange
				'#adff2f', // green yellow
				'#7fffd4', // aqua marine
				'#00ced1', // dark turquoise
				'#00bfff', // deep sky blue
				'#ffff00', // yellow
				'#00ffff', // aqua
				'#000080', // navy
			];
			var counts = {};
			var d = infomgr.getData('variant'); 
			for (var i = 0; i < d.length; i++) {
				var row = d[i]; 
				var so = infomgr.getRowValue('variant', row, 'base__so'); 
				so = so_dic[so];
				if (so != '') {
					if (counts[so] == undefined) {
						counts[so] = 0;
					}
					counts[so] = counts[so] + 1;
				}
			}
			var labels = Object.keys(counts);
			var data = [];
			for (var i = 0; i < labels.length; i++) {
				var count = counts[labels[i]];
				data.push(count);
			}
			div.style.width = 'calc(100% - 37px)';
			var chartDiv = getEl('canvas');
			chartDiv.style.width = 'calc(100% - 20px)';
			chartDiv.style.height = 'calc(100% - 20px)';
			addEl(div, chartDiv);
			var chart = new Chart(chartDiv, {
				type: 'doughnut',
				data: {
					datasets: [{
						data: data,
						backgroundColor: colors
					}],
					labels: labels
				},
				options: {
					responsive: true,
                    responsiveAnimationDuration: 500,
                    maintainAspectRatio: false,
				}
			});
		}
	}
};
