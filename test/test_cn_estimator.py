import cn_estimator
import pytest
import pandas as pd


def test_settings_singleton():
    settings1 = cn_estimator.SettingsCreator()
    settings2 = cn_estimator.SettingsCreator()

    assert (settings1 is settings2) == True

def is_same_output(a, b):
    assert a == b, f"\n{a} \n == \n{b}"

def test_settings_correct():
    settings = cn_estimator.SettingsCreator()

    # inputs
    dictionary_dir = r"input\soilTOhsgConversion_TagbilaranBohol.csv"
    curvenumbertable_dir = r"input\SCSCurveNumTable_TagbilaranCity.csv"
    area_lu_dir = r"input\area_luxsb01_TagbilaranBohol.csv"
    area_soil_dir = r"input\area_soilxsb01_TagbilaranBohol.csv"

    # outputs
    output_folder_directory = r"output"
    arearatio_lu_filename = r"arearatio_luxsb01_TagbilaranBohol.csv"
    arearatio_hsg_filename = r"arearatio_hsgxsb01_TagbilaranBohol.csv"

    # apply settings
    settings.dict_dir(dictionary_dir)
    settings.cn_dir(curvenumbertable_dir)
    settings.area_lu_dir(area_lu_dir)
    settings.area_soil_dir(area_soil_dir)

    # test outputs
    is_same_output(settings.dictionary_directory, dictionary_dir)
    is_same_output(settings.cn_file_directory, curvenumbertable_dir)
    is_same_output(settings.area_lu_directory, area_lu_dir)
    is_same_output(settings.area_soil_directory, area_soil_dir)

    # apply settings
    settings.output_folder_dir(output_folder_directory)
    settings.arearatio_lu_filename(arearatio_lu_filename)
    settings.arearatio_hsg_filename(arearatio_hsg_filename)

    # expected outputs
    arearatio_lu_directory = r"output\arearatio_luxsb01_TagbilaranBohol.csv"
    arearatio_hsg_directory = r"output\arearatio_hsgxsb01_TagbilaranBohol.csv"

    # test outputs
    is_same_output(settings.output_directory, output_folder_directory)
    is_same_output(settings.arearatio_lu_directory, arearatio_lu_directory)
    is_same_output(settings.arearatio_hsg_directory, arearatio_hsg_directory)

def test_settings_wrong():
    settings = cn_estimator.SettingsCreator()

    # inputs
    dictionary_dir = r"no_such_folder"
    curvenumbertable_dir = r"no_such_folder"
    area_lu_dir = r"no_such_folder"
    area_soil_dir = r"no_such_folder"

    # outputs
    output_folder_directory = r"no_such_folder"
    arearatio_lu_filename = r"no_such_file"
    arearatio_hsg_filename = r"no_such_file"

    with pytest.raises(AssertionError):
        settings.dict_dir(dictionary_dir)
    with pytest.raises(AssertionError):
        settings.cn_dir(curvenumbertable_dir)
    with pytest.raises(AssertionError):
        settings.area_lu_dir(area_lu_dir)
    with pytest.raises(AssertionError):
        settings.area_soil_dir(area_soil_dir)

