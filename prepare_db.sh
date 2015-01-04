#!/bin/bash

USER=calendall
PASS=calendall
DB=calendall


CMD="docker exec calendall_db_1 sudo -u postgres psql -c "
Q1="CREATE USER $USER WITH PASSWORD '$PASS';"
Q2="ALTER USER $USER CREATEDB;"
Q3="CREATE DATABASE $DB WITH OWNER $USER ENCODING 'UTF8';"
Q4="GRANT ALL PRIVILEGES ON DATABASE \"$DB\" to $USER;"

$CMD "$Q1"
$CMD "$Q2"
$CMD "$Q3"
$CMD "$Q4"