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
			var counts = {};
			var d = infomgr.getData('variant'); 
			for (var i = 0; i < d.length; i++) {
				var row = d[i]; 
				var so = infomgr.getRowValue('variant', row, 'base__so'); 
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
							'#f7c654',
							'#69a3ef',
							'#69ef93'
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
