# MatData2Py

This library imports Matlab data saved in V7.3 format to python

A few important features: 

1 - loading most type of Matlab variables such as: vectors, arrays (n dimension), **_string_**, char, structure, **_structure array_**, cell, cell array and all different type of numerical precisions as well as boolean etc.(tables, timeframe are not supported yet) 

NOTE: This lib can correctly import **_string_** or **_strcutre arrays_** variable types 

2- The structure data type of matlab can be presented as either dictionary data type in python or dot presented version in python similar to matlab,

3- the variables in matlab file can be all exported in single dictionary or they can be exported as individual variables in python environment 


### Installation
```
pip install matdata2py
```

### Get started
How to use this lib:

```Python

import matdata2py as mtp

# load Matlab data file  
# StructsExportLikeMatlab = True/False structures are exported in dictionary format or dot base reference format similar to matlab 
# ExportVar2PyEnv = True/False export all variables in single dictionary or as separate individual variables into python environment  

Variables_output = mtp.loadmatfile(file_Name, StructsExportLikeMatlab=True, ExportVar2PyEnv=False)
print(Variables_output.keys())


```
