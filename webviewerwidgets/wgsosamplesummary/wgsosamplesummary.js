widgetGenerators['sosamplesummary'] = {
	'info': {
		'name': 'Sequence Ontology by Sample',
		'width': 600, 
		'height': 800, 
		'callserver': true,
		'function': function (div, data) {
			var colorPalette = {
				'Frameshift insertion':'#ff0000', // red
				'Frameshift deletion':'#dc143c', // crimson
				'Stopgain':'#ff4500', // orange red
				'Stoploss':'#ffa500', // orange
				'Missense':'#ffd700', // gold
				'Inframe insertion':'#d2691e', // chocolate
				'Inframe deletion':'#8b4513', // saddle brown
				'Splice site':'#adff2f', // green yellow
				'2k upstream':'#7fffd4', // aqua marine
				'2k downstream':'#00ced1', // dark turquoise
				'3\' UTR':'#00bfff', // deep sky blue
				'5\' UTR':'#ffff00', // yellow
				'Complex substitution':'#0000ff', // blue
				'Synonymous':'#00ff00', // lime
				'Intron':'#00ffff', // aqua
				'Unknown':'#000080', // navy
				'Intergenic':'#008080', // teal
				/*
				'#800080', // purple
				'#800000', // maroon
				'#808000', // olive
				'#008000', // green
				'#ff00ff', // fuchsia
				*/
	        };
			
			if (div != null) {
				emptyElement(div);
			}
			
			div.style.width = 'calc(100% - 37px)';
			var chartDiv = getEl('canvas');
			chartDiv.style.width = 'calc(100% - 20px)';
			chartDiv.style.height = 'calc(100% - 20px)';
			addEl(div, chartDiv);

			var samples = data['samples'];
			var sos = data['sos'];
			var socountdata = data['socountdata'];
			var datasets = [];
			for (var i = 0; i < sos.length; i++) {
				var so = sos[i];
				row = {};
				row['label'] = so
				row['backgroundColor'] = colorPalette[so];
				row['data'] = socountdata[so];
				datasets.push(row);
			}
			var chart = new Chart(chartDiv, {
				type: 'bar',
				data: {
					labels: samples,
					datasets: datasets
				},
				options: {
					title: {
						display: true,
					},
					tooltips: {
						mode: 'index',
						intersect: false
					},
					responsive: true,
					scales: {
						xAxes: [{
							stacked: true,
						}],
						yAxes: [{
							stacked: true
						}]
					}
				}
			});
			widgetCharts['sosamplesummary'] = chart;
		}
	}
};
