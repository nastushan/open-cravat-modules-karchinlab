var widgetName = 'codingvsnoncodingsummary';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'Coding vs Noncoding',
		'width': 280, 
		'height': 280, 
		'callserver': false,
		'function': function (div) {
			if (div != null) {
				emptyElement(div);
			}
            div.style.textAlign = 'center';
			var noCoding = 0;
			var noNoncoding = 0;
			var d = infomgr.getData('variant'); 
			for (var i = 0; i < d.length; i++) {
				var row = d[i]; 
				var hugo = getWidgetData('variant', 'base', row, 'hugo'); 
                var so = getWidgetData('variant', 'base', row, 'so');
				if (hugo == '') {
					noNoncoding++;
				} else {
                    if (so == '2kb downstream' || so == '2kb upstream' ||
                        so == '3-prime utr' || so == '5-prime utr' ||
                        so == 'intron' || so == '') {
                        noNoncoding++;
                    } else {
                        noCoding++;
                    }
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
					responsive: true,
                    responsiveAnimationDuration: 500,
                    maintainAspectRatio: false,
                    legend: {
                        position: 'bottom',
                    },
				}
			});
		}
	}
};
