var widgetName = 'codingvsnoncoding';
widgetGenerators[widgetName] = {
	'summary': {
		'name': 'Coding vs Noncoding',
		'width': 400, 
		'height': 400, 
		'callserver': false,
		'function': function (div) {
			console.log('here');
			if (div != null) {
				emptyElement(div);
			}
			var noCoding = 0;
			var noNoncoding = 0;
			var d = infomgr.getData('variant'); 
			for (var i = 0; i < d.length; i++) {
				var row = d[i]; 
				var hugo = infomgr.getRowValue('variant', row, 'base__hugo'); 
				if (hugo == '') {
					noNoncoding++;
				} else {
					noCoding++;
				}
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
						data: [
							noCoding,
							noNoncoding
						],
						backgroundColor: [
							'#f7c654',
							'#69a3ef',
							],
					}],
					labels: [
						'Coding', 
						'Non-coding'
					]
				},
				options: {
					responsive: true
				}
			});
			widgetCharts[widgetName] = chart;
		}
	}
};
