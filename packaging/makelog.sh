#!/bin/bash

mainlog="CHANGELOG" # master log file
debianlog="debian/changelog" # log generated for debian packaging
pypilog="../library/CHANGELOG.txt" # log generated for pypi packaging

# generate debian changelog

cat $mainlog > $debianlog

# generate pypi changelog

sed -e "/--/d" -e "s/  \*/\*/" \
    -e "s/.*\([0-9].[0-9].[0-9]\).*/\1/" \
    -e '/[0-9].[0-9].[0-9]/ a\
    -----' $mainlog | cat -s > $pypilog

exit 0
