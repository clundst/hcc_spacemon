#!/bin/bash
FSIMAGE_TMP=/root/clundst/fsimage_tmp.txt
DATESTAMP=`date +%s`
ANFSIMAGE=`ls /hadoop-data1/checkpoints/current/fsimage* | grep -v md5 | head -n 1`
echo $ANFSIMAGE
NAME=`echo $ANFSIMAGE | sed "s/\/hadoop-data1\/checkpoints\/current\///"`
echo $NAME
cp $ANFSIMAGE $NAME
hdfs oiv -i $NAME -o $FSIMAGE_TMP
hdfs dfs -cp file:///$FSIMAGE_TMP /user/clundst/fsimage_${DATESTAMP}.txt
rm $NAME
rm $FSIMAGE_TMP
