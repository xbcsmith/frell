#!/bin/bash
set -x -v

NAME=$1

MODULE=$(echo $NAME|sed -e "s/-/_/g"|awk '{print tolower($0)}')

LIC="apache-2.0_stub.txt"
LICENSE="apache-2.0.txt"

echo "Name : $NAME"
echo "Module : $MODULE"

mkdir -p $MODULE

for f in constants.py main.py __init__.py;do
    cat ./src/$LIC ./src/$f > $MODULE/$f
    sed -i "s/@NAME@/${NAME}/g" $MODULE/$f
    sed -i "s/@MODULE@/${MODULE}/g" $MODULE/$f
done

for d in docs scripts;do 
    mkdir -p $d
    echo "${d^} go here" > $d/README
done

mkdir -p ./docs/manpages

for f in Makefile Make.rules Make.defs setup.py;do
    cp -v ./src/$f  $f
    sed -i "s/@NAME@/${NAME}/g" $f
    sed -i "s/@MODULE@/${MODULE}/g" $f
done 

for f in README.md TODO NEWS pylintrc testsuite.py;do
    cp -v ./src/$f $f
    sed -i "s/@NAME@/${NAME}/g" $f
done 

cat ./src/$LICENSE > LICENSE

cp -v ./src/gitignore .gitignore

echo "# REQUIREMENTS GO HERE" > requirements.txt

mkdir -p ./${MODULE}_tests

for tt in base_test.py errors.py logger.ini logger.py base_test_template.py clean_up.sh;do
    cat ./src/$tt > ./${MODULE}_tests/$tt
done

sed -i "s/@NAME@/${NAME}/g" ./${MODULE}_tests/*

echo "Don't forget to rm -rf .git"
