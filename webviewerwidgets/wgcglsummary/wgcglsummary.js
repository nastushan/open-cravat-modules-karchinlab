var widgetName = 'cglsummary';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'Cancer Genome Landscape',
		'width': 280, 
		'height': 280, 
		'callserver': false,
        'variables': {},
        'init': function () {
            var v = this['variables'];
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
            v['tsg'] = noTSG;
            v['oncogene'] = noOncogene;
            v['neutral'] = noNeutral;
        },
        'shoulddraw': function () {
            var v = this['variables'];
            if (v['tsg'] + v['oncogene'] + v['neutral'] == 0) {
                return false;
            } else {
                return true;
            }
        },
		'function': function (div) {
			if (div != null) {
				emptyElement(div);
			}
            var v = this['variables'];
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
							v['neutral'],
							v['oncogene'],
							v['tsg']
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
					responsive: true,
                    responsiveAnimationDuration: 500,
                    maintainAspectRatio: false,
                    legend: {
                        position: 'bottom',
                    },
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItem) {
                                var lbl = null;
                                switch(tooltipItem.index) {
                                    case 0:
                                        lbl = 'Neutral: ' + v['neutral'];
                                        break;
                                    case 1:
                                        lbl = 'Oncogenes: ' + v['oncogene'];
                                        break;
                                    case 2:
                                        lbl = 'Tumor suppressor genes:' + v['tsg'];
                                        break;
                                    default:
                                        break;
                                }
                                return lbl;
                            }
                        }
                    },
				}
			});
		}
	}
};
