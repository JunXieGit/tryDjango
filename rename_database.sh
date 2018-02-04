#!/bin/bash - 
#===============================================================================
#
#          FILE: rename_database.sh
# 
#         USAGE: ./rename_database.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 01/16/2018 14:10
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
mysqlconn="mysql -u root -p108668"
olddb=$1
newdb=$2
$mysqlconn -e "CREATE DATABASE $newdb"
params=$($mysqlconn -N -e "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES \
	                           WHERE table_schema='$olddb'")
for name in $params; do
	      $mysqlconn -e "RENAME TABLE $olddb.$name to $newdb.$name";
      done;
      $mysqlconn -e "DROP DATABASE $olddb"
