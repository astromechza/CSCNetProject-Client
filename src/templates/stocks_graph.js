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
				      formatter: function() {
	                  var s = Highcharts.dateFormat('%H:%M - %a, %b %e, %Y', this.x);

	                  $.each(this.points, function(i, point) {
	                      s += '<br/><span style="color:'+point.series.color+'; font-weight: bold;">'+point.series.name+':</span> '+Math.round(point.y*Math.pow(10,2))/Math.pow(10,2);
	                  });

	                  return s;
	                },
				      useHTML: true              
            },
            
            series: query_data[@QUERY_NUMBER]["data"]
        });
});
