#!/bin/bash
# Copyright (C) Mellanox Technologies Ltd. 2001-2021.   ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Mellanox Technologies Ltd.
# (the "Company") and all right, title, and interest in and to the software product,
# including all associated intellectual property rights, are and shall
# remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.


set -eE

# removing log file
LOG_FILE=/opt/ufm/log/tfs.log
if test -f "$LOG_FILE"; then
    rm "$LOG_FILE"
fi

exit 0