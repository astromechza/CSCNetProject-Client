$(function () {
        $('#graph_@QUERY_NUMBER').highcharts({
            chart: {
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: query_data[@QUERY_NUMBER].title,
                x: -20 //center
            },
            subtitle: {
                text: query_data[@QUERY_NUMBER].subtitle,
                x: -20
            },
            xAxis: {
                categories: query_data[@QUERY_NUMBER].dates
            },
            yAxis: {
                title: {
                    text: query_data[@QUERY_NUMBER].y_axis_legend
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: query_data[@QUERY_NUMBER].data_type
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: query_data[@QUERY_NUMBER].data
        });
    });
