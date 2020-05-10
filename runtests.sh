#!/bin/bash

# from realpython/lessons/installable-single-package

find . -name "*.pyc" -exec rm {} \;
coverage run -p --source=tests,pirobot -m unittest
if [ "$?" = "0" ]; then
    coverage combine
    echo -e "\n\n============================================"
    echo "Test Coverage"
    coverage report
    echo -e "\n run \"coverage html\" for full report"
    echo -e "\n"

    # pyflakes or pep8 or others should go here
fi