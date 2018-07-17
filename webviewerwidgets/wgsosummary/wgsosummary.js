var widgetName = 'sosummary';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'Sequence Ontology',
		'width': 580, 
		'height': 780, 
		'callserver': false,
		'function': function (div) {
			if (div != null) {
				emptyElement(div);
			}
			var so_dic = {
		        '':'Intergenic',
		        'MIS':'Missense',
		        'SYN':'Synonymous',
		        'FI1':'Frameshift insertion',
		        'FI2':'Frameshift insertion',
		        'FD1':'Frameshift deletion',
		        'FD2':'Frameshift deletion',
		        'IIV':'Inframe insertion',
		        'IDV':'Inframe deletion',
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
					responsive: true
				}
			});
			widgetCharts[widgetName] = chart;
		}
	}
};
