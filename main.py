from TemplateExtract.extract import main as M_daoqie
from TemplateExtract_rob.first import main as M_rob
from TemplateExtract_dupin.extract_dupin import main as M_dupin


a=input('please input crime: ')
if a== 'A':
    print('A is daoqie')
elif a== 'B':
    print('B is Rob')
elif a== 'C':
    print("C is dupin")
else :
    print('no adequate crime')