def test_dictionary_converter():
    settings = cn_estimator.SettingsCreator()

    # inputs
    dictionary_dir = r"input\soilTOhsgConversion_TagbilaranBohol.csv"
    curvenumbertable_dir = r"input\SCSCurveNumTable_TagbilaranCity.csv"
    area_lu_dir = r"input\area_luxsb01_TagbilaranBohol.csv"
    area_soil_dir = r"input\area_soilxsb01_TagbilaranBohol.csv"

    # outputs
    output_folder_directory = r"output"
    arearatio_lu_filename = r"arearatio_luxsb01_TagbilaranBohol.csv"
    arearatio_hsg_filename = r"arearatio_hsgxsb01_TagbilaranBohol.csv"

    # apply settings
    settings.dict_dir(dictionary_dir)
    settings.cn_dir(curvenumbertable_dir)
    settings.area_lu_dir(area_lu_dir)
    settings.area_soil_dir(area_soil_dir)

    # apply settings
    settings.output_folder_dir(output_folder_directory)
    settings.arearatio_lu_filename(arearatio_lu_filename)
    settings.arearatio_hsg_filename(arearatio_hsg_filename)

    # convert soil into its equivalent Hydrologic Soil Group (HSG)
    df = pd.read_csv(filepath_or_buffer=area_soil_dir)
    # declare column to convert from
    col_to_convert = "SOILDESC"
    # declare the column to convert to
    col_output = "HSG"
    # begin conversion
    st_to_hsg = cn_estimator.DictionaryConverter(df_for_conversion=df,
        col_from=col_to_convert, col_to=col_output, 
        dict_directory=settings.dictionary_directory)

    csv_result = r"test_data\area_hsgxsb01_TagbilaranBohol.csv"
    expected_result = pd.read_csv(csv_result)
    
    assert expected_result.equals(st_to_hsg.result), f"""\nExpected Result:
    \n{expected_result}\n == \n
    {st_to_hsg.result()}"""

class test_group1:
    settings = cn_estimator.SettingsCreator()

    # inputs
    dictionary_dir = r"input\soilTOhsgConversion_TagbilaranBohol.csv"
    curvenumbertable_dir = r"input\SCSCurveNumTable_TagbilaranCity.csv"
    area_lu_dir = r"input\area_luxsb01_TagbilaranBohol.csv"
    area_soil_dir = r"input\area_soilxsb01_TagbilaranBohol.csv"

    # outputs
    output_folder_directory = r"output"
    arearatio_lu_filename = r"arearatio_luxsb01_TagbilaranBohol.csv"
    arearatio_hsg_filename = r"arearatio_hsgxsb01_TagbilaranBohol.csv"

    # apply settings
    settings.dict_dir(dictionary_dir)
    settings.cn_dir(curvenumbertable_dir)
    settings.area_lu_dir(area_lu_dir)
    settings.area_soil_dir(area_soil_dir)

    # apply settings
    settings.output_folder_dir(output_folder_directory)
    settings.arearatio_lu_filename(arearatio_lu_filename)
    settings.arearatio_hsg_filename(arearatio_hsg_filename)

    def test_dictionary_conversion(self):
        # convert soil into its equivalent Hydrologic Soil Group (HSG)
        df = pd.read_csv(filepath_or_buffer=self.area_soil_dir)
        # declare column to convert from
        col_to_convert = "SOILDESC"
        # declare the column to convert to
        col_output = "HSG"
        # begin conversion
        st_to_hsg = cn_estimator.DictionaryConverter(df_for_conversion=df,
            col_from=col_to_convert, col_to=col_output, 
            dict_directory=self.settings.dictionary_directory)

        csv_result = r"test_data\area_hsgxsb01_TagbilaranBohol.csv"
        expected_result = pd.read_csv(csv_result)
        
        assert expected_result.equals(st_to_hsg.result), f"""\nExpected Result:
        \n{expected_result}\n == \n
        {st_to_hsg.result()}"""

    def test_area_percent_hsg(self):
        self.test_dictionary_conversion()
        # columns to organize by
        col1 = "name"
        col2 = "SOILDESC"

        # columns to value by
        val_col = "area"

        # columns to create
        new_col = "area_ratio"

        # dataframe as input, should be the hsg and subbasin intersection
        hsgxsb_dir = r"test_data\area_hsgxsb01_TagbilaranBohol.csv"
        hsgxsb = pd.read_csv(hsgxsb_dir)

        # initialize the area percent calculator object
        areapercent_calc = cn_estimator.AreaPercentCalculator(df=hsgxsb, col1=col1,
            col2=col2, val_col=val_col, new_col=new_col)
        
        # assertion check
        arearatio_hsgxsb_dir = r"test_data\arearatio_hsgxsb01_TagbilaranBohol.csv"
        expected_df = pd.read_csv(arearatio_hsgxsb_dir).round(6)
        expected_result = list(expected_df['area_ratio'])
        actual_result = list(areapercent_calc.result['area_ratio'].round(6))
        assert (expected_result == actual_result)
        
