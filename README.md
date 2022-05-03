# Zendesk-Search-Project
To offer a simple command line application to search the provided data and return the results in a human readable format.

## Description
With the predefined three json files that are tickets, users and orgization, be capable of searching them by easy and simple keyboard inputs. Where the data exists, values from any related entities should be included in the results, i.e. searching organization by id should return its tickets and users. Whereby it accepts various kind of customized searching ways. And also be provided with a high scalability in the second time development.
On the perspective of result outputs, return values are displayed as a line with the column name and corresponding values. Also be equipped with the strong robustness that could handle and report errors.

## Getting Started
### Dependencies
* Any OS (Widnows, Unbuntu, MacOS and etc.) with Python 3.6+ installed.
* PowserShell for Windows, Bash Shell for Unbuntu and MacOS.

### Installing
* Install or update pip to the latest version
```
py -m pip install --upgrade pip
```
* Install the package with the following command line
```
pip install -i https://test.pypi.org/simple/ Zendesk-Search-GZ
```

### Executing program
* Start the python progress on the terminal
```
python
```
* Then execute the program by the following command line
```
from GZProject import ZendeskSearch
```

## Help
* Exactly matching search (Please keep the separator `@@`, and applies to any datatype of columns.)
```
equal@@searching-value
```
* Contains search (Please keep the separator `@@`, and only applies to `varchar` datatype columns.)
```
like@@searching-value
```

## Authors
* George Zhu 
* https://github.com/George-ZHUYZ

## Version History
* 0.0.1
    * Initial Release

## License
This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments
