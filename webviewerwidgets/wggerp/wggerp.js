widgetGenerators['gerp'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Neutral Rate', 'gerp__gerp_nr', tabName);
			addInfoLine(div, row, 'RS Score', 'gerp__gerp_rs', tabName);
			addInfoLine(div, row, 'RS Ranked Score', 'gerp__gerp_rs_rank', tabName);
		}
	}
}