# -*- coding: utf-8 -*-
"""
27/07/2022 17:04
@author: Sam Mousavi s.mo.mousavi@gmail.com
"""

#!/usr/bin/env python
# coding: utf-8


import numpy as np
import h5py
import copy
import sys

#from sqlalchemy import false


# this data type is similar to matlab structure and can be used similar to Matlab notation (like a.b = 2)


class structtype:
    def __init__(self, **kwargs):
        self.Set(**kwargs)

    def Set(self, **kwargs):
        self.__dict__.update(kwargs)

    def SetAttr(self, lab, val):
        self.__dict__[lab] = val

    pass


class ReadMatH5:
    def __init__(self):
        self.test = 1
        self.string_offset = 1

    # Reads String from Mat file
    def read_string(self, h5Obj_, Var_obj_,offset_):
        Var_location_object = Var_obj_[0][4]
        String_vector = h5Obj_[h5Obj_.get("#subsystem#").get("MCOS")[0][Var_location_object + offset_]][:] # this is Var_location_object + 1 but for some resoin somtimes working only with not +1
        String_vector = np.delete(String_vector, [0, 1, 2, 3, 4])
        Stringg = ""
        for str_ in String_vector:
            Stringg = Stringg + bytes(np.array([str_])).decode("utf-16")
        Stringg = Stringg.replace("\x00", "")
        return Stringg

    # Reads char from Mat file
    def read_char(self, h5Obj_, Var_obj_):
        Char_ = bytes(Var_obj_[:]).decode("utf-16")
        Char_ = Char_.replace("\x00", "")
        return Char_

    # Reads array/matrix from Mat file
    def read_array(self, h5Obj_, Var_obj_,variable_type_):
        mat_out = np.array(Var_obj_)
        complex_matlab_dtype = [("real", "<f8"), ("imag", "<f8")]
        
        if complex_matlab_dtype == Var_obj_.dtype:
            mat_out = mat_out.view("complex")
            
        elif variable_type_ == "int8": 
            mat_out = mat_out.astype('int8')
        elif variable_type_ == "int16": 
            mat_out = mat_out.astype('int16')
        elif variable_type_ == "int32": 
            mat_out = mat_out.astype('int32')
        elif variable_type_ == "int64": 
            mat_out = mat_out.astype('int64')
        elif variable_type_ == "uint8": 
            mat_out = mat_out.astype('uint8')
        elif variable_type_ == "uint16": 
            mat_out = mat_out.astype('uint16')
        elif variable_type_ == "uint32": 
            mat_out = mat_out.astype('uint32')
        elif variable_type_ == "uint64": 
            mat_out = mat_out.astype('uint64')
        elif variable_type_ == "single": 
            mat_out = mat_out.astype('float32')
        elif variable_type_ == "double": 
            mat_out = mat_out.astype('float64')
        elif variable_type_ == "logical": 
            mat_out = mat_out.astype('bool')



        # if variable_type_ == "int8": 
        #     mat_out = np.int8(mat_out[0, 0])
        # if variable_type_ == "int16": 
        #     mat_out = np.int16(mat_out[0, 0])
        # if variable_type_ == "int32": 
        #     mat_out = np.int32(mat_out[0, 0])
        # if variable_type_ == "int64": 
        #     mat_out = np.int64(mat_out[0, 0])
        # if variable_type_ == "uint8": 
        #     mat_out = np.uint8(mat_out[0, 0])
        # if variable_type_ == "uint16": 
        #     mat_out = np.uint16(mat_out[0, 0])
        # if variable_type_ == "uint32": 
        #     mat_out = np.uint32(mat_out[0, 0])
        # if variable_type_ == "uint64": 
        #     mat_out = np.uint64(mat_out[0, 0])
        # if variable_type_ == "single": 
        #     mat_out = np.float32(mat_out[0, 0])
        # if variable_type_ == "double": 
        #     mat_out = np.uint8(mat_out[0, 0])
        if mat_out.shape == (1, 1): # this means we only have single value but not clear what is the type of the variable 
            mat_out = mat_out[0, 0]
        return mat_out

    ## detect the type of the variable
    # -- 'string' , 'char' , 'struct' , 'double' , 'Field Of Structure Array', 'StructArray' , 'çell'
    def var_type(self, Var_obj_):
        # check the type of the data
        try:
            type_of_data = Var_obj_.attrs.get("MATLAB_class").decode("utf-8")
        except:
            type_of_data = "Field Of Structure Array"  # it is a vector of references with the shape of (1 X number of element of structure) or (number of element of structure X 1)

        if type_of_data == "struct":
            fieldss = list(Var_obj_.keys())
            field_type = self.var_type(Var_obj_[fieldss[0]])
            if field_type == "Field Of Structure Array":
                type_of_data = "StructureArray"

        return type_of_data

    # Reads a Structure Array data type from Mat file

    def read_structure_array(self, h5Obj_, StrcArry_obj_):

        fields_names = list(StrcArry_obj_.keys())
        shape_Strcarray = StrcArry_obj_[fields_names[0]].shape
        VertArray = 0
        if shape_Strcarray[0] >= shape_Strcarray[1]:
            VertArray = 1
        StrcArryLen = max(
            StrcArry_obj_[fields_names[0]].shape
        )  # read the length of structure array by size of first field of it

        # -- create a list that content many dics as for each element of array and with field of the structure
        tempDic = dict.fromkeys(fields_names, None)
        main_strcArry = [copy.deepcopy(tempDic) for _ in range(StrcArryLen)]

        # read each field and fill it in the dic array
        if VertArray == 0:
            for field_name in fields_names:
                field_arry_obj = StrcArry_obj_[field_name]
                for indexx in range(StrcArryLen):
                    field_arry_element_ref = field_arry_obj[0, indexx]
                    field_element_obj = h5Obj_[field_arry_element_ref]
                    main_strcArry[indexx][field_name] = self.read_general_variable(h5Obj_, field_element_obj)
        else:
            for field_name in fields_names:
                field_arry_obj = StrcArry_obj_[field_name]
                for indexx in range(StrcArryLen):
                    field_arry_element_ref = field_arry_obj[indexx, 0]
                    field_element_obj = h5Obj_[field_arry_element_ref]
                    main_strcArry[indexx][field_name] = self.read_general_variable(h5Obj_, field_element_obj)
        return main_strcArry

    # Reads a Structure data type from Mat file
    def read_struct(self, h5Obj_, Strc_obj_):
        fields_names = list(Strc_obj_.keys())
        # -- create a dic as structure
        main_strc = dict.fromkeys(fields_names, None)

        # read each field and fill it in the dic array
        for field_name in fields_names:
            field_element_obj = Strc_obj_[field_name]
            main_strc[field_name] = self.read_general_variable(h5Obj_, field_element_obj)
        return main_strc

    # Reads a cell data type from Mat file
    def read_cell(self, h5Obj_, cell_obj_):  # this is for reading a cell

        main_cell = []

        for cell_elem_ref in cell_obj_:
            cell_elem_obj = h5Obj_[cell_elem_ref[0]]
            main_cell.append(self.read_general_variable(h5Obj_, cell_elem_obj))
        return main_cell

    # Reads a Variable with any of such types : 'string' , 'char' , 'struct' , 'double' , 'Field Of Structure Array' ,'StructureArray' from Mat file
    def read_general_variable(self, h5Obj_, Var_obj_):
        # find the type of variable
        variable_type = self.var_type(Var_obj_)
        
        numeric_list = ["int8","int16","int32","int64","uint8","uint16","uint32","uint64","single","double","logical"]
        
        # -- 'string' , 'char' , 'struct' , 'double' , 'Field Of Structure Array' ,'StructureArray'
        if variable_type == "string":
            Var_output = self.read_string(h5Obj_, Var_obj_,self.string_offset)
        elif variable_type == "char":
            Var_output = self.read_char(h5Obj_, Var_obj_)
        elif variable_type == "StructureArray":
            Var_output = self.read_structure_array(h5Obj_, Var_obj_)
        elif variable_type == "struct":
            Var_output = self.read_struct(h5Obj_, Var_obj_)
        elif variable_type == "cell":
            Var_output = self.read_cell(h5Obj_, Var_obj_)
        elif variable_type == "Field Of Structure Array":
            print("[Error] in using ReadGeneralVariable function")
            Var_output = 0
        elif variable_type == "missing":
            Var_output = None
            self.string_offset = self.string_offset - 1
        elif variable_type in numeric_list:
            Var_output = self.read_array(h5Obj_, Var_obj_,variable_type)    
        
        else:
            print("[Error] type" + variable_type +"data is not supported ")
            Var_output = 0
        return Var_output

    # Reads Mat file saved as h5 format (matlab saved data in -V7.3 format )
    def read_h5_to_py(self, h5Obj_):  #
        # extract keys = variable names
        var_names = list(h5Obj_.keys())
        del var_names[0:2]
        var_dic_out = {}
        for var_name in var_names:
            Var_obj = h5Obj_[var_name]
            var_dic_out[var_name] = self.read_general_variable(h5Obj_, Var_obj)

        return var_dic_out

    # receive a dictionary and return a structure similar to matlab
    def structs_like_Matlab(self, Input_Generaldic):
        fields_names = list(Input_Generaldic.keys())
        Out_dic = {}
        for field_name in fields_names:
            Out_dic[field_name] = self.dic_to_var(Input_Generaldic[field_name])
        return Out_dic

    def dic_to_var(self, Input_Var_):

        data_type = str(type(Input_Var_))
        if data_type.find("dict") != -1:  # it is structure
            fields_strct = list(Input_Var_.keys())
            Output_var = structtype()
            for field_name in fields_strct:
                Output_var.SetAttr(field_name, self.dic_to_var(Input_Var_[field_name]))

        if data_type.find("list") != -1:  # it is cell, structure array
            # check for strct arry or cell
            subdata_type = str(type(Input_Var_[0]))
            data_real_type = "cell"

            try:
                dic_list_1 = list(Input_Var_[0].keys())  # the first part of structure array

                if subdata_type.find("dict") != -1:  # it is most likely to be structure array
                    for indexx in range(len(Input_Var_)):  # all the elements of the list are similar

                        dic_list_2 = list(Input_Var_[indexx].keys())
                        if dic_list_2 != dic_list_1:
                            break
                        dic_list_1 = dic_list_2
                    data_real_type = "structArray"
            except:
                pass
            if data_real_type == "structArray":
                fields_strctArray = list(Input_Var_[0].keys())
                Output_var = [structtype() for _ in range(len(Input_Var_))]
                for indexx in range(len(Input_Var_)):
                    for field_name in fields_strctArray:
                        Output_var[indexx].SetAttr(field_name, self.dic_to_var(Input_Var_[indexx][field_name]))
            else:
                Output_var = []
                for indexx in range(len(Input_Var_)):
                    Output_var.append(self.dic_to_var(Input_Var_[indexx]))

        if data_type.find("numpy") != -1:  # it is any array or number
            Output_var = Input_Var_
        if data_type.find("str") != -1:  # it is any array or number
            Output_var = Input_Var_
        if data_type.find("NoneType") != -1:  # it is any array or number   
            Output_var = Input_Var_ 
        return Output_var

    def export_var_to_py_env(self, Input_Dic):
        module = sys.modules["__main__"]
        for name, value in Input_Dic.items():
            setattr(module, name, value)
        pass


# Main function to read and extract all the data from Mat file into Python
# StructsExportLikeMatlab = True ==> 'structures' and 'structure arrays' are saved exactly similar to Matlab notation (dot notation). if 0 the structures are saved as dictionaries
# ExportVar2PyEnv = True ==> variables are exported to Python environment with the same names as saved in the Mat file. If 0 the all the variables are exported as the keys and values of a single dictionary
def loadmatfile(file_Name_, StructsExportLikeMatlab=False, ExportVar2PyEnv=False):  # Main Function
    ReadClass = ReadMatH5()
    with h5py.File(file_Name_, "r") as f:
        Variable_output = ReadClass.read_h5_to_py(f)
    if StructsExportLikeMatlab:
        Variable_output = ReadClass.structs_like_Matlab(Variable_output)
    if ExportVar2PyEnv:
        ReadClass.export_var_to_py_env(Variable_output)
        Variable_output = "Variables are in the Env"
    return Variable_output



