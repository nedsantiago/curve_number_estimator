# Project: Curve Number Estimator
# Written By: Ned Santiago
# Started on: 20230710 - July 10, 2023
# Goals: 
# 1. To stitch together all the curve number estimation calculators
# SUCCESSFUL: able to completely stitch together all the relevant calculators
#       into one python file
#
# 2. To create a modular calculator whereby each component has the potential
#       for use in other projects
# INCONCLUSIVE: will need to use these in other application other than SCS
#
# 3. To follow an object oriented programming approach to the project
# SUCCSESSFUL: multiple objects were built, each inspired by its respective python app
#
# 4. To quickly calculate for the curve numbers when given the subbasin areas
# SUCCESSFUL: calculation takes less than two (2) seconds according to 
#       Powershell's Measure-Command {start-process whateveryouwantexecute -Wait} Command
#
# 5. To have some capability to plugging into future projects such as
#       a qgis subbasin calculator, a gui graphics, or any automation tools
# INCONCLUSIVE: will need to attempt gui and qgis functionality
#
# VERSION 1.0.0 completed on 20230711 - July 11, 2023


import pandas as pd
import numpy as np
from os import path
import csv

def main():
   # overriding settings
    settings = SettingsCreator()
    # soil to hsg conversion
    dict_dir = r"test_data\float_correction_Loboc\soilTOhsgConversion_TagbilaranBohol.csv"
    settings.dict_dir(dict_dir)
    # curve number table
    cntable_dir = r"test_data\float_correction_Loboc\SCSCurveNumTable_Loboc.csv"
    settings.cn_dir(cntable_dir)
    # area of land use
    landuse_dir = r"test_data\float_correction_Loboc\area_luxsbLoboc_45sqkm.csv"
    settings.area_lu_dir(landuse_dir)
    # area of soil
    soil_dir = r"test_data\float_correction_Loboc\area_soilxsbLoboc_45sqkm.csv"
    settings.area_soil_dir(soil_dir)

    # store location of output folder
    output_folder = r"test_data\float_correction_Loboc\output"
    settings.output_folder_dir(output_folder)

    # begin main function
    df_soil = pd.read_csv(settings.area_soil_directory)
    df_lu = pd.read_csv(settings.area_lu_directory)
    df_scstable = pd.read_csv(settings.cn_file_directory)

    NAME = 'name'
    GRIDCODE = "GRIDCODE"
    SOILDESC = "SOILDESC"
    IMP = "imp"
    HSG = "HSG"
    AREA = "area"
    AREA_RATIO = "area_ratio"
    soil_dict_converter = DictionaryConverter(df_for_conversion=df_soil,
        col_from=SOILDESC, col_to=HSG, dict_directory=settings.dictionary_directory)

    hsg_areapercent_calculator = AreaPercentCalculator(df=soil_dict_converter.result,
        col1=NAME, col2=SOILDESC, val_col=AREA, new_col=AREA_RATIO)

    lu_areapercent_calculator = AreaPercentCalculator(df=df_lu,
        col1=NAME, col2=GRIDCODE, val_col=AREA, new_col=AREA_RATIO)

    cn_imp_calculator = CNImpCalculator(hsgxsb=hsg_areapercent_calculator.result,
        luxsb=lu_areapercent_calculator.result, scs_0=df_scstable, name_col=NAME,
        soildesc_col=SOILDESC, gridcode_col=GRIDCODE, val_col=AREA_RATIO, imp_col=IMP)
    
    cn_imp_calculator.print_to_csv(r"test_data\float_correction_Loboc\output\cn_imp_per_sb.csv")
    cn_imp_per_sb = cn_imp_calculator.result

# centralized singleton of all the options for the file
class SettingsCreator():
    """This class holds all the settings for the setup of the calculations.
    This includes the input folder, output folder, input file names, and output file
    name. It also checks the validity of each directory"""

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(SettingsCreator, self).__new__(self)
        return self.instance
    
    def _check_exists(self, file_path):
        assert (path.exists(file_path) == True), "The file/directory does not exist"
    
    def _check_has_output_directory(self):
        assert hasattr(self, "output_directory"), "declare output_folder_dir first"

    def dict_dir(self, dict_dir):
        self._check_exists(dict_dir)
        self.dictionary_directory = dict_dir
    
    def cn_dir(self, cn_dir):
        self._check_exists(cn_dir)
        self.cn_file_directory = cn_dir
    
    def area_lu_dir(self, area_lu):
        self._check_exists(area_lu)
        self.area_lu_directory = area_lu

    def area_soil_dir(self, area_soil):
        self._check_exists(area_soil)
        self.area_soil_directory = area_soil

    def output_folder_dir(self, output_folder):
        self._check_exists(output_folder)
        self.output_directory = output_folder
    
    def arearatio_lu_filename(self, arearatio_lu):
        self._check_has_output_directory()
        self.arearatio_lu_directory = path.join(self.output_directory, arearatio_lu)
    
    def arearatio_hsg_filename(self, arearatio_hsg):
        self._check_has_output_directory()
        self.arearatio_hsg_directory = path.join(self.output_directory, arearatio_hsg)

# Creating a parent class for the next classes
class ConverterCalculator():
    """This serves as the parent class. Child classes must declare an initialized
    calculation or conversion. Child classes will inherit the ability to return
    the result and print the result"""

    def result(self):
        """This method returns the resulting dataframe"""
        if self.result is not None:
            return self.result

    def print_to_csv(self, output_location):
        """This method prints the result dataframe into a csv file at a specified
        location and file name"""

        self.result.to_csv(output_location)

