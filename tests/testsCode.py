# -*- coding: utf-8 -*-
"""
27/07/2022 17:04
@author: Sam Mousavi s.mo.mousavi@gmail.com
"""

from cmath import nan
import os
import numpy as np
import unittest
import matdata2py as mtp

'''
try:
    from pygit2 import Repository
    import pkg_resources
    version = pkg_resources.get_distribution('mat73').version
except:
    version = '0.00'
try:
    repo = Repository('.')
    head = repo.head
    branch = head.shorthand
    name = head.name
    message = head.peel().message
except:
    branch = 'unknown'
    name = 'unknown'
    message = 'no msg'

print(f'#### Installed version: mat73-{version} on {branch}({name}) "{message}" ####')

'''

# file_Name = r"matlab_data.mat"

#%

# Variable_output = mtp.loadmatfile(file_Name, StructsExportLikeMatlab=1, ExportVar2PyEnv=0)
# print(type(Variable_output))

#%
# test class

class Test_code(unittest.TestCase):
    def setUp(self):
        #file_Name = 'DataTestFile.mat'
        print('==============>     Seting up test system  >>>>>')
        file_Name = r"Data_fileV2.mat"
        if not os.path.exists(file_Name):
            file_Name = os.path.join('./tests', file_Name)
        self.__setattr__ ('data_file_name', file_Name)

    def test_check(self):

        print('==============>     Loading data  >>>>>')
        Variables_output = mtp.loadmatfile(self.data_file_name, StructsExportLikeMatlab=True, ExportVar2PyEnv=False)
        print('==============>     Testing data  >>>>>')        
        assert len(Variables_output) == 35 
        assert len(Variables_output.keys())== 35   

        assert Variables_output['double_var']== 0.1
        assert Variables_output['double_var'].dtype==np.float64
        assert Variables_output['int16_var']==16
        assert Variables_output['int16_var'].dtype==np.int16
        assert Variables_output['int32_var']==1234
        assert Variables_output['int32_var'].dtype==np.int32  
        assert Variables_output['int64_var']==65432
        assert Variables_output['int64_var'].dtype==np.int64 
        assert Variables_output['int8_var']==2
        assert Variables_output['int8_var'].dtype==np.int8 
        
        
        assert Variables_output['single_var']==np.array(0.1, dtype=np.float32)
        assert Variables_output['single_var'].dtype==np.float32
        assert Variables_output['uint8_var']==2
        assert Variables_output['uint8_var'].dtype==np.uint8
        assert Variables_output['uint16_var']==12
        assert Variables_output['uint16_var'].dtype==np.uint16
        assert Variables_output['uint32_var']==5452
        assert Variables_output['uint32_var'].dtype==np.uint32       
        assert Variables_output['uint64_var']==32563
        assert Variables_output['uint64_var'].dtype==np.uint64
        
        assert Variables_output['string_var'] == 'String data String_data'
        assert Variables_output['string4'] == 'String data string4'
        assert Variables_output['string5'] == 'String data string5'
        assert Variables_output['string6'] == 'String data string6'


        np.testing.assert_array_equal(Variables_output['nan_var'], np.nan)
        assert Variables_output['nan_var'].dtype==np.float64

      
        np.testing.assert_array_equal(Variables_output['Vecor1_double_var'],np.array([[1.1],[1.2],[0.3]]))
        np.testing.assert_array_equal(Variables_output['array1_double_var'],np.array([[1., 3., 5.],[2., 4., 6.]]))
        np.testing.assert_array_equal(Variables_output['array2_double_var'],np.array([[[ 1.,  3.,  5.],[ 2.,  4.,  6.]],[[ 7.,  9., 11.],[ 8., 10., 12.]]]))
        np.testing.assert_array_equal(Variables_output['array_bool_var'],np.array([[ True],[ True],[False]]))
       
        np.testing.assert_array_equal(Variables_output['array_complex_var'],np.array([[0.999533882997283-2.09178468808884e-06j,
        0.999539919400443-1.81436764501457e-06j,
        0.999651865862015-7.43867650856539e-07j],
       [0.999409170859108-2.85697867929718e-07j,
        0.999414546785809-3.32833541326702e-07j,
        0.999434200429708-2.25400827270285e-07j],
       [0.999259301096249-1.43174900925348e-07j,
        0.999277976038325-5.91130796394622e-08j,
        0.999292494553505-6.89345078918961e-08j]]))

        np.testing.assert_array_equal(Variables_output['array_float_var'],np.array([[1.1, 2. ],[1.2, 3. ],[0.3, 4. ]],dtype=np.float32))
        np.testing.assert_array_equal(Variables_output['array_nan'],np.array([[ np.nan],[ np.nan]]))

        assert Variables_output['bool_var'] == False
        assert Variables_output['cell_char_var'] == ['Smith', 'Chung', 'Morales']
        
        assert Variables_output['complex_var'] == (2+3j)
        assert Variables_output['complex2_var'] == (123456789.12345679+987654321.9876543j)
        assert Variables_output['complex3_var'] == (0.000890908903500617+0j)
        
        assert Variables_output['missing_var'] == None
        assert Variables_output['missing1_var'] == None
        assert Variables_output['missing2_var'] == None
        assert Variables_output['char_var'] == 'char data char_var'

        # =============== test cell var
        cell_var = Variables_output['cell_var'] 
        np.testing.assert_array_equal(cell_var[0],np.array([[1.1],[2.2]]))
        assert cell_var[1] == True 
        np.testing.assert_array_equal(cell_var[2],np.array([[False],[ True]]))
        assert cell_var[3] == 1.1
        assert cell_var[3].dtype == np.float64 
        assert cell_var[4] == 0.0
        assert cell_var[4].dtype == np.float64 
        
        assert cell_var[5] == 'char data cell_car'
        assert cell_var[6] == 'String data cell_var'
        assert cell_var[7] == ['subcell', 0.0, 'check']
        
        # =============== test Cell1
        cell_var = Variables_output['Cell1']
        assert cell_var[0] == 'String data cell1'
        assert cell_var[1] == 'Char data cell1'
        assert cell_var[2] == 23.0
        assert cell_var[3] == 1.2

        np.testing.assert_array_equal(cell_var[4],np.array([[1., 3.],[2., 4.]]))

        # =============== test Structure_arrray
        struct_var = Variables_output['Structure_arrray']

        np.testing.assert_equal(struct_var[0].Double1,1.1)
        np.testing.assert_equal(struct_var[0].StringField,"Done1")
        np.testing.assert_array_equal(struct_var[0].Vector2,np.array([[1., 2., 3., 4., 5., 6.]]))
        np.testing.assert_array_equal(struct_var[0].Vectore3,np.array([[38.69096079517817],[np.nan]]))
        np.testing.assert_array_equal(struct_var[0].VectorComplex,np.array([[1.1+3.1j],[1.1+4.1j],[1.1+5.1j]]))

        np.testing.assert_equal(struct_var[0].Strucutre_1.String,'string Struc_array_1')
        np.testing.assert_equal(struct_var[0].Strucutre_1.complex1,(1+2j))
        np.testing.assert_equal(struct_var[0].Strucutre_1.double1,12.12)


        np.testing.assert_equal(struct_var[1].Double1,1.115)
        np.testing.assert_equal(struct_var[1].StringField,"Done2")
        np.testing.assert_array_equal(struct_var[1].Vector2,np.array([[1., 2., 3., 4., 5., 8.]]))
        np.testing.assert_array_equal(struct_var[1].Vectore3,np.array([[27.29626025330152 ],[26.998637477953995]]))
        np.testing.assert_array_equal(struct_var[1].VectorComplex,np.array([[1.1+3.1j],[1.1+4.1j],[1.1+5.1j]]))

        np.testing.assert_equal(struct_var[1].Strucutre_1.String,'string Struc_array_2')
        np.testing.assert_equal(struct_var[1].Strucutre_1.complex1,(1+2j))
        np.testing.assert_equal(struct_var[1].Strucutre_1.double1,12.12)

        np.testing.assert_equal(struct_var[2].Double1,1.1300000000000001)
        np.testing.assert_equal(struct_var[2].StringField,"Done3")
        np.testing.assert_array_equal(struct_var[2].Vector2,np.array([[1.,  2.,  5.,  7.,  9., 10.]]))
        np.testing.assert_array_equal(struct_var[2].Vectore3,np.array([[25.29793590453957],[25.51052360121637]]))
        np.testing.assert_array_equal(struct_var[2].VectorComplex,np.array([[1.1+3.1j],[1.1+4.1j],[1.1+5.1j]]))

        np.testing.assert_equal(struct_var[2].Strucutre_1.String,'string Struc_array_3')
        np.testing.assert_equal(struct_var[2].Strucutre_1.complex1,(1+2j))
        np.testing.assert_equal(struct_var[2].Strucutre_1.double1,12.12)

        # =============== test Structure_data
        Structure_data = Variables_output['Structure_data']
        np.testing.assert_array_equal(Structure_data.VectorNumber2,np.array([[1.1               , 1.115             , 1.1300000000000001,
        1.145             , 1.1600000000000001, 1.175             ,
        1.1900000000000002, 1.205             , 1.2200000000000002,
        1.235             , 1.25              , 1.2650000000000001,
        1.28              , 1.2950000000000002, 1.31              ]]))

        np.testing.assert_array_equal(Structure_data.VectorNumber1,np.array([[1.1               ],
       [1.115             ],
       [1.1300000000000001],
       [1.145             ],
       [1.1600000000000001],
       [1.175             ],
       [1.1900000000000002],
       [1.205             ],
       [1.2200000000000002],
       [1.235             ],
       [1.25              ]]))

        np.testing.assert_equal(Structure_data.Structure_data.singleDigit,1.0)


        np.testing.assert_equal(Structure_data.Char,'D12C09B1 str8 ')
        np.testing.assert_equal(Structure_data.String,'test string')
        np.testing.assert_array_equal(Structure_data.MatrixDouble1,np.array([[2.9983843749027489e+01, 2.5923812034359112e-01,
         4.0417842013594496e-02, 1.0625877668526745e-02,
         3.8902860887212337e-03, 1.7724323868406008e-03,
         9.4167358407144645e-04, 5.5996158554477476e-04,
         3.6241659446241582e-04, 2.4976838663141594e-04,
         1.8201590104043768e-04, 1.3844427331050966e-04],
        [2.9983843749027489e+01, 2.6643189203250378e-01,
         3.8668195526954892e-02, 9.9622481709728417e-03,
         3.6022735463152435e-03, 1.6297237030539317e-03,
         8.6344184938850045e-04, 5.1502758614091547e-04,
         3.3429427438070019e-04, 2.3276200460524844e-04,
         1.7069264140820152e-04, 1.3102573657307830e-04]]))

        np.testing.assert_array_equal(Structure_data.MatrixComplex,np.array([[0.9995338829972826-2.0917846880888414e-06j,
         0.9995399194004425-1.8143676450145702e-06j,
         0.9996518658620146-7.4386765085653872e-07j],
        [0.9994091708591079-2.8569786792971773e-07j,
         0.9994145467858089-3.3283354132670212e-07j,
         0.9994342004297083-2.2540082727028528e-07j],
        [0.9992593010962487-1.4317490092534823e-07j,
         0.9992779760383251-5.9113079639462167e-08j,
         0.9992924945535046-6.8934507891896113e-08j]]))

        print('<<<<<<<<<<<<<<<<<<   End of testing data (data imported correctly) >>>>>>>>>>>>>>>>>>>>')


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
if __name__ == '__main__':

    unittest.main()