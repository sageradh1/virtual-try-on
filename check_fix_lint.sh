#!/bin/bash

echo "Fixing code with Black..."
black app/

echo "Running Pylint..."
pylint app/

echo "Done!"
