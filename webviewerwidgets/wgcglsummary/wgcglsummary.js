var widgetName = 'cglsummary';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'Cancer Genome Landscape',
		'width': 280, 
		'height': 280, 
		'callserver': false,
		'function': function (div) {
			if (div != null) {
				emptyElement(div);
			}
			var noTSG = 0;
			var noOncogene = 0;
			var noNeutral = 0;
			var d = infomgr.getData('gene'); 
			for (var i = 0; i < d.length; i++) {
				var row = d[i]; 
				var cgl = infomgr.getRowValue('gene', row, 'cgl__class'); 
				if (cgl == '') {
					noNeutral++;
				} else if (cgl == 'TSG'){
					noTSG++;
				} else if (cgl == 'Oncogene') {
					noOncogene++;
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
							noNeutral,
							noOncogene,
							noTSG
						],
						backgroundColor: [
							'#f7c654',
							'#69a3ef',
							'#69ef93'
							],
					}],
					labels: [
						'Neutral', 
						'Oncogene',
						'TSG'
					]
				},
				options: {
					responsive: true
				}
			});
		}
	}
};
