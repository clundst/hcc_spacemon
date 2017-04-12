#!/bin/bash

## Grab latest fs image from /user/clundst in hadoop, process it and upload it
cd /grid_home/cmsphedex/spacemon

FSIMAGE=`ls -lct /mnt/hadoop/user/clundst/fs* | head -n 1 | awk '{print $9}'`
STAMPENDING="${FSIMAGE#*_}"
DUMPFILE=dumpfile.${STAMPENDING}
echo $DUMPFILE
cp $FSIMAGE ./fsimage.${STAMPENDING}
./format_fsimage_nocksum.py -i ./fsimage.${STAMPENDING} -o $DUMPFILE
./DMWMMON/SpaceMon/Utilities/spacemon --dump $DUMPFILE --node T2_US_Nebraska --verbose --upload-record
rm ./fsimage.${STAMPENDING}
rm $DUMPFILE