def test_dictionary_conversion():
    test1 = test_group1()
    test1.test_dictionary_conversion()

def test_area_percent_calculator():
    test = test_group1()
    test.test_area_percent_hsg()

def test_cn_calculator():
    test = test_group1()


class testgroup_loboc():
    """This class is used for testing with the Loboc River dataset"""
    
    def __init__(self):
        #inputs

        # start test dataframes and lists
        # inputs
        dir_arearatio_hsgxsb = r"test_data\float_correction_Loboc\arearatio_hsgxsbLoboc_45sqkm.csv"
        self.input_hsgxsb = pd.read_csv(dir_arearatio_hsgxsb)

        dir_arearatio_luxsb = r"test_data\float_correction_Loboc\arearatio_luxsbLoboc_45sqkm.csv"
        self.input_luxsb = pd.read_csv(dir_arearatio_luxsb)

        dir_scs_0 = r"test_data\float_correction_Loboc\SCSCurveNumTable_Loboc.csv"
        self.input_scs_0 = pd.read_csv(dir_scs_0)
        # outputs
        dir_scsnum = r"test_data\float_correction_Loboc\CNperSB_Loboc_45sqkm.csv"
        self.output_list_scsnum = list(pd.read_csv(dir_scsnum)["SCS_num, #"].round(6))

        dir_imp = r"test_data\float_correction_Loboc\impperSB_Loboc_45sqkm.csv"
        self.output_list_imp = list(pd.read_csv(dir_imp)["imp, %"].round(6))
        # end test dataframes and lists

    def test_cn_calculator(self):
        # create a calculator object
        # use the previous parameters as inputs
        cn_calculator = cn_estimator.CNImpCalculator(
            hsgxsb=self.input_hsgxsb,
            luxsb=self.input_luxsb,
            scs_0=self.input_scs_0,
            name_col='name', 
            soildesc_col='SOILDESC',
            gridcode_col='GRIDCODE',
            val_col="area_ratio",
            imp_col="imp")
        results = cn_calculator.result

        # convert results to list for comparison
        actual_imp = results["imp"].round(6)
        actual_imp = actual_imp.values.tolist()
        actual_scsnum = results["SCS num"].round(6)
        actual_scsnum = actual_scsnum.values.tolist()
        
        # assert as the same lists
        assert actual_scsnum == self.output_list_scsnum, "final estimated scs #'s values do not match"
        assert actual_imp == self.output_list_imp, "final estimated imp values do not match"      


def test_whole():
    # overriding settings
    settings = cn_estimator.SettingsCreator()
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
    soil_dict_converter = cn_estimator.DictionaryConverter(df_for_conversion=df_soil,
        col_from=SOILDESC, col_to=HSG, dict_directory=settings.dictionary_directory)

    hsg_areapercent_calculator = cn_estimator.AreaPercentCalculator(df=soil_dict_converter.result,
        col1=NAME, col2=SOILDESC, val_col=AREA, new_col=AREA_RATIO)

    lu_areapercent_calculator = cn_estimator.AreaPercentCalculator(df=df_lu,
        col1=NAME, col2=GRIDCODE, val_col=AREA, new_col=AREA_RATIO)

    cn_imp_calculator = cn_estimator.CNImpCalculator(hsgxsb=hsg_areapercent_calculator.result,
        luxsb=lu_areapercent_calculator.result, scs_0=df_scstable, name_col=NAME,
        soildesc_col=SOILDESC, gridcode_col=GRIDCODE, val_col=AREA_RATIO, imp_col=IMP)
    
    cn_imp_per_sb = cn_imp_calculator.result
    


def test_group_loboc():
    test = testgroup_loboc()
    test.test_cn_calculator()


if __name__ == '__main__':
    test_group_loboc()
    test_whole()