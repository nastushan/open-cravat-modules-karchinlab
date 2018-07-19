$.getScript('/widget_support/mupit/3dmol.js', function () {});

widgetGenerators['mupit'] = {
	'variant': {
		'width': 600, 
		'height': 500, 
		'function': function (div, row, tabName) {
			var canvasdiv = getEl('div');
			canvasdiv.id = 'mupit_canvas_variant';
			canvasdiv.style.width = widgetGenerators['mupit']['variant']['width'] + 'px';
			canvasdiv.style.height = widgetGenerators['mupit']['variant']['height'] + 'px';
			addEl(div, canvasdiv);
			var $canvasdiv = $(canvasdiv);
			v = $3Dmol.createViewer($canvasdiv, {});
			$.get('/widget_support/mupit/test.pdb', function (data) {
				v.addModel(data, 'pdb');
				v.setStyle({}, {cartoon:{style:"trace"}});
				v.zoomTo();
				v.render();
			});
			/*$.get('/widget_support/mupit/test.pdb', function (data) {
				v.addModel(data, 'pdb');
				v.zoomTo();
				v.render();
			});*/
		}
	}
}