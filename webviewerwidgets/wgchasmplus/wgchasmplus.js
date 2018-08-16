widgetGenerators['chasmplus'] = {
	'variant': {
		'width': 280, 
		'height': 280, 
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Score', 'chasmplus__score', tabName);
			addInfoLine(div, row, 'P-value', 'chasmplus__pval', tabName);
			addInfoLine(div, row, 'Transcript', 'chasmplus__transcript', tabName);
            var allMappings = infomgr.getRowValue(tabName, row, 'chasmplus__results');
            if (allMappings != '') {
                var table = getWidgetTableFrame(['50%', '25%', '25%']);
                table.style.width = '100%';
                var thead = getWidgetTableHead(['Transcript', 'Score', 
                    'P-value']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                var lines = allMappings.split(',')
                for (var i = 0; i < lines.length; i++) {
                    var toks = lines[i].split(':')
                    var transcript = toks[0]
                    var score = toks[1].replace('(', '')
                    var pval = toks[2].replace(')', '')
                    var tr = getWidgetTableTr([transcript, score, pval]);
                    addEl(tbody, tr);
                }
                addEl(div, addEl(table, tbody));
            }
		}
	}
}
