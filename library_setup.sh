#!/bin/bash
mkdir lib
cd lib
wget http://www.highcharts.com/downloads/zips/Highcharts-3.0.0.zip -O h.zip
mkdir highcharts
unzip h.zip -d highcharts/
rm h.zip
