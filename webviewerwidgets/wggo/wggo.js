var widgetName = 'go';
widgetGenerators[widgetName] = {
	'summary': {
		'name': 'Gene Ontology',
		'width': 700, 
		'height': 400, 
		'callserver': true,
		'function': function (div, data) {
			if (div != null) {
				emptyElement(div);
			}
			if (data == undefined) {
				return;
			}
			var colorPalette = [
				'#ff0000', // red
				'#dc143c', // crimson
				'#ff4500', // orange red
				'#ffa500', // orange
				'#ffd700', // gold
				'#d2691e', // chocolate
				'#8b4513', // saddle brown
				'#adff2f', // green yellow
				'#7fffd4', // aqua marine
				'#00ced1', // dark turquoise
				'#00bfff', // deep sky blue
				'#ffff00', // yellow
				'#0000ff', // blue
				'#00ff00', // lime
				'#00ffff', // aqua
				'#000080', // navy
				'#800080', // purple
				'#800000', // maroon
				'#808000', // olive
				'#008080', // teal
				'#008000', // green
				'#ff00ff', // fuchsia
			];
			div.style.width = 'calc(100% - 37px)';
			var chartDiv = getEl('canvas');
			chartDiv.style.width = 'calc(100% - 20px)';
			chartDiv.style.height = 'calc(100% - 20px)';
			addEl(div, chartDiv);
			
			var x = [];
			var y = [];
			var maxY = 0;
			var colors = [];
			for (var i = 0; i < data.length; i++){
				var desc = data[i]['description'];
				var geneCount = data[i]['geneCount'];
				x.push(desc);
				y.push(geneCount);
				if (geneCount > maxY) {
					maxY = geneCount;
				}
				colors.push(colorPalette[i % colorPalette.length]);
			}
			
			var color = Chart.helpers.color;
			var chart = new Chart(chartDiv, {
				type: 'horizontalBar',
				data: {
					labels: x,
					datasets: [
						{
							data: y,
							backgroundColor: colors,
							borderColor: '#000000',
							borderWidth: 0.7,
							hoverBorderColor: '#aaaaaa'
						}
					]
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					legend: {display: false},
					scales: {
						xAxes: [{
							scaleLabel: {
								display: true,
								labelString: '# genes',
							},
							ticks: {
								beginAtZero: true,
								stepSize: 1.0,
								max: maxY + 1,
							}
						}],
					},
					tooltips: {
						backgroundColor: '#ffffff',
						displayColors: false,
						titleFontColor: '#000000',
						titleFontStyle: 'normal',
						bodyFontColor: '#000000',
						borderColor: '#333333',
						borderWidth: 1,
					}
				}
			});
			widgetCharts[widgetName] = chart;
		}
	}
};
