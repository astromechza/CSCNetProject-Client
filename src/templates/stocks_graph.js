$(function () {
    $('#graph_@QUERY_NUMBER').highcharts('StockChart', {
            chart: {
		            zoomType: 'x'
            },

            rangeSelector: {
				      buttons: [{
				          type: 'hour',
				          count: 1,
				          text: '1h'
				        }, {
				          type: 'day',
				          count: 1,
				          text: '1d'
				        }, {
				          type: 'all',
				          text: 'All'
				      }],
				      selected: 1
            },

            yAxis: {
                title: { text: 'Reading value' }
            },
            
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2
            },
            
            series: query_data[@QUERY_NUMBER]["data"]
        });
});
