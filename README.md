# gtest_json2html

This is handy Python3 script to generate a html file(s) from googletest json output.

This script assumes the gtest json output is from gtest version 1.8.x or later

## Platforms
* Linux, FreeBSD, OpenBSD, Solaris, AIX
* Windows
* macOS

## Usage

First generate the json report:

Run your googletest executable with the --gtest_output option:

```bash
./gtest-mytests --gtest_output=json:test-results.json
```

Convert the the test report file to html:

```bash
python3 gtest_json2html.py test-results.json output/index.html
```

All the generated HTML output in in directory `output`.

Open the file `output/index.html` with your favorite browser.

