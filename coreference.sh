if [ "$#" -ne 2 ]; then
    echo "Useage: coreference.sh <listfile> <output_directory>"
    exit 1
fi

# python coreference.py listfile.txt output/
python coreference.py "$1" "$2"
