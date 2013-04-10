$(function () {
    $('#graph_@QUERY_NUMBER').highcharts('StockChart', {
            chart: {
            },

            rangeSelector: {
                selected: 4
            },

            yAxis: {
                labels: {
                        formatter: function() {
                                return (this.value > 0 ? '+' : '') + this.value + '%';
                        }
                },
                plotLines: [{
                        value: 0,
                        width: 2,
                        color: 'silver'
                }]
            },
            
            plotOptions: {
                series: {
                        compare: 'percent'
                }
            },
            
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2
            },
            
            series: query_data[@QUERY_NUMBER]["data"]
        });
});
