$.getScript('/result/widgetfile/wgjbrowse/browser.bundle.js', function () {});

var widgetName = 'jbrowse';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'JBrowse Genome Browser',
		'width': 780,
		'height': 780,
		'callserver': false,
		'function': function (div) {
			var data = infomgr.getData('variant')
			var columns = infomgr.getColumns('variant')
			const features = data.map(variant => {
				const feature = {}
				columns.forEach((col, idx) => {
					if (variant[idx]) {
						feature[col.title.toLowerCase()] = variant[idx]
					}
				});
				feature.seq_id = feature['chrom']
				feature.start = feature['position']
				feature.end = feature['position'] + feature['ref base'].length
				feature.name = feature['uid']
				return feature
			})
			div.id = 'GenomeBrowser'
			div.className = 'jbrowse'

			var config = {
				containerID: 'GenomeBrowser',
				dataRoot: undefined,
				baseUrl: '.',
				browserRoot: '/result/widgetfile/wgjbrowse/',
				update_browser_title: false,
				forceTracks: 'GRCH38 Reference Sequence,Variants',
				show_tracklist: false,
				defaultLocation: 'chr1:0..1000000000000',
				refSeqOrder: 'by_list',
				refSeqOrderList: [
					'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY'
				],
				refSeqs: {
					url: 'https://s3.amazonaws.com/1000genomes/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa.fai',
				},
				tracks: [
					{
						key: 'GRCH38 Reference Sequence',
						label: 'GRCH38 Reference Sequence',
						urlTemplate: 'https://s3.amazonaws.com/1000genomes/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa'
					},
					{
						key: 'Variants',
						label: 'Variants',
						storeClass: 'JBrowse/Store/SeqFeature/FromConfig',
						features: features,
						type: 'CanvasVariants'
					}
				]
			};
	
			window.JBrowse = new window.Browser(config);
		}
	}
};
