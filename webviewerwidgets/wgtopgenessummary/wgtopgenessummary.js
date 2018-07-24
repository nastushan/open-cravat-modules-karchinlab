widgetGenerators['topgenessummary'] = {
	'info': {
		'name': 'Most Frequently Mutated Genes (normalized by gene length and sorted by % samples mutated)',
		'width': 780, 
		'height': 780, 
		'callserver': true,
		'function': function (div, data) {
			if (div != null) {
				emptyElement(div);
			}
			
			div.style.width = 'calc(100% - 37px)';
			var chartDiv = getEl('canvas');
			chartDiv.style.width = 'calc(100% - 20px)';
			chartDiv.style.height = 'calc(100% - 20px)';
			addEl(div, chartDiv);

			var x = [];
			var y = [];
			for (var i = 0; i < data.length; i++) {
				var row = data[i];
				x.push(row[0]);
				y.push(row[1]);
			}
			
			var chart = new Chart(chartDiv, {
				type: 'horizontalBar',
				data: {
					labels: x,
					datasets: [
						{
							data: y,
							borderColor: '#000000',
							borderWidth: 0.7,
							hoverBorderColor: '#aaaaaa',
							backgroundColor: '#f49e42'
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
								labelString: ' % samples',
							},
							ticks: {
								beginAtZero: true,
								stepSize: 1.0,
								max: 1.0,
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
		}
	}
};
