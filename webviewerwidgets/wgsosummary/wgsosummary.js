var widgetName = 'sosummary';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'Sequence Ontology',
		'width': 400, 
		'height': 400, 
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
						backgroundColor: [
							'#222034',
							'#45283c',
							'#663931',
							'#8f563B',
							'#dfa066',
							'#eec39a',
							'#fbf236',
							'#99e550',
							'#6abe30',
							'#37496e',
							'#4b692f',
							'#524b24',
							'#323c39',
							'#3f3f74',
							'#306082',
							'#5b6ee1',
							'#639Bff',
							'#5fCDE4',
							'#Cbdbfc'
							],
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
