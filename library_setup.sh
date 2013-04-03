#!/bin/bash
mkdir lib
cd lib
wget http://www.highcharts.com/downloads/zips/Highcharts-3.0.0.zip -O h.zip # get highcharts, call it something short for convienence later
mkdir highcharts
unzip h.zip -d highcharts/ # unzip highcharts into folder made for it
rm h.zip # clean up uneccessary downloads
