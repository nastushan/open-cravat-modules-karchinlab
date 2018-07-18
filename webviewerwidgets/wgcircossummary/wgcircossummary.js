var widgetName = 'circossummary';

$.getScript('/widget_support/circossummary/biocircos-1.1.1.js', function () {});
$.getScript('/widget_support/circossummary/karyotype.human.grch38.js', function () {});
$.getScript('/widget_support/circossummary/d3.js', function () {});

widgetGenerators[widgetName] = {
	'info': {
		'name': 'Circos',
		'width': 600, 
		'height': 700, 
		'callserver': true,
		'function': function (div, data) {
			if (div != null) {
				emptyElement(div);
			}
			var chartSize = {
					widgth: 580, 
					height: 600
			};
			var genome = [
		        ['1', 248956422],
		        ['2', 242193529],
		        ['3', 198295559],
		        ['4', 190214555],
		        ['5', 181538259],
		        ['6', 170805979],
		        ['7', 159345973],
		        ['8', 145138636],
		        ['9', 138394717],
		        ['10', 133797422],
		        ['11', 135086622],
		        ['12', 133275309],
		        ['13', 114364328],
		        ['14', 107043718],
		        ['15', 101991189],
		        ['16', 90338345],
		        ['17', 83257441],
		        ['18', 80373285],
		        ["19", 58617616],
		        ['20', 64444167],
		        ['21', 46709983],
		        ['22', 50818468],
		        ['X', 156040895],
		        ['Y', 57227415]
		    ];
			var parentDiv = div;
			var chartDiv = null;
			var chartDivId = 'circos_summary';
			var dataParams = null;
			var chartSettings = {
					target: chartDivId,
					svgWidth: chartSize['widgth'],
					svgHeight: chartSize['height'],
					chrPad: 0.01,
					innerRadius: 260,
					outerRadius: 270,
					zoom: true,
					genomeFillColor: ["rgb(187, 187, 187)"],
					genomeLabel: {
						display : true,
						textSize : 10,
						textColor : "#000",
						dx : 0.028,
						dy : "-0.55em"
					},
					ticks: {
						'display': false
					},
					HISTOGRAMMouseEvent: true,
					HISTOGRAMMouseOverDisplay: true,
					HISTOGRAMMouseEnterColor: 'none',
					HISTOGRAMMouseLeaveColor: 'none',
					HISTOGRAMMouseMoveColor: 'none',
					HISTOGRAMMouseOutColor: 'none',
					HISTOGRAMMouseOverColor: 'none',
					HISTOGRAMMouseOutDisplay: true,
					HISTOGRAMMouseOverTooltipsHtml01 : "chr :",
					HISTOGRAMMouseOverTooltipsHtml02 : "<br>position: ",
					HISTOGRAMMouseOverTooltipsHtml03 : " ~ ",
					HISTOGRAMMouseOverTooltipsHtml04 : "<br>Sequence ontologies: ",
					HISTOGRAMMouseOverTooltipsHtml05 : "<br>count : ",
					HISTOGRAMMouseOverTooltipsHtml06 : "",
					HISTOGRAMMouseOverTooltipsPosition : "absolute",
					HISTOGRAMMouseOverTooltipsBackgroundColor : "white",
					HISTOGRAMMouseOverTooltipsBorderStyle : "solid",
					HISTOGRAMMouseOverTooltipsBorderWidth : 0,
					HISTOGRAMMouseOverTooltipsPadding : "3px",
					HISTOGRAMMouseOverTooltipsBorderRadius : "3px",
					HISTOGRAMMouseOverTooltipsOpacity : 0.8,
			};
			function addLegendItem (legendDiv, legendColor, legendText) {
				var legendHeight = '14px';
				var bar = getEl('div');
				bar.style.display = 'inline-block';
				bar.style.width = '14px';
				bar.style.height = legendHeight;
				bar.style.backgroundColor = legendColor;
				addEl(legendDiv, bar);
				
				var spacer = getEl('div');
				spacer.style.display = 'inline-block';
				spacer.style.width = '10px';
				spacer.style.height = legendHeight;
				addEl(legendDiv, spacer);
				
				var text = getEl('div');
				text.style.display = 'inline-block';
				text.style.verticalAlign = 'top';
				text.style.height = legendHeight;
				text.style.fontSize = '12px';
				text.textContent = legendText;
				addEl(legendDiv, text);
			}
			
			chartDiv = getEl('div');
			chartDiv.id = chartDivId;
			chartDiv.style.width = chartSize['width'];
			chartDiv.style.height = chartSize['height'];
			chartDiv.style.display = 'inline-block';
			addEl(parentDiv, chartDiv);

			var missense = 
				[
					"HISTOGRAM01",
					{maxRadius: 255, minRadius: 225, histogramFillColor: "#66ff66"},
					data['Missense']
				];
			var nonSilent = 
				[
					"HISTOGRAM02",
					{maxRadius: 220, minRadius: 190, histogramFillColor: "#aaaa44"},
					data['Non-silent']
				];
			var inactivating = 
				[
					"HISTOGRAM03",
					{maxRadius: 185, minRadius: 155, histogramFillColor: "#ff6666"},
					data['Inactivating']
				];
			var circos = new BioCircos(missense, nonSilent, inactivating, genome, chartSettings);
			circos.draw_genome(circos.genomeLength);
			
			var histogramSetting = {
				'Missense': {'color': '#66ff66'},
				'Non-silent': {'color': '#aaaa44'},
				'Inactivating': {'color': '#ff6666'}
			};
			
			var legendDiv = getEl('div');
			legendDiv.id = 'circoslegenddiv';
			legendDiv.style.display = 'inline-block';
			legendDiv.style.verticalAlign = 'top';
			var categories = ['Inactivating', 'Missense', 'Non-silent'];
			for (var i = 0; i < categories.length; i++) {
				var category = categories[i];
				var legend = getEl('div');
				legend.style.padding = '3px';
				addLegendItem(legend, histogramSetting[category]['color'], category);
				addEl(legendDiv, legend);
			}
			addEl(parentDiv, legendDiv);

		}
	}
};
