# Coreference Resolution

A program for coreference resolution. Tested on CADE machine lab1-10.

## Input

### List Directory

A file containing a list of newline separated `.crf` files to find coreferences in.

*Example:*

```txt
files/test.crf
files/test.crf
files/test.crf
```

### Output Directory

The directory name to put the output of the the coreference resolver.

## Output

The coreference resolver will run on each file sepcified in the input and write the output to a new file inside the `outputFile` directory under the name`orignalFilename.response`.