# converts a column's values to another set of values based on a provided dictionary
class DictionaryConverter(ConverterCalculator):
    """This class takes a csv file as a conversion dictionary and a file to convert.
    It produces the same table, but with one of its columns converted to a desired
    format, symbology, etc."""
    
    def __init__(self, df_for_conversion:pd.DataFrame, col_from, 
        col_to, dict_directory):
        # assert that all files must be a certain type
        assert type(df_for_conversion) is pd.DataFrame, "input must be a dataframe"
        assert type(dict_directory) is str, "input must be a string of the location"
        
        # open the dictionary table as dictionary
        with open(dict_directory, mode = 'r', encoding='utf-8-sig') as infile:
            dictreader = csv.DictReader(infile)
            mydict = {rows[col_from]:rows[col_to] for rows in dictreader}
        
        # replace the values of the specified column with conversion table
        self.result = df_for_conversion.replace({col_from:mydict})

# group values by a category and get each area's percentage
class AreaPercentCalculator(ConverterCalculator):
    """This class takes in categorized values with possible duplicate categories.
    It will calculate a row's ratio of the toal value in its respective category.
    For example, a name, landuse, and area categories.  The class will calculate
    the of a land use against the total area per name"""
    
    def __init__(self, df, col1, col2, val_col, new_col):
        # assertion checks
        assert type(df) == pd.DataFrame
        assert type(col1) == str
        assert type(col2) == str
        assert type(new_col) == str

        # group the dataframe primarily by col1 then col2, 
        # summing the values when grouping
        self.result = df.groupby([col1,col2]).sum()
        
        # making a new column which is the decimal (ratio) of each row to the total of 
        # the group
        self.result[new_col] = self.result[val_col] / self.result.groupby(col1)[val_col].transform('sum')

        # drop the irrelevant and old value column
        self.result = self.result.drop(labels=val_col, axis=1)
        self.result = self.result.reset_index()

# converts all the area percents into its equivalent curve number
class CNImpCalculator(ConverterCalculator):
    """This class is specifically built to calculate the equivalent curve number of a
    subbasin. The calculation assumes that the intersection of land use and soil type
    is a matter of chance rather than location, and the chances are based on the 
    area ratio of a classification"""
    
    def __init__(self, hsgxsb, luxsb, scs_0, name_col, soildesc_col, gridcode_col, val_col, imp_col):
        # gather the different dataframes
        # area ratio of HSGxSB
        assert type(hsgxsb) is pd.DataFrame, "needs to be a dataframe"
        self.hsgxsb = hsgxsb
        # area ratio of LUxSB
        assert type(luxsb) is pd.DataFrame, "needs to be a dataframe"
        self.luxsb = luxsb
        # get the SCS number table
        assert type(scs_0) is pd.DataFrame, "needs to be a dataframe"
        self.scs_0 = scs_0

        self.calculate(name_col, soildesc_col, gridcode_col, val_col, imp_col)

    def calculate(self, name_col, soildesc_col, gridcode_col, val_col, imp_col):
        # initialize the output lists
        # list of area ratio impervious
        imp_list = []
        # list of SCS Curve Numbers
        scs_list = []

        # list of subbasin names for iteration
        sb_list = self.hsgxsb[name_col].unique().tolist()
        # iterating through the subbasin list
        for subbasin in sb_list:
            # CALCULATE THE SCS NUMBER PER SUBBASIN

            # convert HSG into a vertical numpy matrix (n x 1)
            hsg_arr = self.hsgxsb[self.hsgxsb[name_col] == subbasin][[val_col]].to_numpy()
            # convert LU data into a horizontal numpy matrix of (1 x n)
            lu_arr = self.luxsb[self.luxsb[name_col] == subbasin][[val_col]].to_numpy().T

            # matrix multiply the HSG (n x 1) to LU (1 x n)
            hsgxlu = np.matmul(hsg_arr,lu_arr)

            # taking the SCS number table, remove irrelevant columns and rows
            # to know irrelevant cols and rows, get the list of hsg's and lu's for this iteration
            subbasin_hsgs = self.hsgxsb[self.hsgxsb[name_col] == subbasin][[soildesc_col]]
            subbasin_hsgs = subbasin_hsgs[soildesc_col].tolist()
            subbasin_lus = self.luxsb[self.luxsb[name_col] == subbasin][[gridcode_col]]
            subbasin_lus = subbasin_lus[gridcode_col].tolist()

            # after finding the parts that are relevant to this iteration,
            # convert to numpy array
            scsnum = self.scs_0.loc[self.scs_0[gridcode_col].isin(subbasin_lus)][subbasin_hsgs].to_numpy()
            
            # matrix multiply the the HSGxLU to the SCSnumtable
            sb_scsnum = np.matmul(hsgxlu, scsnum)

            # get the diagonal sum (trace) of the numpy array
            scs = np.trace(sb_scsnum)

            # append the result to the list of SCS numbers
            scs_list.append(scs)

            # GETTING THE IMPERVIOUS RATIO PER SUBBASIN

            # taking SCS number table, remove irrelevant (n x 1)
            imp_scs = self.scs_0.loc[self.scs_0[gridcode_col].isin(subbasin_lus)][imp_col].to_numpy()
            imp_scs = np.reshape(imp_scs, (imp_scs.shape[0],1))

            # using LU (1 x n)
            # matrix multiply imp ratio (n x 1) to LU (1 x n)
            imp_lu = np.matmul(lu_arr, imp_scs)

            # sum all the values in the product
            imp = np.sum(imp_lu)

            # append the value * 100 to the list of impervious ratios
            imp_list.append(imp * 100)
        
        # create a pandas dataframe using the Subbasin list as index
        # with one column for SCS number and another for imperviousness
        # self.result = the final dataframe
        self.result = pd.DataFrame({"SCS num":scs_list, imp_col:imp_list}, index=sb_list)


if __name__ == '__main__':
    main()