widgetGenerators['lollipop'] = {
	'variant': {
		'donterase': true,
		'width': 580, 
		'height': 180, 
		'variables': {
			'varColors': {
					'synonymous': 'rgb(250, 250, 250)',
					'missense': 'rgb(255, 251, 123)',
					'complex substitution': 'rgb(141, 237, 255)',
					'inframe insertion': 'rgb(181, 255, 131)',
					'inframe deletion': 'rgb(181, 255, 131)',
					'stop lost': 'rgb(63, 255, 193)',
					'splice site': 'rgb(255, 118, 35)',
					'stop gained': 'rgb(250, 0, 0)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'SYN': 'rgb(250, 250, 250)',
					'MIS': 'rgb(255, 251, 123)',
					'CSS': 'rgb(141, 237, 255)',
					'INI': 'rgb(181, 255, 131)',
					'IND': 'rgb(181, 255, 131)',
					'STL': 'rgb(63, 255, 193)',
					'SPL': 'rgb(255, 118, 35)',
					'STG': 'rgb(250, 0, 0)',
					'FI1': 'rgb(200, 0, 255)',
					'FI2': 'rgb(200, 0, 255)',
					'FIV': 'rgb(200, 0, 255)',
					'FSI': 'rgb(200, 0, 255)',
					'FD1': 'rgb(200, 0, 255)',
					'FD2': 'rgb(200, 0, 255)',
					'FDV': 'rgb(200, 0, 255)',
					'FSD': 'rgb(200, 0, 255)',
			},
			'varColorNoSo': '#aaaaaa',
			'reftranscript': null,
			'aaWidth': null,
			'boxDomainHeight': 30,
			'boxR': 6,
			'proteinWidth': null,
			'proteinHeight': 30,
			'aalen': null,
			'domainLineHeight': 7,
			'domainLineMinWidth': 7,
			'variantMinWidth': 2,
			'variantRadius': 5,
			'xStart': 4,
			'xEndPad': 14,
			'varHeightMax': 22,
			'varHeightMin': 12,
			'maxVarNumSample': 5,
			'hugo': null,
			'widgetContentDiv': null,
			'variantdatasource': null,
			'variantcategory': null,
			'sitedatasource': null,
		},
		'function': function (div, row) {
			var self = this;
			var widgetName = 'lollipop';
			var widgetDiv = div.parentElement;
			var toks = widgetDiv.id.split('_');
			var tabName = toks[1];
			
			var v = widgetGenerators[widgetName][tabName]['variables'];
			
			v.widgetContentDiv = div;
            v.tabName = tabName;
			
			var hugo = infomgr.getRowValue(tabName, row, 'base__hugo');
			if (hugo == '') {
				$(div).empty();
                var sdiv = getEl('div');
                sdiv.textContent = 'No gene';
                addEl(div, sdiv);
				return;
			}
			if (hugo != v.hugo || v['resized'] != false || this.drawing == true) {
				if (v.drawing) {
					clearTimeout(self.runTimeout);
					    $(div).empty();
				}
				v.hugo = hugo;
				v.drawing = true;
				self.runTimeout = setTimeout(function () {
					$(div).empty();
                    var spinner = getSpinner();
                    spinner.className = 'widgetspinner';
                    addEl(div, spinner);
					$.get('/result/runwidget/' + widgetName, 
							{hugo: hugo}).done(function (data) {
                        var widgetContentDiv = document.getElementById('widgetcontentdiv_' + widgetName + '_' + self.variables.tabName);
                        var spinner = widgetContentDiv.getElementsByClassName('widgetspinner')[0];
                        $(spinner).remove();
						widgetGenerators[widgetName]['data'] = data;
						if (data['hugo'] != v.hugo) {
						    return;
						}
                        if (data['len'] == undefined) {
                            var sdiv = getEl('div');
                            sdiv.textContent = 'No protein diagram in UniProt';
                            addEl(div, sdiv);
                            return;
                        }
						draw(data);
						if (v.variantdatasource != null) {
							var select = 
								document.getElementById(
									getVarDatasourceSelectorId());
							var idx = getOptionIndex(select, v.variantdatasource);
							if (idx == -1) {
								idx = 0;
							} else {
								select.selectedIndex = idx;
								select.dispatchEvent(new Event('change'));
							}
						}
						if (v.variantcategory != null) {
							var select = 
								document.getElementById(getVarCategorySelectorId());
							var idx = getOptionIndex(select, v.variantcategory);
							if (idx == -1) {
								idx = 0;
							} else {
								select.selectedIndex = idx
								select.dispatchEvent(new Event('change'));
							}
						}
						if (v.sitedatasource != null) {
							var select = 
								document.getElementById(
										getProtSiteSourceSelectorId());
							var idx = getOptionIndex(select, v.sitedatasource);
							if (idx == -1) {
								idx = 0;
							} else {
								select.selectedIndex = idx;
								select.dispatchEvent(new Event('change'));
							}
						}
						this.drawing = false;
					});
				}, 200);
			} else {
				drawMyVariants(widgetGenerators[widgetName]['data']);
			}
			
			function getOptionIndex (select, value) {
				var options = select.options;
				var index = -1;
				for (var i = 0; i < options.length; i++) {
					if (options[i].value == value) {
						index = i;
						break;
					}
				}
				return index;
			}
			
			function getMyVarCanvasId (datasource) {
				var id = tabName + '_' + widgetName + '_myvar_canvas';
				return id;
			}
			
			function getOtherVarCanvasId (datasource) {
				var id = tabName + '_' + widgetName + '_othervar_canvas';
				return id;
			}
			
			function getProtCanvasId () {
				var id = tabName + '_' + widgetName + '_prot_canvas';
				return id;
			}
			
			function getSiteCanvasId () {
				var id = tabName + '_' + widgetName + '_site_canvas';
				return id;
			}
			
			function getVarDatasourceSelectorId () {
				var id = tabName + '_' + widgetName + '_vardatasourceselect';
				return id;
			}
			
			function getVarCategorySelectorId () {
				var id = tabName + '_' + widgetName + '_varcategselect';
				return id;
			}
			
			function getVarCategorySelectorDivId () {
				var id = getVarCategorySelectorId() + '_div';
				return id;
			}
			
			function getProtSiteSourceSelectorId () {
				var id = tabName + '_' + widgetName + '_protsitedatasourceselect';
				return id;
			}
			
			function getMyVariant () {
				var allMappings = JSON.parse(infomgr.getRowValue(tabName, row, 'base__all_mappings'));
				var hugos = Object.keys(allMappings);
				variant = {};
				for (var i = 0; i < hugos.length; i++) {
					var hugo = hugos[i];
					var uniprot_ds = allMappings[hugo];
					for (var j = 0; j < uniprot_ds.length; j++) {
						var transcript = uniprot_ds[j][3];
						if (transcript == v.reftranscript) {
							var protchange = uniprot_ds[j][1];
							if (protchange == null) {
								continue;
							}
							variant['so'] = uniprot_ds[j][2];
							var refaa = protchange[0];
							var protchangelen = protchange.length;
							var altaa = protchange.substring(protchangelen - 1, protchangelen);
							var start = protchange.substring(1, protchangelen - 1);
							variant['start'] = start;
							variant['refaa'] = refaa;
							variant['altaa'] = altaa;
							variant['count'] = infomgr.getRowValue(tabName, row, 'base__numsample');
							break;
						}
					}
				}
				return variant;
			}
			
			function onChangeOtherVariantDatasource (select, data) {
				var categorySelect = 
					document.getElementById(getVarCategorySelectorId());
				for (; categorySelect.options.length > 0;) {
					categorySelect.remove(0);
				}
				var datasource = select.options[select.selectedIndex].value;
				var categories = null;
				var categoryPartDiv = 
					document.getElementById(getVarCategorySelectorDivId());
				if (datasource == '') {
					categories = [];
					$('#' + getOtherVarCanvasId()).empty();
					categoryPartDiv.style.display = 'none';
				} else {
					categories = Object.keys(data['variants'][datasource]);
					categories.sort();
					categoryPartDiv.style.display = 'inline-block';
				}
				var option = new Option('', '');
				categorySelect.options.add(option);
				for (var i = 0; i < categories.length; i++) {
					var category = categories[i];
					if (category == '') {
						continue;
					}
					var option = new Option(category, category);
					categorySelect.options.add(option);
				}
				categorySelect.setAttribute('datasource', datasource);
				var v = widgetGenerators[widgetName][tabName]['variables'];
				v.variantdatasource = datasource;
			}
			
			function onChangeOtherVariantCategory (
					canvasId, data, datasource, category) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				$('#' + canvasId).empty();
				var stage = acgraph.create(canvasId);
				var y = 0;
				var varHeightInc = (v.varHeightMax - v.varHeightMin) / 
					v.maxVarNumSample;
				var variants = data['variants'][datasource][category];
				for (var j = 0; j < variants.length; j++) {
					var variant = variants[j];
					var start = variant['start'];
					var count = variant['num_sample'];
					variant['count'] = count;
					var x = start * v.aaWidth + v.xStart + v.aaWidth / 2;
					var width = v.variantMinWidth;
					var height = Math.min(
						v.varHeightMin + count * varHeightInc, 
						v.varHeightMax);
					var so = variant['so'];
					var color = v.varColors[so];
					if (color == undefined) {
						color = v.varColorNoSo;
					}
					var rect = stage.rect(x - width / 2, 
							y, 
							width, height).
							fill(color);
					var circle = stage.circle(x, y + height, v.variantRadius).
							fill(color);
                    var aachange = variant['refaa'] + variant['start'] + variant['altaa'];
                    rect.domElement_.setAttribute('aachange', aachange);
                    circle.domElement_.setAttribute('aachange', aachange);
					setupVariantPopup(rect, variant);
					setupVariantPopup(circle, variant);
				}
				var v = widgetGenerators[widgetName][tabName]['variables'];
				v.variantcategory = category;
			}
			
			function onChangeProtSiteDatasource (
					canvasId, data, datasource) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				var canvas = document.getElementById(canvasId);
				$(canvas).empty();
				if (datasource == '') {
					return;
				}
				v.sitedatasource = datasource;
				var stage = acgraph.create(canvasId);
				var y = 0;
				var domains = data['domains'];
				var lineDomains = domains[datasource];
				var stacks = {};
				var addlX = 10;
				for (var i = 0; i < lineDomains.length; i++) {
					var domain = lineDomains[i];
					var start = parseInt(domain.start * v.aaWidth);
					var stop = Math.max(
							parseInt(domain.stop * v.aaWidth), 
							v.domainLineMinWidth);
					var stackLevel = 0;
					while (true) {
						var stack = stacks[stackLevel];
						var collided = false;
						if (stack == undefined) {
							stack = {};
							stacks[stackLevel] = stack;
						}
						for (var k = start; k <= stop; k++) {
							if (stack[k] != undefined) {
								collided = true;
								break;
							}
						}
						if (collided == false) {
							for (l = start; l <= stop + addlX; l++) {
								stack[l] = true;
							}
							stacks[stackLevel] = stack;
							drawLineDomain(
									stage, 
									domain, 
									y + (v.domainLineHeight + 4) * stackLevel);
							break;
						} else {
							stackLevel++;
						}
					}
				}
				var dsDiv = canvas.parentElement;
				var maxStackLevel = Math.max(Object.keys(stacks));
				dsDiv.style.height = maxStackLevel * (v.domainLineHeight + 2) 
					+ 5 + 'px';
			}
			
			function setupVariantPopup (element, variant) {
                element.variant = variant;
				var v = widgetGenerators[widgetName][tabName]['variables'];
				acgraph.events.listen(element, 'mouseover', function (evt) {
					if (v['popup'] == null) {
						var x = evt.clientX;
						var y = evt.clientY - 50;
						var variant = evt.target['variant'];
						
						var div = getEl('div');
						div.style.position = 'fixed';
						div.style.top = y + 'px';
						div.style.left = x + 'px';
						div.style.zIndex = '10';
						div.style.padding = '6px';
						div.style.background = 'white';
						div.style.border = '1px solid black';
						div.style.borderRadius = '6px';
						
						var span = getEl('span');
						span.style.fontWeight = 'bold';
						var text = variant['refaa'] + variant['start'] + 
							variant['altaa'] + ' (' + variant['so'] + ')';
						addEl(div, addEl(span, getTn(text)));
						addEl(div, getEl('br'));
						
						var span = getEl('span');
						span.style.fontWeight = 'bold';
						addEl(span, getTn('# Samples: '));
						addEl(div, span);
						addEl(div, getTn(variant['count']));
						
						addEl(v.widgetContentDiv, div);
						v['popup'] = div;
					}
				});
				acgraph.events.listen(element, 'mouseout', function (evt) {
					if (v['popup'] != null) {
						$(v['popup']).remove();
						v['popup'] = null;
					}
				});
			}
			
			function setupDomainPopup (element, domain) {
				element.domain = domain;
				acgraph.events.listen(element, 'mouseover', function (evt) {
					if (v['popup'] == null) {
						var x = evt.clientX;
						var y = evt.clientY - 50;
						var domain = evt.target['domain'];
						var div = getEl('div');
						div.style.position = 'fixed';
						div.style.top = y + 'px';
						div.style.left = x + 'px';
						div.style.zIndex = '10';
						div.style.padding = '6px';
						div.style.background = 'white';
						div.style.border = '1px solid black';
						div.style.borderRadius = '6px';
						var span = getEl('span');
						span.style.fontWeight = 'bold';
						addEl(span, getTn(domain['desc']));
						addEl(div, span);
						addEl(div, getTn(':    '));
						span = getEl('span');
						addEl(span, getTn(domain['start']));
						addEl(div, span);
						addEl(div, getTn('     -     '));
						span = getEl('span');
						addEl(span, getTn(domain['stop']));
						addEl(div, span);
						addEl(div, getEl('br'));
						span = getEl('span');
						addEl(span, getTn(domain['feature_key']));
						addEl(div, span);
						addEl(v.widgetContentDiv, div);
						v['popup'] = div;
					}
				});
				acgraph.events.listen(element, 'mouseout', function (evt) {
					if (v['popup'] != null) {
						$(v['popup']).remove();
						v['popup'] = null;
					}
				});
			}
			
			function drawMyVariant (variant, stage, y, varHeightInc) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				var x = parseInt(variant.start) * v.aaWidth + v.xStart;
				var width = Math.max(v.variantMinWidth, v.aaWidth);
				var height = Math.min(
					v.varHeightMax, 
					Math.max(v.varHeightMin, 
							variant.count * varHeightInc)
					);
				var color = v.varColors[variant.so];
				if (color == undefined) {
					color = v.varColorNoSo;
				}
				var rect = stage.rect(
					x - width / 2, 
					y + v.varHeightMax - height, 
					width, 
					height).
					fill(color);
				var circle = stage.circle(
					x, 
					y + v.varHeightMax - height, 
					v.variantRadius).
					fill(color);
                var aachange = variant['refaa'] + variant['start'] + variant['altaa'];
                rect.domElement_.setAttribute('aachange', aachange);
                circle.domElement_.setAttribute('aachange', aachange);
				setupVariantPopup(rect, variant);
				setupVariantPopup(circle, variant);
			}
			
			function drawBoxDomain (stage, domain, y) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				var x = domain['start'] * v.aaWidth + v.xStart;
				var width = (domain['stop'] - domain['start']) * v.aaWidth;
				var color = 'brown';
				var box = stage.rect(x, y, width, v.boxDomainHeight).
					round(v.boxR, 
						v.boxR, 
						v.boxR, 
						v.boxR).
					stroke('##555555').
					fill({
						keys: ['0 #a34b1f', '0.6 #dddddd', '1 #a34b1f'],
						angle: 90
					});
				var text = stage.text(x + 2, y + 2, domain['shrt_desc']);
				setupDomainPopup(box, domain);
				setupDomainPopup(text, domain);
			}
			
			function drawLineDomain (stage, domain, y) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				var x = domain['start'] * v.aaWidth + v.xStart;
				var width = Math.max(v.domainLineMinWidth, 
						(domain['stop'] - domain['start']) * v.aaWidth - 2);
				var line = stage.rect(x, y, width, v.domainLineHeight).
					stroke('rgb(250, 162, 86)').
					fill('rgb(250, 162, 86)');
				setupDomainPopup (line, domain);
			}

			function draw (data) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				v.proteinWidth = getComputedStyle(div)['width'];
				v.proteinWidth = parseInt(
					v.proteinWidth.substring(0, v.proteinWidth.length - 2)) 
					- v.variantRadius - v.xEndPad;
				v.aalen = data['len'];
				v.aaWidth = v.proteinWidth / v.aalen;
				v.reftranscript = data['transcript'];
				drawControlPanel(data);
				drawMyVariants(data);
				drawProtein(data);
				setupOtherVariantDiv(data);
				setupSiteDiv(data);
				this.drawing = false;
			}
			
			function drawControlPanel (data) {
				
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				// Container
				var dsDiv = getEl('div');
				dsDiv.style.width = '100%';
				dsDiv.style.height = '20px';
				addEl(div, dsDiv);
			
				// Protein site datasource selector
				var partDiv = getEl('div');
				partDiv.style.display = 'inline-block';
				span = getEl('span');
				addEl(span, getTn('Track: '));
				addEl(partDiv, span);
				select = getEl('select');
				select.id = getProtSiteSourceSelectorId();
				select.className = 'detailwidgetselect';
				var datasources = Object.keys(data['domains']);
				datasources.sort();
				var option = new Option('', '');
				select.options.add(option);
				for (var i = 0; i < datasources.length; i++) {
					var datasource = datasources[i];
					var option = new Option(datasource, datasource);
					select.options.add(option);
				}
				select.addEventListener('change', function (evt) {
					var select = evt.target;
					while (select.selectedIndex == -1) {}
					var datasource = select.getAttribute('datasource');
					onChangeProtSiteDatasource(
							getSiteCanvasId(), 
							data, select.options[select.selectedIndex].value);
				});
				addEl(partDiv, select);
				addEl(dsDiv, partDiv);

				// Variant datasource selector
				var datasources = Object.keys(data['variants']);
				datasources.sort();
				var partDiv = getEl('div');
				partDiv.style.display = 'inline-block';
				var span = getEl('span');
				addEl(span, getTn('\xa0\xa0Reference variants from: '));
				addEl(partDiv, span);
				var select = getEl('select');
				select.id = getVarDatasourceSelectorId();
				select.className = 'detailwidgetselect';
				select.addEventListener('change', function (evt) {
					var select = evt.target;
					onChangeOtherVariantDatasource(select, data);
				});
				addEl(partDiv, select);
				var option = new Option('', '');
				select.options.add(option);
				for (var i = 0; i < datasources.length; i++) {
					var datasource = datasources[i];
					var option = new Option(datasource, datasource);
					select.options.add(option);
				}
				addEl(dsDiv, partDiv);
				
				// Variant category selector
				var partDiv = getEl('div');
				partDiv.id = getVarCategorySelectorDivId();
				partDiv.style.display = 'none';
				span = getEl('span');
				addEl(span, getTn('  (Category: '));
				addEl(partDiv, span);
				select = getEl('select');
				select.id = getVarCategorySelectorId();
				select.className = 'detailwidgetselect';
				select.addEventListener('change', function (evt) {
					var select = evt.target;
					var datasource = select.getAttribute('datasource');
					onChangeOtherVariantCategory(
							getOtherVarCanvasId(), 
							data, datasource, 
							select.options[select.selectedIndex].value);
				});
				addEl(partDiv, select);
				addEl(partDiv, addEl(getEl('span'), getTn(')')));
				addEl(dsDiv, partDiv);
			}
			
			function drawMyVariants (data) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				// Erases canvas for a new gene.
				var canvasId = getMyVarCanvasId();
				var canvas = document.getElementById(canvasId);
				if (canvas == undefined || canvas == null) {
					var dsDiv = getEl('div');
					dsDiv.style.width = '100%';
					dsDiv.style.height = v.varHeightMax + v.variantRadius;
					
					var canvas = getEl('div');
					canvas.id = canvasId;
					canvas.style.width = '100%';
					canvas.style.height = v.varHeightMax + v.variantRadius;
					addEl(dsDiv, canvas);
					
					addEl(div, dsDiv);
				} else {
					$(canvas).empty();
				}
				
				// Stage
				var stage = acgraph.create(canvas);
				var y = v.variantRadius;
				var varHeightInc = (v.varHeightMax - v.varHeightMin) / 
						v.maxVarNumSample;

				// Draws.
				var variant = getMyVariant();
				if (variant != null && variant.start != undefined) {
					drawMyVariant(variant, stage, y, varHeightInc);
				}
			}
			
			function drawProtein (data) {
				
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				// Protein container
				var dsDiv = getEl('div');
				dsDiv.style.width = '100%';
				dsDiv.style.height = '30px';
				dsDiv.setAttribute('datasource', datasource);
				addEl(div, dsDiv);

                // Transcript
                var tsDiv = getEl('div');
                tsDiv.style.position = 'absolute';
                tsDiv.style.bottom = '7px';
                tsDiv.style.right = '12px';
                tsDiv.textContent = v.reftranscript;
                addEl(div, tsDiv);
				
				// Protein canvas
				var canvas = getEl('div');
				var canvasId = getProtCanvasId();
				canvas.id = canvasId;
				canvas.style.width = '100%';
				canvas.style.height = '100%';
				addEl(dsDiv, canvas);
				
				// Protein stage
				var stage = acgraph.create(canvas);
				var y = 0;
				
				// Protein
				stage.rect(v.xStart, y, v.proteinWidth, v.proteinHeight).
					round(v.boxR, v.boxR, v.boxR, v.boxR).
					stroke('#555555').
					fill({
						keys: ['0 #aaaaaa', '0.6 #dddddd', '1 #aaaaaa'],
						angle: 90,
						
					});
				
				// Pfam boxes
				var datasource = 'pfam';
				if (data['domains'] != undefined && 
						data['domains'][datasource] != undefined) {
					var domains = data['domains'][datasource];
					for (var i = 0; i < domains.length; i++) {
						var domain = domains[i];
						drawBoxDomain(stage, domain, y);
					}
				}
			}
			
			function setupOtherVariantDiv (data) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				var datasources = Object.keys(data['variants']);
				datasources.sort();
				var dsDiv = getEl('div');
				dsDiv.id = getOtherVarCanvasId();
				dsDiv.style.width = '100%';
				dsDiv.style.height = v.varHeightMax + v.variantRadius;
				addEl(div, dsDiv);
				var canvasId = dsDiv.id + '_canvas';
				
				var canvas = getEl('div');
				canvas.id = canvasId;
				canvas.style.width = '100%';
				canvas.style.height = v.varHeightMax + v.variantRadius;
				addEl(dsDiv, canvas);
			}
			
			function setupSiteDiv (data) {
				
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				var dsDiv = getEl('div');
				dsDiv.style.width = '100%';
				dsDiv.style.height = '30px';
				
				var canvas = getEl('div');
				var canvasId = getSiteCanvasId();
				canvas.id = canvasId;
				canvas.style.width = '100%';
				canvas.style.height = '100%';
				addEl(dsDiv, canvas);
				
				addEl(div, dsDiv);
			}
		}
	},
	'gene': {
		'donterase': true,
		'width': 580, 
		'height': 180, 
		'variables': {
			'varColors': {
					'synonymous': 'rgb(250, 250, 250)',
					'missense': 'rgb(255, 251, 123)',
					'complex substitution': 'rgb(141, 237, 255)',
					'inframe insertion': 'rgb(181, 255, 131)',
					'inframe deletion': 'rgb(181, 255, 131)',
					'stop lost': 'rgb(63, 255, 193)',
					'splice site': 'rgb(255, 118, 35)',
					'stop gained': 'rgb(250, 0, 0)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift insertion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'frameshift deletion': 'rgb(200, 0, 255)',
					'SYN': 'rgb(250, 250, 250)',
					'MIS': 'rgb(255, 251, 123)',
					'CSS': 'rgb(141, 237, 255)',
					'INI': 'rgb(181, 255, 131)',
					'IND': 'rgb(181, 255, 131)',
					'STL': 'rgb(63, 255, 193)',
					'SPL': 'rgb(255, 118, 35)',
					'STG': 'rgb(250, 0, 0)',
					'FI1': 'rgb(200, 0, 255)',
					'FI2': 'rgb(200, 0, 255)',
					'FIV': 'rgb(200, 0, 255)',
					'FSI': 'rgb(200, 0, 255)',
					'FD1': 'rgb(200, 0, 255)',
					'FD2': 'rgb(200, 0, 255)',
					'FDV': 'rgb(200, 0, 255)',
					'FSD': 'rgb(200, 0, 255)',
			},
			'varColorNoSo': '#aaaaaa',
			'reftranscript': null,
			'aaWidth': null,
			'boxDomainHeight': 30,
			'boxR': 6,
			'proteinWidth': null,
			'proteinHeight': 30,
			'aalen': null,
			'domainLineHeight': 7,
			'domainLineMinWidth': 7,
			'variantMinWidth': 2,
			'variantRadius': 5,
			'xStart': 160,
			'xEndPad': 14,
			'varHeightMax': 22,
			'varHeightMin': 12,
			'maxVarNumSample': 5,
			'hugo': null,
			'widgetContentDiv': null,
			'variantdatasource': null,
			'variantcategory': null,
			'sitedatasource': null,
		},
		'function': function (div, row) {
			var self = this;
			var widgetName = 'lollipop';
			var widgetDiv = div.parentElement;
			var toks = widgetDiv.id.split('_');
			var tabName = toks[1];
			
			var v = widgetGenerators[widgetName][tabName]['variables'];

			v.widgetContentDiv = div;
            v.tabName = tabName;
			
			var hugo = infomgr.getRowValue(tabName, row, 'base__hugo');
			if (hugo == '') {
				$(div).empty();
                var sdiv = getEl('div');
                sdiv.textContent = 'No gene';
                addEl(div, sdiv);
				return;
			}
			
			if (hugo != v.hugo || v['resized'] != false || this.drawing == true) {
				if (v.drawing) {
					clearTimeout(self.runTimeout);
                    $(div).empty();
				}
                v.hugo = hugo;
				v.drawing = true;
				self.runTimeout = setTimeout(function () {
					$(div).empty();
                    var spinner = getSpinner();
                    spinner.className = 'widgetspinner';
                    addEl(div, spinner);
					$.get('/result/runwidget/' + widgetName, 
							{hugo: hugo}).done(function (data) {
                        var widgetContentDiv = document.getElementById('widgetcontentdiv_' + widgetName + '_' + self.variables.tabName);
                        var spinner = widgetContentDiv.getElementsByClassName('widgetspinner')[0];
                        $(spinner).remove();
						widgetGenerators[widgetName]['data'] = data;
                        if (data['hugo'] != v.hugo) {
                            return;
                        }
                        if (data['len'] == undefined) {
                            var sdiv = getEl('div');
                            sdiv.textContent = 'No protein diagram in UniProt';
                            addEl(div, sdiv);
                            return;
                        }
						draw(data);
						if (v.variantdatasource != null) {
							var select = 
								document.getElementById(
									getVarDatasourceSelectorId());
							var idx = getOptionIndex(select, v.variantdatasource);
							if (idx == -1) {
								idx = 0;
							} else {
								select.selectedIndex = idx;
								select.dispatchEvent(new Event('change'));
							}
						}
						if (v.variantcategory != null) {
							var select = 
								document.getElementById(getVarCategorySelectorId());
							var idx = getOptionIndex(select, v.variantcategory);
							if (idx == -1) {
								idx = 0;
							} else {
								select.selectedIndex = idx
								select.dispatchEvent(new Event('change'));
							}
						}
						if (v.sitedatasource != null) {
							var select = 
								document.getElementById(
										getProtSiteSourceSelectorId());
							var idx = getOptionIndex(select, v.sitedatasource);
							if (idx == -1) {
								idx = 0;
							} else {
								select.selectedIndex = idx;
								select.dispatchEvent(new Event('change'));
							}
						}
					});
				}, 200);
			} else {
				drawMyVariants(widgetGenerators[widgetName]['data']);
			}
			
			function getOptionIndex (select, value) {
				var options = select.options;
				var index = -1;
				for (var i = 0; i < options.length; i++) {
					if (options[i].value == value) {
						index = i;
						break;
					}
				}
				return index;
			}
			
			function getMyVarCanvasId (datasource) {
				var id = tabName + '_' + widgetName + '_myvar_canvas';
				return id;
			}
			
			function getOtherVarCanvasId (datasource) {
				var id = tabName + '_' + widgetName + '_othervar_canvas';
				return id;
			}
			
			function getProtCanvasId () {
				var id = tabName + '_' + widgetName + '_prot_canvas';
				return id;
			}
			
			function getSiteCanvasId () {
				var id = tabName + '_' + widgetName + '_site_canvas';
				return id;
			}
			
			function getVarDatasourceSelectorId () {
				var id = tabName + '_' + widgetName + '_vardatasourceselect';
				return id;
			}
			
			function getVarCategorySelectorId () {
				var id = tabName + '_' + widgetName + '_varcategselect';
				return id;
			}
			
			function getVarCategorySelectorDivId () {
				var id = getVarCategorySelectorId() + '_div';
				return id;
			}
			
			function getProtSiteSourceSelectorId () {
				var id = tabName + '_' + widgetName + '_protsitedatasourceselect';
				return id;
			}
			
			function onChangeOtherVariantDatasource (select, data) {
				var categorySelect = 
					document.getElementById(getVarCategorySelectorId());
				for (; categorySelect.options.length > 0;) {
					categorySelect.remove(0);
				}

				var datasource = select.options[select.selectedIndex].value;
				
				var categories = null;
				var categoryPartDiv = 
					document.getElementById(getVarCategorySelectorDivId());
				if (datasource == '') {
					categories = [];
					$('#' + getOtherVarCanvasId()).empty();
					categoryPartDiv.style.display = 'none';
				} else {
					categories = Object.keys(data['variants'][datasource]);
					categories.sort();
					categoryPartDiv.style.display = 'inline-block';
				}
				
				var option = new Option('', '');
				categorySelect.options.add(option);
				for (var i = 0; i < categories.length; i++) {
					var category = categories[i];
					if (category == '') {
						continue;
					}
					var option = new Option(category, category);
					categorySelect.options.add(option);
				}
				
				categorySelect.setAttribute('datasource', datasource);
				
				var v = widgetGenerators[widgetName][tabName]['variables'];
				v.variantdatasource = datasource;
			}
			
			function onChangeOtherVariantCategory (
					canvasId, data, datasource, category) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				$('#' + canvasId).empty();
				var stage = acgraph.create(canvasId);
				var y = 0;
				var varHeightInc = (v.varHeightMax - v.varHeightMin) / 
					v.maxVarNumSample;
				var variants = data['variants'][datasource][category];
				for (var j = 0; j < variants.length; j++) {
					var variant = variants[j];
					var start = variant['start'];
					var count = variant['num_sample'];
					variant['count'] = count;
					var x = start * v.aaWidth + v.xStart + v.aaWidth / 2;
					var width = v.variantMinWidth;
					var height = Math.min(
						v.varHeightMin + count * varHeightInc, 
						v.varHeightMax);
					var so = variant['so'];
					var color = v.varColors[so];
					if (color == undefined) {
						color = v.varColorNoSo;
					}
					var rect = stage.rect(x - width / 2, 
							y, 
							width, height).
							fill(color);
					var circle = stage.circle(x, y + height, v.variantRadius).
							fill(color);
                    var aachange = variant['refaa'] + variant['start'] + variant['altaa'];
                    rect.domElement_.setAttribute('aachange', aachange);
                    circle.domElement_.setAttribute('aachange', aachange);
					setupVariantPopup(rect, variant);
					setupVariantPopup(circle, variant);
				}
				
				var v = widgetGenerators[widgetName][tabName]['variables'];
				v.variantcategory = category;
			}
			
			function onChangeProtSiteDatasource (
					canvasId, data, datasource) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				var canvas = document.getElementById(canvasId);
				$(canvas).empty();
				if (datasource == '') {
					return;
				}
				
				v.sitedatasource = datasource;
				
				var stage = acgraph.create(canvasId);
				var y = 0;
				
				var domains = data['domains'];
				var lineDomains = domains[datasource];
				var stacks = {};
				var addlX = 10;
				for (var i = 0; i < lineDomains.length; i++) {
					var domain = lineDomains[i];
					var start = parseInt(domain.start * v.aaWidth);
					var stop = Math.max(
							parseInt(domain.stop * v.aaWidth), 
							v.domainLineMinWidth);
					var stackLevel = 0;
					while (true) {
						var stack = stacks[stackLevel];
						var collided = false;
						if (stack == undefined) {
							stack = {};
							stacks[stackLevel] = stack;
						}
						for (var k = start; k <= stop; k++) {
							if (stack[k] != undefined) {
								collided = true;
								break;
							}
						}
						if (collided == false) {
							for (l = start; l <= stop + addlX; l++) {
								stack[l] = true;
							}
							stacks[stackLevel] = stack;
							drawLineDomain(
									stage, 
									domain, 
									y + (v.domainLineHeight + 4) * stackLevel);
							break;
						} else {
							stackLevel++;
						}
					}
				}
				var dsDiv = canvas.parentElement;
				var maxStackLevel = Math.max(Object.keys(stacks));
				dsDiv.style.height = maxStackLevel * (v.domainLineHeight + 2) 
					+ 5 + 'px';
			}
			
			function setupVariantPopup (element, variant) {
                element.variant = variant;
				var v = widgetGenerators[widgetName][tabName]['variables'];
				acgraph.events.listen(element, 'mouseover', function (evt) {
					if (v['popup'] == null) {
						var x = evt.clientX;
						var y = evt.clientY - 50;
						var variant = evt.target['variant'];
						
						var div = getEl('div');
						div.style.position = 'fixed';
						div.style.top = y + 'px';
						div.style.left = x + 'px';
						div.style.zIndex = '10';
						div.style.padding = '6px';
						div.style.background = 'white';
						div.style.border = '1px solid black';
						div.style.borderRadius = '6px';
						
						var span = getEl('span');
						span.style.fontWeight = 'bold';
						var text = variant['refaa'] + variant['start'] + 
							variant['altaa'] + ' (' + variant['so'] + ')';
						addEl(div, addEl(span, getTn(text)));
						addEl(div, getEl('br'));
						
						var span = getEl('span');
						span.style.fontWeight = 'bold';
						addEl(span, getTn('# Samples: '));
						addEl(div, span);
						addEl(div, getTn(variant['count']));
						
						addEl(v.widgetContentDiv, div);
						v['popup'] = div;
					}
				});
				acgraph.events.listen(element, 'mouseout', function (evt) {
					if (v['popup'] != null) {
						$(v['popup']).remove();
						v['popup'] = null;
					}
				});
			}
			
			function setupDomainPopup (element, domain) {
				element.domain = domain;
				acgraph.events.listen(element, 'mouseover', function (evt) {
					if (v['popup'] == null) {
						var x = evt.clientX;
						var y = evt.clientY - 50;
						var domain = evt.target['domain'];
						var div = getEl('div');
						div.style.position = 'fixed';
						div.style.top = y + 'px';
						div.style.left = x + 'px';
						div.style.zIndex = '10';
						div.style.padding = '6px';
						div.style.background = 'white';
						div.style.border = '1px solid black';
						div.style.borderRadius = '6px';
						var span = getEl('span');
						span.style.fontWeight = 'bold';
						addEl(span, getTn(domain['desc']));
						addEl(div, span);
						addEl(div, getTn(':    '));
						span = getEl('span');
						addEl(span, getTn(domain['start']));
						addEl(div, span);
						addEl(div, getTn('     -     '));
						span = getEl('span');
						addEl(span, getTn(domain['stop']));
						addEl(div, span);
						addEl(div, getEl('br'));
						span = getEl('span');
						addEl(span, getTn(domain['feature_key']));
						addEl(div, span);
						addEl(v.widgetContentDiv, div);
						v['popup'] = div;
					}
				});
				acgraph.events.listen(element, 'mouseout', function (evt) {
					if (v['popup'] != null) {
						$(v['popup']).remove();
						v['popup'] = null;
					}
				});
			}

			function drawMyVariant (variant, stage, y, varHeightInc) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				var x = parseInt(variant.start) * v.aaWidth + v.xStart;
				var width = Math.max(v.variantMinWidth, v.aaWidth);
				var height = Math.min(
					v.varHeightMax, 
					Math.max(v.varHeightMin, 
							variant.count * varHeightInc)
					);
				var color = v.varColors[variant.so];
				if (color == undefined) {
					color = v.varColorNoSo;
				}
				var rect = stage.rect(
					x - width / 2, 
					y + v.varHeightMax - height, 
					width, 
					height).
					fill(color);
				var circle = stage.circle(
					x, 
					y + v.varHeightMax - height, 
					v.variantRadius).
					fill(color);
                var aachange = variant['refaa'] + variant['start'] + variant['altaa'];
                rect.domElement_.setAttribute('aachange', aachange);
                circle.domElement_.setAttribute('aachange', aachange);
                circle.domElement_.classList.add('lollipop_gene');
				setupVariantPopup(rect, variant);
				setupVariantPopup(circle, variant);
			}
			
			function drawBoxDomain (stage, domain, y) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				var x = domain['start'] * v.aaWidth + v.xStart;
				var width = (domain['stop'] - domain['start']) * v.aaWidth;
				var color = 'brown';
				var box = stage.rect(x, y, width, v.boxDomainHeight).
					round(v.boxR, 
						v.boxR, 
						v.boxR, 
						v.boxR).
					stroke('##555555').
					fill({
						keys: ['0 #a34b1f', '0.6 #dddddd', '1 #a34b1f'],
						angle: 90
					});
				var text = stage.text(x + 2, y + 2, domain['shrt_desc']);
				setupDomainPopup(box, domain);
				setupDomainPopup(text, domain);
			}
			
			function drawLineDomain (stage, domain, y) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				var x = domain['start'] * v.aaWidth + v.xStart;
				var width = Math.max(v.domainLineMinWidth, 
						(domain['stop'] - domain['start']) * v.aaWidth - 2);
				var line = stage.rect(x, y, width, v.domainLineHeight).
					stroke('rgb(250, 162, 86)').
					fill('rgb(250, 162, 86)');
				setupDomainPopup (line, domain);
			}

			function draw (data) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				v.proteinWidth = getComputedStyle(div)['width'];
				v.proteinWidth = parseInt(
					v.proteinWidth.substring(0, v.proteinWidth.length - 2)) 
					- v.variantRadius - v.xEndPad - v.xStart;
				
				v.aalen = data['len'];
				v.aaWidth = v.proteinWidth / v.aalen;
				v.reftranscript = data['transcript'];
				
				drawControlPanel(data);
				drawMyVariants(data);
				drawProtein(data);
				setupOtherVariantDiv(data);
				setupSiteDiv(data);
                drawMyVariantsTable(data);
				
				v.drawing = false;
			}

            function drawMyVariantsTable (data) {
                var div = getEl('div');
                div.style.position = 'absolute';
                div.style.top = '50px';
                div.style.left = '4px';
                var contentDiv = document.getElementById('widgetcontentdiv_lollipop_gene');
                addEl(contentDiv, div);
                var table = getEl('table');
                table.className = 'lollipop_gene_varianttable';
                table.style.width = '160px';
                addEl(div, table);
                var thead = getEl('thead');
                var tr = getEl('tr');
                var th = getEl('th');
                th.style.fontSize = '8px';
                addEl(th, getTn('Change'));
                addEl(tr, th);
                var th = getEl('th');
                th.style.fontSize = '8px';
                addEl(th, getTn('Seq Ont'));
                addEl(tr, th);
                var th = getEl('th');
                th.style.fontSize = '8px';
                addEl(th, getTn('# Samples'));
                addEl(tr, th);
                addEl(thead, tr);
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
				var v = widgetGenerators[widgetName][tabName]['variables'];
                var myVariants = v['myvariants'];
                if (myVariants.length == 0) {
                    $(table).remove();
                    var sdiv = getEl('div');
                    sdiv.textContent = 'No variants map to';
                    sdiv.style.position = 'relative';
                    sdiv.style.left = '4px';
                    addEl(div, sdiv);
                    var sdiv = getEl('div');
                    sdiv.textContent = 'UniProt\'s canonical';
                    sdiv.style.position = 'relative';
                    sdiv.style.left = '4px';
                    addEl(div, sdiv);
                    var sdiv = getEl('div');
                    sdiv.textContent = 'transcript';
                    sdiv.style.position = 'relative';
                    sdiv.style.left = '4px';
                    addEl(div, sdiv);
                    return;
                }
                for (var i = 0; i < myVariants.length; i++) {
                    var variant = myVariants[i];
                    tr = getEl('tr');
                    td = getEl('td');
                    td.style.fontSize = '8px';
                    td.style.cursor = 'default';
                    td.addEventListener('mouseover', function (evt) {
                        var aachange = evt.target.textContent;
                        var circles = $('circle.lollipop_gene[aachange=' + aachange + ']');
                        for (var i = 0; i < circles.length; i++) {
                            var circle = circles[i];
                            circle.setAttribute('oldfill', circle.getAttribute('fill'));
                            circle.setAttribute('fill', 'black');
                        }
                    });
                    td.addEventListener('mouseout', function (evt) {
                        var aachange = evt.target.textContent;
                        var circles = $('circle.lollipop_gene[aachange=' + aachange + ']');
                        for (var i = 0; i < circles.length; i++) {
                            var circle = circles[i];
                            circle.setAttribute('fill', circle.getAttribute('oldfill'));
                        }
                    });
                    addEl(td, getTn(variant.refaa + variant.start + variant.altaa));
                    addEl(tr, td);
                    td = getEl('td');
                    td.style.fontSize = '8px';
                    addEl(td, getTn(variant.so));
                    addEl(tr, td);
                    td = getEl('td');
                    addEl(td, getTn(variant.count));
                    td.style.fontSize = '8px';
                    addEl(tr, td);
                    addEl(tbody, tr);
                }
            }

			function drawControlPanel (data) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				// Container
				var dsDiv = getEl('div');
				dsDiv.style.width = '100%';
				dsDiv.style.height = '20px';
				addEl(div, dsDiv);
			
				// Protein site datasource selector
				var partDiv = getEl('div');
				partDiv.style.display = 'inline-block';
				span = getEl('span');
				addEl(span, getTn('Track: '));
				addEl(partDiv, span);
				select = getEl('select');
				select.id = getProtSiteSourceSelectorId();
				select.className = 'detailwidgetselect';
				var datasources = Object.keys(data['domains']);
				datasources.sort();
				var option = new Option('', '');
				select.options.add(option);
				for (var i = 0; i < datasources.length; i++) {
					var datasource = datasources[i];
					var option = new Option(datasource, datasource);
					select.options.add(option);
				}
				select.addEventListener('change', function (evt) {
					var select = evt.target;
					while (select.selectedIndex == -1) {}
					var datasource = select.getAttribute('datasource');
					onChangeProtSiteDatasource(
							getSiteCanvasId(), 
							data, select.options[select.selectedIndex].value);
				});
				addEl(partDiv, select);
				addEl(dsDiv, partDiv);

				// Variant datasource selector
				var datasources = Object.keys(data['variants']);
				datasources.sort();
				var partDiv = getEl('div');
				partDiv.style.display = 'inline-block';
				var span = getEl('span');
				addEl(span, getTn('\xa0\xa0Reference variants from: '));
				addEl(partDiv, span);
				var select = getEl('select');
				select.id = getVarDatasourceSelectorId();
				select.className = 'detailwidgetselect';
				select.addEventListener('change', function (evt) {
					var select = evt.target;
					onChangeOtherVariantDatasource(select, data);
				});
				addEl(partDiv, select);
				var option = new Option('', '');
				select.options.add(option);
				for (var i = 0; i < datasources.length; i++) {
					var datasource = datasources[i];
					var option = new Option(datasource, datasource);
					select.options.add(option);
				}
				addEl(dsDiv, partDiv);
				
				// Variant category selector
				var partDiv = getEl('div');
				partDiv.id = getVarCategorySelectorDivId();
				partDiv.style.display = 'none';
				span = getEl('span');
				addEl(span, getTn('  (Category: '));
				addEl(partDiv, span);
				select = getEl('select');
				select.id = getVarCategorySelectorId();
				select.className = 'detailwidgetselect';
				select.addEventListener('change', function (evt) {
					var select = evt.target;
					var datasource = select.getAttribute('datasource');
					onChangeOtherVariantCategory(
							getOtherVarCanvasId(), 
							data, datasource, 
							select.options[select.selectedIndex].value);
				});
				addEl(partDiv, select);
				addEl(partDiv, addEl(getEl('span'), getTn(')')));
				addEl(dsDiv, partDiv);
			}

			function drawMyVariants (data) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				// Erases canvas for a new gene.
				var canvasId = getMyVarCanvasId();
				var canvas = document.getElementById(canvasId);
				if (canvas == undefined) {
					var dsDiv = getEl('div');
					dsDiv.style.width = '100%';
					dsDiv.style.height = v.varHeightMax + v.variantRadius;
					
					var canvas = getEl('div');
					canvas.id = canvasId;
					canvas.style.width = '100%';
					canvas.style.height = v.varHeightMax + v.variantRadius;
					addEl(dsDiv, canvas);
					
					addEl(div, dsDiv);
				} else {
					$(canvas).empty();
				}
				
				// Stage
				var stage = acgraph.create(canvas);
				var y = v.variantRadius;
				var varHeightInc = (v.varHeightMax - v.varHeightMin) / 
						v.maxVarNumSample;

				// Draws.u
                var v = widgetGenerators[widgetName][tabName]['variables'];
                v['myvariants'] = [];
                var variantRowNos = varByGene[v.hugo];
                var variantRows = infomgr.datas.variant;
                for (var i = 0; i < variantRowNos.length; i++) {
                    var row = variantRows[variantRowNos[i]];
                    var variant = getMyVariant(row);
                    if (Object.keys(variant).length == 0) {
                        continue;
                    }
                    v['myvariants'].push(variant);
                    if (variant != null && Object.keys(variant).length > 0) {
                        drawMyVariant(variant, stage, y, varHeightInc);
                    }
                }
			}

			function getMyVariant (row) {
				var allMappings = JSON.parse(infomgr.getRowValue('variant', row, 'base__all_mappings'));
				var hugos = Object.keys(allMappings);
				variant = {};
				for (var i = 0; i < hugos.length; i++) {
					var hugo = hugos[i];
					var uniprot_ds = allMappings[hugo];
					for (var j = 0; j < uniprot_ds.length; j++) {
						var transcript = uniprot_ds[j][3];
						if (transcript == v.reftranscript) {
							var protchange = uniprot_ds[j][1];
                            if (protchange == null) {
                                continue;
                            }
							variant['so'] = uniprot_ds[j][2];
							var refaa = protchange[0];
							var protchangelen = protchange.length;
							var altaa = protchange.substring(protchangelen - 1, protchangelen);
							var start = protchange.substring(1, protchangelen - 1);
							variant['start'] = start;
							variant['refaa'] = refaa;
							variant['altaa'] = altaa;
							variant['count'] = infomgr.getRowValue('variant', row, 'base__numsample');
							break;
						}
					}
				}
				return variant;
			}

			function drawProtein (data) {
				
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				// Protein container
				var dsDiv = getEl('div');
				dsDiv.style.width = '100%';
				dsDiv.style.height = '30px';
				dsDiv.setAttribute('datasource', datasource);
				addEl(div, dsDiv);
				
                // Transcript
                var tsDiv = getEl('div');
                tsDiv.style.position = 'absolute';
                tsDiv.style.bottom = '7px';
                tsDiv.style.right = '12px';
                tsDiv.textContent = v.reftranscript;
                addEl(div, tsDiv);
				
				// Protein canvas
				var canvas = getEl('div');
				var canvasId = getProtCanvasId();
				canvas.id = canvasId;
				canvas.style.width = '100%';
				canvas.style.height = '100%';
				addEl(dsDiv, canvas);
				
				// Protein stage
				var stage = acgraph.create(canvas);
				var y = 0;
				
				// Protein
				stage.rect(v.xStart, y, v.proteinWidth, v.proteinHeight).
					round(v.boxR, v.boxR, v.boxR, v.boxR).
					stroke('#555555').
					fill({
						keys: ['0 #aaaaaa', '0.6 #dddddd', '1 #aaaaaa'],
						angle: 90,
						
					});
				
				// Pfam boxes
				var datasource = 'pfam';
				if (data['domains'] != undefined && 
						data['domains'][datasource] != undefined) {
					var domains = data['domains'][datasource];
					for (var i = 0; i < domains.length; i++) {
						var domain = domains[i];
						drawBoxDomain(stage, domain, y);
					}
				}

                // My variant table
			}
			
			function setupOtherVariantDiv (data) {
				var v = widgetGenerators[widgetName][tabName]['variables'];
				var datasources = Object.keys(data['variants']);
				datasources.sort();
				var dsDiv = getEl('div');
				dsDiv.id = getOtherVarCanvasId();
				dsDiv.style.width = '100%';
				dsDiv.style.height = v.varHeightMax + v.variantRadius;
				addEl(div, dsDiv);
				var canvasId = dsDiv.id + '_canvas';
				
				var canvas = getEl('div');
				canvas.id = canvasId;
				canvas.style.width = '100%';
				canvas.style.height = v.varHeightMax + v.variantRadius;
				addEl(dsDiv, canvas);
			}
			
			function setupSiteDiv (data) {
				
				var v = widgetGenerators[widgetName][tabName]['variables'];
				
				var dsDiv = getEl('div');
				dsDiv.style.width = '100%';
				dsDiv.style.height = '30px';
				
				var canvas = getEl('div');
				var canvasId = getSiteCanvasId();
				canvas.id = canvasId;
				canvas.style.width = '100%';
				canvas.style.height = '100%';
				addEl(dsDiv, canvas);
				
				addEl(div, dsDiv);
			}
		}
	}
};
