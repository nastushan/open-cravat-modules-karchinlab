widgetGenerators['gnomad_gene'] = {
	'gene': {
		'width': 840, 
		'height': 150, 
		'function': function (div, row, tabName) {
			var trx = infomgr.getRowValue(tabName, row, 'gnomad_gene__transcript');
			var trxls = trx != null ? trx.split(';') : [];
			var oelof = infomgr.getRowValue(tabName, row, 'gnomad_gene__oe_lof');
			var oelofls = oelof != null ? oelof.split(';').map(Number) : [];
			var oemis = infomgr.getRowValue(tabName, row, 'gnomad_gene__oe_mis');
			var oemisls = oemis != null ? oemis.split(';').map(Number) : [];
			var oesyn = infomgr.getRowValue(tabName, row, 'gnomad_gene__oe_syn');
			var oesynls = oesyn != null ? oesyn.split(';').map(Number) : [];
			var lofz = infomgr.getRowValue(tabName, row, 'gnomad_gene__lof_z');
			var lofzls = lofz != null ? lofz.split(';').map(Number) : [];
			var misz = infomgr.getRowValue(tabName, row, 'gnomad_gene__mis_z');
			var miszls = misz != null ? misz.split(';').map(Number) : [];
			var synz = infomgr.getRowValue(tabName, row, 'gnomad_gene__syn_z');
			var synzls = synz != null ? synz.split(';').map(Number) : [];
			var pli = infomgr.getRowValue(tabName, row, 'gnomad_gene__pLI');
			var plils = pli != null ? pli.split(';').map(Number) : [];
			var prec = infomgr.getRowValue(tabName, row, 'gnomad_gene__pRec');
			var precls = prec != null ? prec.split(';').map(Number) : [];
			var pnull = infomgr.getRowValue(tabName, row, 'gnomad_gene__pNull');
			var pnullls = pnull != null ? pnull.split(';').map(Number) : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Transcript','Obv/Exp LoF','Obv/Exp Mis','Obv/Exp Syn','LoF Z-Score','Mis Z-Score','Syn Z-Score','pLI','pRec','pNull'],['20%']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for(var i=0;i<trxls.length;i++){
				var tr = getWidgetTableTr([trxls[i],oelofls[i],oemisls[i],oesynls[i],lofzls[i],miszls[i],synzls[i],plils[i],precls[i],pnullls[i]]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}