from .libsteps import pylibsteps
from ctypes import c_char_p
import platform
import os
global STEPS_LIB

class STEPS():
    """
    Common usage to build a simulator with STEPS:
        1) simulator = STEPS(is_default=True, log_file="") # use default simulator, disable log file and show information to stdout.
        2) simulator = STEPS(is_default=True, log_file="case.log") # use default simulator, save log to case.log file.
        3) simulator = STEPS(is_default=False, log_file="") # create new simulator, disable log file and show information to stdout.
        4) simulator = STEPS(is_default=False, log_file="case.log") # create new simulator, save log to case.log file.
    """
        
    def __init__(self, is_default=False, log_file=""):
        """
        STEPS initialization.
        """
        global STEPS_LIB
        if 'STEPS_LIB' not in globals():
            STEPS_LIB = pylibsteps.load_library()
        if is_default==True:
            self.toolkit_index = STEPS_LIB.api_get_const_INDEX_NOT_EXIST()
        else:
            log_file = self.__get_c_char_p_of_string(log_file)
            self.toolkit_index = STEPS_LIB.api_generate_new_toolkit(log_file)
        
    def __del__(self):
        """
        STEPS destruction.
        """
        global STEPS_LIB
        if 'STEPS_LIB' in globals():
            STEPS_LIB.api_delete_toolkit(self.toolkit_index)

    def __extract_single_bus_device_id(self, did):
        """
        Private function to extract bus and identifier from single bus device id tuple.
        Args:
            (1) did: tuple in the format of (bus, ickt) where bus should be a positive number, and ickt should be a string.
        Rets:
            (1) bus: integer, device bus number.
            (2) ickt: string, device identifier.
        """
        bus = did[0]
        ickt = did[1]
        return bus, ickt

    def __extract_double_bus_device_id(self, did):
        """
        Private function to extract bus and identifier from two bus device id tuple.
        Args:
            (1) did: tuple in the format of (ibus, jbus, ickt) where ibus and jbus should be a positive number, and ickt should be a string.
        Rets:
            (1) ibus: integer, device first bus number.
            (2) jbus: integer, device second bus number.
            (3) ickt: string, device identifier.
        """
        ibus = did[0]
        jbus = did[1]
        ickt = did[2]
        return ibus, jbus, ickt
    
    def __extract_triple_bus_device_id(self, did):
        """
        Private function to extract bus and identifier from three bus device id tuple.
        Args:
            (1) did: tuple in the format of (ibus, jbus, kbus, ickt) where ibus and jbus should be a positive number, kbus should be non-negative, and ickt should be a string.
        Rets:
            (1) ibus: integer, device first bus number.
            (2) jbus: integer, device second bus number.
            (3) kbus: integer, device third bus number.
            (4) ickt: string, device identifier.
        """
        ibus = did[0]
        jbus = did[1]
        kbus = 0
        ickt = did[-1]
        if len(did)>3:
            kbus = did[2]
        return ibus, jbus, kbus, ickt
        
    def __get_c_char_p_of_string(self, data):
        """
        Private function to get the char* pointer of C Language from the input string data. It is usually used to pass Python string to STEPS kernel.
        Args:
            (1) data: Python string.
        Rets:
            (1) char* pointer. If Python version is not 2 or 3, None will be returned.
        """
        python_version = platform.python_version_tuple()
        python_version = python_version[0]
        if python_version == '3':
            return c_char_p(bytes(data, 'utf-8'))
        elif python_version == '2':
            return c_char_p(bytes(data))
        else:
            return None
            
    def __get_string_from_c_char_p(self, data):
        """
        Private function to get the Python string from the char* pointer of C Language. It is usually used to pass the char* of STEPS kernel to Python string.
        Args:
            (1) data: char* pointer.
        Rets:
            (1) Python string.
        """
        python_version = platform.python_version_tuple()
        python_version = python_version[0]
        if python_version == '3':
            return str(data, encoding='utf-8')
        elif python_version == '2':
            return str(data)
        else:
            return None
            
    def set_toolkit_log_file(self, log_file="", log_file_append_mode=False):
        """
        Set toolkit log file. The default mode is to write to new file.
        Args:
            (1) log_file: string, target log file name. If no file is set (""), the log will be exported to stdout.
            (2) log_file_append_mode: boolean, log file append mode. True for writting to new file, False for appending to existing file. Default is False.
        Rets: N/A
        """
        global STEPS_LIB
        log_file = self.__get_c_char_p_of_string(log_file)
        STEPS_LIB.api_set_toolkit_log_file(log_file, log_file_append_mode, self.toolkit_index)
        return      

    def set_parallel_thread_number(self, num=1):
        """
        Set parallel thread number for parallel simulation.
        Args:
            (1) num: integer, parallel thread number. If num=1, serial simulation is used. num should be < number of CPU physical cores.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_set_toolkit_parallel_thread_number(num, self.toolkit_index)
        return
        
    def get_parallel_thread_number(self):
        """
        Set parallel thread number for parallel simulation.        
        Args: N/A
        Rets:
            (1) parallel thread number, integer
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_toolkit_parallel_thread_number(self.toolkit_index)

    def set_dynamic_model_database_capacity(self, cap=10000000):
        """
        Set capacity of dynamic model database. If the capacity is not enough, dynamic data cannot be successfully loaded.
        Args:
            (1) cap: integer, database capacity, in bytes.
        Rets:
            (1) N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_set_toolkit_dynamic_model_database_capacity(cap, self.toolkit_index)
        return
        
    def get_dynamic_model_database_capacity(self):
        """
        Get capacity of dynamic model database. 
        Args: N/A
        Rets:
            (1) database capacity in bytes, integer
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_toolkit_dynamic_model_database_capacity(self.toolkit_index)
        
    def clear_toolkit(self):
        """
        Clear all data in the toolkit.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_clear_toolkit(self.toolkit_index)
        return
    
    def get_toolkit_float_data(self, dataname):
        """
        Get toolkit general float data.
        Args:
            (1) dataname: String of variable name.
        Rets:
            (1) Value of the variable. 0 if the variable name is invalid.
        """
        global STEPS_LIB
        dataname = self.__get_c_char_p_of_string(dataname)
        return STEPS_LIB.api_get_toolkit_float_data(dataname, self.toolkit_index)

    def set_toolkit_float_data(self, dataname, value):
        """
        Set toolkit general float data.
        Args:
            (1) dataname: String of variable name.
            (2) value: Value to set.
        Rets: N/A
        """
        global STEPS_LIB
        dataname = self.__get_c_char_p_of_string(dataname)
        return STEPS_LIB.api_set_toolkit_float_data(dataname, value, self.toolkit_index)
    
    def get_system_base_power_in_MVA(self):
        """
        Get toolkit system base power.
        Args: N/A
        Rets:
            (1) System base power in MVA.
        """
        global STEPS_LIB
        return self.get_toolkit_float_data("SBASE")
    
    def set_system_base_power_in_MVA(self, sbase):
        """
        Set toolkit system base power.
        Args:
            (1) sbase: System base power in MVA.
        Rets: N/A
        """
        global STEPS_LIB
        return self.set_toolkit_float_data("SBASE", sbase)
    
    def get_toolkit_string_data(self, dataname):
        """
        Get toolkit general string variable.
        Args:
            (1) dataname: String of variable name.
        Rets:
            (1) String to variable.
        """
        global STEPS_LIB
        dataname = self.__get_c_char_p_of_string(dataname)
        return self.__get_string_from_c_char_p(STEPS_LIB.api_get_toolkit_string_data(dataname, self.toolkit_index))

    def set_toolkit_string_data(self, dataname, value):
        """
        Set toolkit general string variable.
        Args:
            (1) dataname: String of variable name.
            (2) value: String to set.
        Rets: N/A
        """
        global STEPS_LIB
        dataname = self.__get_c_char_p_of_string(dataname)
        value = self.__get_c_char_p_of_string(value)
        return STEPS_LIB.api_set_toolkit_string_data(dataname, value, self.toolkit_index)
    
    def get_case_information(self):
        """
        Get case information string.
        Args: N/A
        Rets:
            (1) String of case information.
        """
        return self.get_toolkit_string_data("CASE INFORMATION")
    
    def get_case_additional_information(self):
        """
        Get case additional information string.
        Args: N/A
        Rets:
            (1) String of case additional information.
        """
        return self.get_toolkit_string_data("CASE ADDITIONAL INFORMATION")
    
    def set_case_information(self, value):
        """
        Set case information.
        Args:
            (1) value: String of case information.
        Rets: N/A
        """
        return self.set_toolkit_string_data("CASE INFORMATION", value)
    
    def set_case_additional_information(self, value):
        """
        Set case additional information string.
        Args:
            (1) value: String of case additional information.
        Rets: N/A
        """
        return self.set_toolkit_string_data("CASE ADDITIONAL INFORMATION", value)    

    def get_toolkit_bool_data(self, dataname):
        """
        Get toolkit general boolean data.
        Args:
            (1) dataname: String of variable name.
        Rets:
            (1) Boolean value of given dataname. If data name is invalid, False is returned.
        """
        global STEPS_LIB
        dataname = self.__get_c_char_p_of_string(dataname)
        return STEPS_LIB.api_get_toolkit_bool_data(dataname, self.toolkit_index)        

    def set_toolkit_bool_data(self, dataname, value):
        """
        Set toolkit general boolean data.
        Args:
            (1) dataname: String of variable name.
            (2) value: Boolean value.
        Rets: N/A
        """
        global STEPS_LIB
        dataname = self.__get_c_char_p_of_string(dataname)
        return STEPS_LIB.api_set_toolkit_bool_data(dataname, value, self.toolkit_index)
    
    def get_toolkit_detailed_log_logic(self):
        """
        Get toolkit detailed log logic.
        Args: N/A
        Rets: 
            (1) Boolean value of the detailed log logic. True if detailed log is enabled, False if otherwise.
        """
        global STEPS_LIB
        return self.get_toolkit_bool_data("DETAILED LOG LOGIC")
    
    def set_toolkit_detailed_log_logic(self, logic):
        """
        Set toolkit detailed log logic.
        Args:
            (1) logic: True to enable detailed log, False to disable detailed log.
        Rets: N/A
        """
        global STEPS_LIB
        return self.set_toolkit_bool_data("DETAILED LOG LOGIC", logic)
    

    def get_allowed_maximum_bus_number(self):
        """
        Get allowed maximum bus number.
        Args: N/A
        Rets:
            (1) Allowed maximum bus number.
        """
        global STEPS_LIB
        return int(STEPS_LIB.api_get_allowed_maximum_bus_number(self.toolkit_index))

    def set_allowed_maximum_bus_number(self, max_bus_number):
        """
        Set allowed maximum bus number. All buses in the database should be less than the give max bus number.
        Args:
            (1) max_bus_number: Allowed maximum bus number.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_set_allowed_maximum_bus_number(max_bus_number, self.toolkit_index)

    def get_bus_capacity(self):
        """
        Get capacity for storing buses in database.
        Args: N/A
        Rets:
            (1) Maximum number of buses that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("BUS")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_generator_capacity(self):
        """
        Get capacity for storing generators in database.
        Args: N/A
        Rets:
            (1) Maximum number of generators that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Generator")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_wt_generator_capacity(self):
        """
        Get capacity for storing wind turbine generators in database.
        Args: N/A
        Rets:
            (1) Maximum number of wind turbine generators that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("WT Generator")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_pv_unit_capacity(self):
        """
        Get capacity for storing PV units in database.
        Args: N/A
        Rets:
            (1) Maximum number of PV units that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("PV Unit")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_load_capacity(self):
        """
        Get capacity for storing loads in database.
        Args: N/A
        Rets:
            (1) Maximum number of loads that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Load")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_fixed_shunt_capacity(self):
        """
        Get capacity for storing fixed shunts in database.
        Args: N/A
        Rets:
            (1) Maximum number of fixed shunts that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Fixed Shunt")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_line_capacity(self):
        """
        Get capacity for storing transmission lines in database.
        Args: N/A
        Rets:
            (1) Maximum number of transmission lines that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Line")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_transformer_capacity(self):
        """
        Get capacity for storing transformers in database.
        Args: N/A
        Rets:
            (1) Maximum number of transformers that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Transformer")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_hvdc_capacity(self):
        """
        Get capacity for storing HVDC links in database.
        Args: N/A
        Rets:
            (1) Maximum number of HVDC links that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("HVDC")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_equivalent_device_capacity(self):
        """
        Get capacity for storing equivalent devices in database.
        Args: N/A
        Rets:
            (1) Maximum number of equivalent devices that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Equivalent Device")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_energy_storage_capacity(self):
        """
        Get capacity for storing energy storages in database.
        Args: N/A
        Rets:
            (1) Maximum number of energy storages that can be stored in the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Energy Storage")
        return int(STEPS_LIB.api_get_device_capacity(device, self.toolkit_index))
        
    def get_area_capacity(self):
        """
        Get capacity for storing areas in database.
        Args: N/A
        Rets:
            (1) Maximum number of areas that can be stored in the database.
        """
        global STEPS_LIB
        return int(STEPS_LIB.api_get_area_capacity(self.toolkit_index))
        
    def get_zone_capacity(self):
        """
        Get capacity for storing zones in database.
        Args: N/A
        Rets:
            (1) Maximum number of zones that can be stored in the database.
        """
        global STEPS_LIB
        return int(STEPS_LIB.api_get_zone_capacity(self.toolkit_index))
        
    def get_owner_capacity(self):
        """
        Get capacity for storing owners in database.
        Args: N/A
        Rets:
            (1) Maximum number of owners that can be stored in the database.
        """
        global STEPS_LIB
        return int(STEPS_LIB.api_get_owner_capacity(self.toolkit_index))

    def set_bus_capacity(self, capacity):
        """
        Set capacity for storing buses in database.
        Args:
            (1) capacity: Maximum number of buses that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("BUS")
        return STEPS_LIB.api_set_device_capacity("BUS", capacity, self.toolkit_index)
        
    def set_generator_capacity(self, capacity):
        """
        Set capacity for storing generators in database.
        Args:
            (1) capacity: Maximum number of generators that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Generator")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_wt_generator_capacity(self, capacity):
        """
        Set capacity for storing wind turbine generators in database.
        Args:
            (1) capacity: Maximum number of wind turbine generators that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Wt Generator")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
    def set_pv_unit_capacity(self, capacity):
        """
        Set capacity for storing PV units in database.
        Args:
            (1) capacity: Maximum number of PV units that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("PV Unit")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_load_capacity(self, capacity):
        """
        Set capacity for storing loads in database.
        Args:
            (1) capacity: Maximum number of loads that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Load")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_fixed_shunt_capacity(self, capacity):
        """
        Set capacity for storing fixed shunts in database.
        Args:
            (1) capacity: Maximum number of fixed shunts that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Fixed Shunt")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_line_capacity(self, capacity):
        """
        Set capacity for storing transmission lines in database.
        Args:
            (1) capacity: Maximum number of transmission lines that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Line")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_transformer_capacity(self, capacity):
        """
        Set capacity for storing transformers in database.
        Args:
            (1) capacity: Maximum number of transformers that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Transformer")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_hvdc_capacity(self, capacity):
        """
        Set capacity for storing HVDC links in database.
        Args:
            (1) capacity: Maximum number of HVDC links that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("HVDC")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_equivalent_device_capacity(self, capacity):
        """
        Set capacity for storing equivalent devices in database.
        Args:
            (1) capacity: Maximum number of equivalent devices that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Equivalent Device")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_energy_storage_capacity(self, capacity):
        """
        Set capacity for storing energy storages in database.
        Args:
            (1) capacity: Maximum number of energy storages that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Energy Storage")
        return STEPS_LIB.api_set_device_capacity(device, capacity, self.toolkit_index)
        
    def set_area_capacity(self, capacity):
        """
        Set capacity for storing areas in database.
        Args:
            (1) capacity: Maximum number of areas that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        return STEPS_LIB.api_set_area_capacity(capacity, self.toolkit_index)
        
    def set_zone_capacity(self, capacity):
        """
        Set capacity for storing zones in database.
        Args:
            (1) capacity: Maximum number of zones that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        return STEPS_LIB.api_set_zone_capacity(capacity, self.toolkit_index)
        
    def set_owner_capacity(self, capacity):
        """
        Set capacity for storing owners in database.
        Args:
            (1) capacity: Maximum number of owners that can be stored in the database.
        Rets: N/A
        Tips:
            This function SHOULD be called before adding devices to the database.
        """
        global STEPS_LIB
        return STEPS_LIB.api_set_owner_capacity(capacity, self.toolkit_index)

    def load_powerflow_data(self, file, ftype):
        """
        Load powerflow data from file.
        Args:
            (1) file: string, source powerflow file name.
            (2) ftype: string, powerflow data format.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_load_powerflow_data_from_file(file, ftype, self.toolkit_index)

    def save_powerflow_data(self, file, ftype, export_zero_line=True, export_out_of_service_bus=True, export_mode=0):
        """
        Save powerflow data to file.
        Args:
            (1) file: string, target powerflow file name.
            (2) ftype: string, powerflow data format.
            (3) export_zero_line: boolean, logic of whether exporting zero impedance lines. True for export, False for not export.
            (4) export_out_of_service_bus: boolean, logic of whether exporting out-of-service buses. True for export, False for not export.
            (5) export_mode: integer, export mode (0,1,2,3). 0 for exporting data as import, 1 for exporting data ordered by bus number in ascending order, 2 for exporting data ordered by bus name in ascending order, 3 for exporting buses in the order of generator, load, hvdc buses.
        Rets: N/A
        """
        if export_mode not in (0,1,2,3):
            export_mode = 0;
        if export_mode==0:
            self.__save_powerflow_data_in_keep_mode(file, ftype, export_zero_line, export_out_of_service_bus)
        elif export_mode==1:
            self.__save_powerflow_data_in_bus_number_ordered_mode(file, ftype, export_zero_line, export_out_of_service_bus)
        elif export_mode==2:
            self.__save_powerflow_data_in_bus_name_ordered_mode(file, ftype, export_zero_line, export_out_of_service_bus)
        elif export_mode==3:
            self.__save_powerflow_data_in_dynamic_optimized_mode(file, ftype, export_zero_line, export_out_of_service_bus)
        else:
            print("parameter export_mode is invalid in save_powerflow_data()")
        
    def __save_powerflow_data_in_keep_mode(self, file, ftype, export_zero_line=True, export_out_of_service_bus=True):
        """
        Save powerflow data to file in keep as original mode
        Args:
            (1) file: string, target powerflow file name.
            (2) ftype: string, powerflow data format.
            (3) export_zero_line: boolean, logic of whether exporting zero impedance lines. True for export, False for not export.
            (4) export_out_of_service_bus: boolean, logic of whether exporting out-of-service buses. True for export, False for not export.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_save_powerflow_data_to_file(file, ftype, export_zero_line, export_out_of_service_bus, 0, self.toolkit_index)
        
    def __save_powerflow_data_in_bus_number_ordered_mode(self, file, ftype, export_zero_line=True, export_out_of_service_bus=True):
        """
        Save powerflow data to file in bus number ascending order.
        Args:
            (1) file: string, target powerflow file name.
            (2) ftype: string, powerflow data format.
            (3) export_zero_line: boolean, logic of whether exporting zero impedance lines. True for export, False for not export.
            (4) export_out_of_service_bus: boolean, logic of whether exporting out-of-service buses. True for export, False for not export.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_save_powerflow_data_to_file(file, ftype, export_zero_line, export_out_of_service_bus, 1, self.toolkit_index)
        
    def __save_powerflow_data_in_bus_name_ordered_mode(self, file, ftype, export_zero_line=True, export_out_of_service_bus=True):
        """
        Save powerflow data to file in bus name ascending order.
        Args:
            (1) file: string, target powerflow file name.
            (2) ftype: string, powerflow data format.
            (3) export_zero_line: boolean, logic of whether exporting zero impedance lines. True for export, False for not export.
            (4) export_out_of_service_bus: boolean, logic of whether exporting out-of-service buses. True for export, False for not export.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_save_powerflow_data_to_file(file, ftype, export_zero_line, export_out_of_service_bus, 2, self.toolkit_index)
        
    def __save_powerflow_data_in_dynamic_optimized_mode(self, file, ftype, export_zero_line=True, export_out_of_service_bus=True):
        """
        Save powerflow data to file in generator, load, hvdc bus order. This method is used for improving dynamic simulation performance.
        Args:
            (1) file: string, target powerflow file name.
            (2) ftype: string, powerflow data format.
            (3) export_zero_line: boolean, logic of whether exporting zero impedance lines. True for export, False for not export.
            (4) export_out_of_service_bus: boolean, logic of whether exporting out-of-service buses. True for export, False for not export.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_save_powerflow_data_to_file(file, ftype, export_zero_line, export_out_of_service_bus, 3, self.toolkit_index)

    def load_powerflow_result(self, file, ftype):
        """
        Load powerflow result from file.
        Args:
            (1) file: string, source powerflow result file name.
            (2) ftype: string, powerflow result data format.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_load_powerflow_result_from_file(file, ftype, self.toolkit_index)
        
    def load_dynamic_data(self, file, ftype):
        """
        Load dynamic data from file.
        Args:
            (1) file: string, source dynamic data file name.
            (2) ftype: string, dynamic data format.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_load_dynamic_data_from_file(file, ftype, self.toolkit_index)
        
    def save_dynamic_data(self, file, ftype):
        """
        Save dynamic data to file.
        Args:
            (1) file: string, target dynamic data file name.
            (2) ftype: string, dynamic data format.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        ftype = self.__get_c_char_p_of_string(ftype)
        STEPS_LIB.api_save_dynamic_data_to_file(file, ftype, self.toolkit_index)

    def check_powerflow_data(self):
        """
        Check powerflow data. If any inappropriate data is set, report will be sent to log file.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_check_powerflow_data(self.toolkit_index)
        
    def check_dynamic_data(self):
        """
        Check dynamic model data. If any inappropriate data is set, report will be sent to log file.
        Args: N/A
        Rets: N/A        
        """
        global STEPS_LIB
        STEPS_LIB.api_check_dynamic_data(self.toolkit_index)
        
    def check_missing_models(self):
        """
        Check missing models. If any compulsory models are missing, report will be sent to log file.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_check_missing_models(self.toolkit_index)
        
    def check_least_dynamic_time_constants(self):
        """
        Check the least dynamic time constants. Report of the first least time constants in models will be sent to log file. The dynamic simulation time step should be < one fourth of the least time constant.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_check_least_dynamic_time_constants(self.toolkit_index)
        
    def check_network_connectivity(self, remove_void_islands=False):
        """
        Check network connectivity. 
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_check_network_connectivity(remove_void_islands, self.toolkit_index)
        

    def add_bus(self, busnumber, busname, basevoltage):
        """
        Add new bus with bus number, bus name, and base voltage.
        Args:
            (1) busnumber: Bus number.
            (2) busname: String of bus name.
            (3) basevoltage: Base voltage in kV.
        Rets: N/A
        """
        global STEPS_LIB
        busname = self.__get_c_char_p_of_string(busname)
        STEPS_LIB.api_add_bus(busnumber, busname, basevoltage, self.toolkit_index)
        return

    def add_generator(self, generator):
        """
        Add new generator with device id.
        Args:
            (1) generator: Tuple device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_generator(bus, ickt, self.toolkit_index)
        return

    def add_wt_generator(self, generator):
        """
        Add new wind turbine generator with device id.
        Args:
            (1) generator: Tuple device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_wt_generator(bus, ickt, self.toolkit_index)

    def add_pv_unit(self, unit):
        """
        Add new PV unit with device id.
        Args:
            (1) unit: Tuple device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(unit)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_pv_unit(bus, ickt, self.toolkit_index)
        return

    def add_load(self, load):
        """
        Add new load with device id.
        Args:
            (1) load: Tuple device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_load(bus, ickt, self.toolkit_index)
        return

    def add_fixed_shunt(self, shunt):
        """
        Add new fixed shunt with device id.
        Args:
            (1) shunt: Tuple device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(shunt)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_fixed_shunt(bus, ickt, self.toolkit_index)
        return

    def add_line(self, line):
        """
        Add new transmission line with device id.
        Args:
            (1) line: Tuple device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_line(ibus, jbus, ickt, self.toolkit_index)
        return

    def add_hvdc(self, hvdc):
        """
        Add new HVDC link with device id.
        Args:
            (1) hvdc: Tuple device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_hvdc(ibus, jbus, ickt, self.toolkit_index)
        return

    def add_transformer(self, transformer):
        """
        Add new transformer with device id.
        Args:
            (1) transformer: Tuple device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
        """
        global STEPS_LIB
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_transformer(ibus, jbus, kbus, ickt, self.toolkit_index)
        return

    def add_equivalent_device(self, device):
        """
        Add new equivalent device with device id.
        Args:
            (1) device: Tuple device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(device)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_equivalent_device(bus, ickt, self.toolkit_index)
        return

    def add_energy_storage(self, storage):
        """
        Add new energy storage with device id.
        Args:
            (1) storage: Tuple device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(storage)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_add_energy_storage(bus, ickt, self.toolkit_index)
        return

    def add_area(self, areanumber, areaname):
        """
        Add new area with area number and area name.
        Args:
            (1) areanumber: Area number.
            (2) areaname: String of area name.
        Rets: N/A
        """
        global STEPS_LIB
        areaname = self.__get_c_char_p_of_string(areaname)
        STEPS_LIB.api_add_area(areanumber, areaname, self.toolkit_index)
        return

    def add_zone(self, zonenumber, zonename):
        """
        Add new zone with zone number and zone name.
        Args:
            (1) zonenumber: Zone number.
            (2) zonename: String of zone name.
        Rets: N/A
        """
        global STEPS_LIB
        zonename = self.__get_c_char_p_of_string(zonename)
        STEPS_LIB.api_add_zone(zonenumber, zonename, self.toolkit_index)
        return

    def add_owner(self, ownernumber, ownername):
        """
        Add new owner with owner number and owner name.
        Args:
            (1) ownernumber: Owner number.
            (2) ownername: String of owner name.
        Rets: N/A
        """
        global STEPS_LIB
        ownername = self.__get_c_char_p_of_string(ownername)
        STEPS_LIB.api_add_owner(ownernumber, ownername, self.toolkit_index)
        return

    def remove_bus(self, busnumber):
        """
        Remove bus of bus number.
        Args:
            (1) busnumber: Bus number.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_remove_bus(busnumber, self.toolkit_index)
        return

    def remove_generator(self, generator):
        """
        Remove generator with device id.
        Args:
            (1) generator: Tuple generator device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_generator(bus, ickt, self.toolkit_index)
        return

    def remove_wt_generator(self, generator):
        """
        Remove wind turbine generator with device id.
        Args:
            (1) generator: Tuple wind turbine generator device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_wt_generator(bus, ickt, self.toolkit_index)
        return

    def remove_pv_unit(self, unit):
        """
        Remove PV unit with device id.
        Args:
            (1) unit: Tuple PV unit device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(unit)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_pv_unit(bus, ickt, self.toolkit_index)
        return

    def remove_load(self, load):
        """
        Remove load with device id.
        Args:
            (1) load: Tuple load device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_load(bus, ickt, self.toolkit_index)
        return

    def remove_fixed_shunt(self, shunt):
        """
        Remove fixed shunt with device id.
        Args:
            (1) shunt: Tuple fixed shunt device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(shunt)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_fixed_shunt(bus, ickt, self.toolkit_index)
        return

    def remove_line(self, line):
        """
        Remove transmission line with device id.
        Args:
            (1) line: Tuple transmission line device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_line(ibus, jbus, ickt, self.toolkit_index)
        return

    def remove_hvdc(self, hvdc):
        """
        Remove HVDC link with device id.
        Args:
            (1) hvdc: Tuple HVDC link device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_hvdc(ibus, jbus, ickt, self.toolkit_index)
        return

    def remove_transformer(self, transformer):
        """
        Remove transformer with device id.
        Args:
            (1) transformer: Tuple transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
        """
        global STEPS_LIB
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_transformer(ibus, jbus, kbus, ickt, self.toolkit_index)
        return

    def remove_equivalent_device(self, device):
        """
        Remove equivalent device with device id.
        Args:
            (1) device: Tuple equivalent device device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(device)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_equivalent_device(bus, ickt, self.toolkit_index)
        return

    def remove_energy_storage(self, storage):
        """
        Remove energy storage with device id.
        Args:
            (1) storage: Tuple energy storage device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(storage)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_remove_energy_storage(bus, ickt, self.toolkit_index)
        return

    def remove_area(self, areanumber):
        """
        Remove area with area number.
        Args:
            (1) arenumber: area number to remove.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_remove_area(areanumber, self.toolkit_index)
        return

    def remove_zone(self, zonenumber):
        """
        Remove zone with zone number.
        Args:
            (1) zonenumber: zone number to remove.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_remove_zone(zonenumber, self.toolkit_index)
        return

    def remove_owner(self, ownernumber):
        """
        Remove owner with owner number.
        Args:
            (1) ownernumber: owner number to remove.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_remove_owner(ownernumber, self.toolkit_index)
        return
    
    def change_bus_number(self, old_number, new_number):
        """
        Change bus number in the database..
        Args:
            (1) old_number: Old bus number.
            (2) new_number: New bus number.
        Rets: N/A
        Tips:
            The new_number should be valid, a.k.a, should be positive and < system allowed maximum bus number.
        """
        global STEPS_LIB
        STEPS_LIB.api_change_bus_number(old_number, new_number, self.toolkit_index)
        return
    
    def change_bus_number_with_file(self, file):
        """
        Change bus number in the database with csv file.
        Args:
            (1) file: Bus pair csv file.
        Rets: N/A
        Tips:
            The bus pair csv should have no header lines. Each line is a record, and each record should have the following format: "original_number, new_number".
            It is recommended that there should be no intersection between the sets of new bus numbers and old bus numbers.
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_change_bus_number_with_file(file, self.toolkit_index)
        return
        
    def get_bus_count(self):
        """
        Return number of buses, including both in-service and out-of-service buses.
        Args: N/A
        Rets: 
            (1) Number of buses.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("BUS")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_generator_count(self):
        """
        Return number of generators.
        Args: N/A
        Rets: 
            (1) Number of generators.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Generator")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_wt_generator_count(self):
        """
        Return number of wind turbine generators.
        Args: N/A
        Rets: 
            (1) Number of wind turbine generators.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("WT Generator")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_pv_unit_count(self):
        """
        Return number of PV units.
        Args: N/A
        Rets: 
            (1) Number of PV units.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("PV Unit")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_load_count(self):
        """
        Return number of loads.
        Args: N/A
        Rets: 
            (1) Number of loads.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Load")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_fixed_shunt_count(self):
        """
        Return number of fixed shunt.
        Args: N/A
        Rets: 
            (1) Number of fixed shunts.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Fixed Shunt")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_line_count(self):
        """
        Return number of transmission lines.
        Args: N/A
        Rets: 
            (1) Number of transmission lines.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Line")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_transformer_count(self):
        """
        Return number of transformers.
        Args: N/A
        Rets: 
            (1) Number of transformers.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Transformer")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_hvdc_count(self):
        """
        Return number of HVDC links.
        Args: N/A
        Rets: 
            (1) Number of HVDC links.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("HVDC")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_equivalent_device_count(self):
        """
        Return number of equivalent devices.
        Args: N/A
        Rets: 
            (1) Number of equivalent devices.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Equivalent Device")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_energy_storage_count(self):
        """
        Return number of energy storages.
        Args: N/A
        Rets: 
            (1) Number of energy storages.
        """
        global STEPS_LIB
        device = self.__get_c_char_p_of_string("Energy Storage")
        return STEPS_LIB.api_get_device_count(device, self.toolkit_index)
    def get_area_count(self):
        """
        Return number of areas.
        Args: N/A
        Rets: 
            (1) Number of areas.
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_area_count(self.toolkit_index)
    def get_zone_count(self):
        """
        Return number of zones.
        Args: N/A
        Rets: 
            (1) Number of zones.
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_zone_count(self.toolkit_index)
    def get_owner_count(self):
        """
        Return number of owners.
        Args: N/A
        Rets: 
            (1) Number of owners.
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_owner_count(self.toolkit_index)
    def get_in_service_bus_count(self):
        """
        Return number of in-service buses.
        Args: N/A
        Rets: 
            (1) Number of in-service buses.
        """
        global STEPS_LIB
        STEPS_LIB.api_get_in_service_bus_count(self.toolkit_index)
        return
    def update_overshadowed_buses(self):
        """
        Update overshowed buses.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        return STEPS_LIB.api_update_overshadowed_buses(self.toolkit_index)
    def set_all_buses_un_overshadowed(self):
        """
        Set all buses as un-overshowed.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_set_all_buses_un_overshadowed(self.toolkit_index)
        return
    def get_overshadowed_bus_count(self):
        """
        Get number of overshowed buses. If there are n buses directly connected by zero impedance line or lines, n-1 buses are overshadowed by one of them. 
        Args: N/A
        Rets:
            (1) Number of overshadowed buses.
        Tips:
            This function calls api to update overshadowed buses first.
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_overshadowed_bus_count(self.toolkit_index)

    def is_bus_exist(self, bus):
        """
        Check if given bus exists or not.
        Args:
            (1) bus: bus number.
        Rets:
            (1) True if the bus exists, False otherwise.
        """
        global STEPS_LIB
        return STEPS_LIB.api_is_bus_exist(bus, self.toolkit_index)

    def is_generator_exist(self, generator):
        """
        Check if given generator exists or not.
        Args:
            (1) generator: tuple of generator device id in format of (bus, ickt).
        Rets:
            (1) True if the generator exists, False otherwise.
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_generator_exist(bus, ickt, self.toolkit_index)

    def is_wt_generator_exist(self, generator):
        """
        Check if given wind turbine generator exists or not.
        Args:
            (1) generator: tuple of wind turbine generator device id in format of (bus, ickt).
        Rets:
            (1) True if the wind turbine generator exists, False otherwise.
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_wt_generator_exist(bus, ickt, self.toolkit_index)

    def is_pv_unit_exist(self, pv_unit):
        """
        Check if given PV unit exists or not.
        Args:
            (1) pv_unit: tuple of PV unit device id in format of (bus, ickt).
        Rets:
            (1) True if the PV unit exists, False otherwise.
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(pv_unit)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_pv_unit_exist(bus, ickt, self.toolkit_index)

    def is_load_exist(self, load):
        """
        Check if given load exists or not.
        Args:
            (1) load: tuple of load device id in format of (bus, ickt).
        Rets:
            (1) True if the load exists, False otherwise.
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_load_exist(bus, ickt, self.toolkit_index)

    def is_fixed_shunt_exist(self, shunt):
        """
        Check if given fixed shunt exists or not.
        Args:
            (1) shunt: tuple of fixed shunt device id in format of (bus, ickt).
        Rets:
            (1) True if the fixed shunt exists, False otherwise.
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(shunt)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_fixed_shunt_exist(bus, ickt, self.toolkit_index)

    def is_line_exist(self, line):
        """
        Check if given transmission line exists or not.
        Args:
            (1) line: tuple of transmission line device id in format of (ibus, jbus, ickt).
        Rets:
            (1) True if the transmission line exists, False otherwise.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_line_exist(ibus, jbus, ickt, self.toolkit_index)

    def is_transformer_exist(self, transformer):
        """
        Check if given transformer exists or not.
        Args:
            (1) transformer: tuple of transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
        Rets:
            (1) True if the transformer exists, False otherwise.
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
        """
        global STEPS_LIB
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_transformer_exist(ibus, jbus, kbus, ickt, self.toolkit_index)

    def is_hvdc_exist(self, hvdc):
        """
        Check if given HVDC link exists or not.
        Args:
            (1) hvdc: tuple of HVDC link device id in format of (ibus, jbus, ickt).
        Rets:
            (1) True if the HVDC link exists, False otherwise.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_hvdc_exist(ibus, jbus, ickt, self.toolkit_index)

    def is_equivalent_device_exist(self, equivalent_device):
        """
        Check if given equivalent device exists or not.
        Args:
            (1) equivalent_device: tuple of equivalent device device id in format of (bus, ickt).
        Rets:
            (1) True if the equivalent device exists, False otherwise.
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(equivalent_device)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_equivalent_device_exist(bus, ickt, self.toolkit_index)

    def is_energy_storage_exist(self, energy_storage):
        """
        Check if given energy storage device exists or not.
        Args:
            (1) energy_storage: tuple of energy storage device id in format of (bus, ickt).
        Rets:
            (1) True if the energy storage device exists, False otherwise.
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(energy_storage)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_is_energy_storage_exist(bus, ickt, self.toolkit_index)
    
    def bus_name2number(self, name):
        """
        Converter bus name to bus number.
        Args:
            (1) name: bus name.
        Rets:
            (1) Bus number. 0 if bus does not exist.
        Tips:
            If two or more buses have the same bus name, only the first bus is returned.
        """
        global STEPS_LIB
        name = self.__get_c_char_p_of_string(name)
        return int(STEPS_LIB.api_bus_name2bus_number(name, self.toolkit_index))

    def bus_number2name(self, bus):
        """
        Converter bus number to bus name.
        Args:
            (1) bus: bus number.
        Rets:
            (1) String of bus name. Empty string if bus does not exist.
        """
        global STEPS_LIB
        return self.__get_string_from_c_char_p(STEPS_LIB.api_bus_number2bus_name(bus, self.toolkit_index))

    def get_all_buses(self):
        """
        Get all buses in the database.
        Args: N/A
        Rets:
            (1) Tuple of all buses. Empty tuple if no buses in the database.
        """
        global STEPS_LIB
        STEPS_LIB.api_initialize_all_bus_search(self.toolkit_index)
        buses = []
        while True:
            bus = STEPS_LIB.api_get_current_bus_number(self.toolkit_index)
            if bus==0:
                break
            buses.append(int(bus))
            STEPS_LIB.api_goto_next_bus(self.toolkit_index)
        return tuple(buses)
   
    def get_buses_with_constraints(self, vbase_min=0.0, vbase_max=10000000.0, v_min=0.0, v_max=10000000.0, area=0, zone=0, owner=0):
        """
        Get all buses in the database satisfying all constraints.
        Args:
            (1) vbase_min: minimum base voltage in kV. Returned buses must have base voltage >= vbase_min.
            (2) vbase_max: maximum base voltage in kV. Returned buses must have base voltage <= vbase_max.
            (3) v_min: minimum voltage in pu. Returned buses must have pu voltage >= v_min.
            (4) v_max: maximum voltage in pu. Returned buses must have pu voltage <= v_max.
            (5) area: area number. Returned buses must be in the area. Ignore the area constraint if area=0.
            (6) zone: zone number. Returned buses must be in the zone. Ignore the zone constraint if zone=0.
            (8) owner: owner number. Returned buses must be of the owner. Ignore the owner constraint if owner=0.
        Rets:
            (1) Tuple of buses satisfying all constraints. Empty tuple if no buses are satisfying the constants.
        """
        global STEPS_LIB
        buses = []        
        STEPS_LIB.api_initialize_bus_search(vbase_min, vbase_max, v_min, v_max, area, zone, owner, self.toolkit_index)
        while True:
            bus = STEPS_LIB.api_get_current_bus_number(self.toolkit_index)
            if bus==0:
                break
            buses.append(int(bus))
            STEPS_LIB.api_goto_next_bus(self.toolkit_index)
        return tuple(buses)
                
    def get_all_generators(self):
        """
        Get all generators in the database.
        Args: N/A
        Rets:
            (1) Tuple of all generators. Empty tuple if no generators in the database.
        """
        return self.get_generators_at_bus(0)
        
    def get_generators_at_bus(self, bus):
        """
        Get all generators in the database.
        Args: N/A
        Rets:
            (1) Tuple of all generators. Empty tuple if no generators in the database.
        """
        global STEPS_LIB
        device = "GENERATOR"
        device = self.__get_c_char_p_of_string(device)
        blank = self.__get_c_char_p_of_string("")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        generators = []
        while True:
            bus = STEPS_LIB.api_get_current_device_bus_number(device, blank, self.toolkit_index)
            if bus==0:
                break
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            generators.append((int(bus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(generators)
        
    def get_all_wt_generators(self):
        """
        Get all wind turbine generators in the database.
        Args: N/A
        Rets:
            (1) Tuple of all wind turbine generators. Empty tuple if no wind turbine generators in the database.
        """
        return self.get_wt_generators_at_bus(0)
        
    def get_wt_generators_at_bus(self, bus):
        """
        Get all wind turbine generators at given bus.
        Args: 
            (1) bus: bus number
        Rets:
            (1) Tuple of all wind turbine generators at given bus. Empty tuple if no wind turbine generators at given bus.
        """
        global STEPS_LIB
        device = "WT GENERATOR"
        device = self.__get_c_char_p_of_string(device)
        blank = self.__get_c_char_p_of_string("")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        wt_generators = []
        while True:
            bus = STEPS_LIB.api_get_current_device_bus_number(device, blank, self.toolkit_index)
            if bus==0:
                break
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            wt_generators.append((int(bus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(wt_generators)
        
    def get_all_pv_units(self):
        """
        Get all PV units in the database.
        Args: N/A
        Rets:
            (1) Tuple of all PV units. Empty tuple if no PV units in the database.
        """
        return self.get_pv_units_at_bus(0)
        
    def get_pv_units_at_bus(self, bus):
        """
        Get all PV units at given bus.
        Args: 
            (1) bus: bus number
        Rets:
            (1) Tuple of all PV units at given bus. Empty tuple if no PV units at given bus.
        """
        global STEPS_LIB
        device = "PV UNIT"
        device = self.__get_c_char_p_of_string(device)
        blank = self.__get_c_char_p_of_string("")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        pv_units = []
        while True:
            bus = STEPS_LIB.api_get_current_device_bus_number(device, blank, self.toolkit_index)
            if bus==0:
                break
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            pv_units.append((int(bus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(pv_units)
        
    def get_all_energy_storages(self):
        """
        Get all energy storages in the database.
        Args: N/A
        Rets:
            (1) Tuple of all energy storages. Empty tuple if no energy storages in the database.
        """
        return self.get_energy_storages_at_bus(0)
        
    def get_energy_storages_at_bus(self, bus):
        """
        Get all energy storages at bus with input bus number.
        Args:
            (1) bus: bus number
        Rets:
            (1) Tuple of all energy storages at given bus. Empty tuple if no energy storages at given bus.
        """
        global STEPS_LIB
        device = "ENERGY STORAGE"
        device = self.__get_c_char_p_of_string(device)
        blank = self.__get_c_char_p_of_string("")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        energy_storages = []
        while True:
            bus = STEPS_LIB.api_get_current_device_bus_number(device, blank, self.toolkit_index)
            if bus==0:
                break
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            energy_storages.append((int(bus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(energy_storages)
        
    def get_all_loads(self):
        """
        Get all loads in the database.
        Args: N/A
        Rets:
            (1) Tuple of all loads. Empty tuple if no loads in the database.
        """
        return self.get_loads_at_bus(0)
        
    def get_loads_at_bus(self, bus):
        """
        Get all loads at bus with input bus number.
        Args:
            (1) bus: bus number
        Rets:
            (1) Tuple of all loads at given bus. Empty tuple if no loads at given bus.
        """
        global STEPS_LIB
        device = "LOAD"
        device = self.__get_c_char_p_of_string(device)
        blank = self.__get_c_char_p_of_string("")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        loads = []
        while True:
            bus = STEPS_LIB.api_get_current_device_bus_number(device, blank, self.toolkit_index)
            if bus==0:
                break
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            loads.append((int(bus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(loads)
        
    def get_all_fixed_shunts(self):
        """
        Get all fixed shunts in the database.
        Args: N/A
        Rets:
            (1) Tuple of all fixed shunt. Empty tuple if no fixed shunts in the database.
        """
        return self.get_fixed_shunts_at_bus(0)
        
    def get_fixed_shunts_at_bus(self, bus):
        """
        Get all fixed shunts at bus with input bus number.
        Args:
            (1) bus: bus number
        Rets:
            (1) Tuple of all fixed shunts at given bus. Empty tuple if no fixed shunts at given bus.
        """
        global STEPS_LIB
        device = "FIXED SHUNT"
        device = self.__get_c_char_p_of_string(device)
        blank = self.__get_c_char_p_of_string("")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        fixed_shunts = []
        while True:
            bus = STEPS_LIB.api_get_current_device_bus_number(device, blank, self.toolkit_index)
            if bus==0:
                break
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            fixed_shunts.append((int(bus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(fixed_shunts)
                
    def get_all_equivalent_devices(self):
        """
        Get all equivalent devices in the database.
        Args: N/A
        Rets:
            (1) Tuple of all equivalent devices. Empty tuple if no equivalent devices in the database.
        """
        return self.get_equivalent_devices_at_bus(0)
        
    def get_equivalent_devices_at_bus(self, bus):
        """
        Get all equivalent devices at bus with input bus number.
        Args:
            (1) bus: bus number
        Rets:
            (1) Tuple of all equivalent devices at given bus. Empty tuple if no equivalent devices at given bus.
        """
        global STEPS_LIB
        device = "EQUIVALENT DEVICE"
        device = self.__get_c_char_p_of_string(device)
        blank = self.__get_c_char_p_of_string("")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        equivalent_devices = []
        while True:
            bus = STEPS_LIB.api_get_current_device_bus_number(device, blank, self.toolkit_index)
            if bus==0:
                break
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            equivalent_devices.append((int(bus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(equivalent_devices)

    def get_all_lines(self):
        """
        Get all transmission lines in the database.
        Args: N/A
        Rets:
            (1) Tuple of all transmission lines. Empty tuple if no transmission lines in the database.
        """
        return self.get_lines_at_bus(0)
        
    def get_lines_at_bus(self, bus):
        """
        Get all transmission lines at bus with input bus number.
        Args:
            (1) bus: bus number
        Rets:
            (1) Tuple of all transmission lines at given bus. Empty tuple if no transmission lines at given bus.
        """
        global STEPS_LIB
        device = "LINE"
        device = self.__get_c_char_p_of_string(device)
        send_side = self.__get_c_char_p_of_string("SEND")
        recv_side = self.__get_c_char_p_of_string("RECEIVE")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        lines = []
        while True:
            ibus = STEPS_LIB.api_get_current_device_bus_number(device, send_side, self.toolkit_index)
            if ibus==0:
                break
            jbus = STEPS_LIB.api_get_current_device_bus_number(device, recv_side, self.toolkit_index)
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            lines.append((int(ibus), int(jbus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(lines)
        
    def get_lines_between_buses(self, ibus, jbus):
        """
        Get all transmission lines between ibus and jbus.
        Args:
            (1) ibus: i-side bus number
            (2) jbus: j-side bus number
        Rets:
            (1) Tuple of all transmission lines between given buses. Empty tuple if no transmission lines between given buses.
        Example:
            get_lines_between_buses(1,2)
        """
        lines = self.get_lines_at_bus(ibus)
        if len(lines)==0:
            return lines
        else:
            lns = []
            for line in lines:
                if jbus in line:
                    lns.append(line) 
            return tuple(lns)

    def get_all_transformers(self):
        """
        Get all transformers in the database.
        Args: N/A
        Rets:
            (1) Tuple of all transformers. Empty tuple if no transformers in the database.
        """
        return self.get_transformers_at_bus(0)
        
    def get_transformers_at_bus(self, bus):
        """
        Get all transformers at bus with input bus number.
        Args:
            (1) bus: bus number
        Rets:
            (1) Tuple of all transformers at given bus. Empty tuple if no transformers at given bus.
        """
        global STEPS_LIB
        device = "TRANSFORMER"
        device = self.__get_c_char_p_of_string(device)
        pri_side = self.__get_c_char_p_of_string("PRIMARY")
        sec_side = self.__get_c_char_p_of_string("SECONDARY")
        ter_side = self.__get_c_char_p_of_string("TERTIARY")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        transformers = []
        while True:
            ibus = STEPS_LIB.api_get_current_device_bus_number(device, pri_side, self.toolkit_index)
            if ibus==0:
                break
            jbus = STEPS_LIB.api_get_current_device_bus_number(device, sec_side, self.toolkit_index)
            kbus = STEPS_LIB.api_get_current_device_bus_number(device, ter_side, self.toolkit_index)
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            transformers.append((int(ibus), int(jbus), int(kbus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(transformers)
    
    def get_transformers_between_buses(self, ibus, jbus, kbus=0):
        """
        Get all transformers between ibus, jbus, and kbus. If kbus=0, two-winding transformers are returned.
        Args:
            (1) ibus: i-side bus number
            (2) jbus: j-side bus number
            (3) kbus: k-side bus number, 0 for two-winding transformers
        Rets:
            (1) Tuple of all transformers between given buses. Empty tuple if no transformers between given buses.
        Example:
            get_transformers_between_buses(1,2)
            get_transformers_between_buses(1,2,0)
            get_transformers_between_buses(1,2,3)
        """
        transformers = self.get_transformers_at_bus(ibus)
        if len(transformers)==0:
            return transformers
        else:
            transes = []
            for trans in transformers:
                if jbus in trans and kbus in trans:
                    transes.append(trans) 
            return tuple(transes)
            
    def get_all_hvdcs(self):
        """
        Get all HVDC links in the database.
        Args: N/A
        Rets:
            (1) Tuple of all HVDC links. Empty tuple if no HVDC links in the database.
        """
        return self.get_hvdcs_at_bus(0)
        
    def get_hvdcs_at_bus(self, bus):
        """
        Get all HVDC links at bus with input bus number.
        Args:
            (1) bus: bus number
        Rets:
            (1) Tuple of all HVDC links at given bus. Empty tuple if no HVDC links at given bus.
        """
        global STEPS_LIB
        device = "HVDC"
        device = self.__get_c_char_p_of_string(device)
        rec_side = self.__get_c_char_p_of_string("RECTIFIER")
        inv_side = self.__get_c_char_p_of_string("INVERTER")
        STEPS_LIB.api_initialize_device_search(device, bus, self.toolkit_index)
        hvdcs = []
        while True:
            ibus = STEPS_LIB.api_get_current_device_bus_number(device, rec_side, self.toolkit_index)
            if ibus==0:
                break
            jbus = STEPS_LIB.api_get_current_device_bus_number(device, inv_side, self.toolkit_index)
            id = STEPS_LIB.api_get_current_device_identifier(device, self.toolkit_index)
            id = self.__get_string_from_c_char_p(id)
            hvdcs.append((int(ibus), int(jbus), id))
            STEPS_LIB.api_goto_next_device(device, self.toolkit_index)
        return tuple(hvdcs)

    def get_hvdcs_between_buses(self, ibus, jbus):
        """
        Get all HVDC links between ibus and jbus.
        Args:
            (1) ibus: i-side bus number
            (2) jbus: j-side bus number
        Rets:
            (1) Tuple of all HVDC links between given buses. Empty tuple if no HVDC links between given buses.
        Example:
            get_hvdcs_between_buses(1,2)
        """
        hvdcs = self.get_hvdcs_at_bus(ibus)
        if len(hvdcs)==0:
            return hvdcs
        else:
            dcs = []
            for dc in hvdcs:
                if jbus in dc:
                    dcs.append(dc) 
            return tuple(dcs)

    def get_generators_with_constraints(self, area=0, zone=0):
        """
        Get all generators satisfying area and zone constraints.
        Args:
            (1) area: Area number. Retured generators must be in the area. Area constraint is ignored if area=0.
            (2) zone: Zone number. Retured generators must be in the zone. Zone constraint is ignored if zone=0.
        Rets:
            (1) Tuple of all generators in given area and zone. Empty tuple if none in given area and zone.
        """
        all_gens = self.get_all_generators()
        if area==0 and zone==0:
            return all_gens
        else:
            gens = []
            if area==0 and zone!=0:
                for gen in all_gens:
                    bus = gen[0]
                    gen_zone = self.get_bus_data(bus, "i", "zone")
                    if gen_zone==zone:
                        gens.append(gen)
            elif area!=0 and zone==0:
                for gen in all_gens:
                    bus = gen[0]
                    gen_area = self.get_bus_data(bus, "i", "area")
                    if gen_area==area:
                        gens.append(gen)
            else:
                for gen in all_gens:
                    bus = gen[0]
                    gen_area = self.get_bus_data(bus, "i", "area")
                    gen_zone = self.get_bus_data(bus, "i", "zone")
                    if gen_area==area and gen_zone==zone:
                        gens.append(gen)
        return tuple(gens)
        
    def get_wt_generators_with_constraints(self, area=0, zone=0):
        """
        Get all wind trubine generators satisfying area and zone constraints.
        Args:
            (1) area: Area number. Retured wind turbine generators must be in the area. Area constraint is ignored if area=0.
            (2) zone: Zone number. Retured wind turbine generators must be in the zone. Zone constraint is ignored if zone=0.
        Rets:
            (1) Tuple of all wind turbine generators in given area and zone. Empty tuple if none in given area and zone.
        """
        all_gens = self.get_all_wt_generators()
        if area==0 and zone==0:
            return all_gens
        else:
            gens = []
            if area==0 and zone!=0:
                for gen in all_gens:
                    bus = gen[0]
                    gen_zone = self.get_bus_data(bus, "i", "zone")
                    if gen_zone==zone:
                        gens.append(gen)
            elif area!=0 and zone==0:
                for gen in all_gens:
                    bus = gen[0]
                    gen_area = self.get_bus_data(bus, "i", "area")
                    if gen_area==area:
                        gens.append(gen)
            else:
                for gen in all_gens:
                    bus = gen[0]
                    gen_area = self.get_bus_data(bus, "i", "area")
                    gen_zone = self.get_bus_data(bus, "i", "zone")
                    if gen_area==area and gen_zone==zone:
                        gens.append(gen)
        return tuple(gens)

    def get_pv_units_with_constraints(self, area=0, zone=0):
        """
        Get all PV units satisfying area and zone constraints.
        Args:
            (1) area: Area number. Retured PV units must be in the area. Area constraint is ignored if area=0.
            (2) zone: Zone number. Retured PV units must be in the zone. Zone constraint is ignored if zone=0.
        Rets:
            (1) Tuple of all PV units in given area and zone. Empty tuple if none in given area and zone.
        """
        all_pvs = self.get_all_pv_units()
        if area==0 and zone==0:
            return all_pvs
        else:
            pvs = []
            if area==0 and zone!=0:
                for pv in all_pvs:
                    bus = pv[0]
                    pv_zone = self.get_bus_data(bus, "i", "zone")
                    if pv_zone==zone:
                        pvs.append(pv)
            elif area!=0 and zone==0:
                for pv in all_pvs:
                    bus = pv[0]
                    pv_area = self.get_bus_data(bus, "i", "area")
                    if pv_area==area:
                        pvs.append(pv)
            else:
                for pv in all_pvs:
                    bus = pv[0]
                    pv_area = self.get_bus_data(bus, "i", "area")
                    pv_zone = self.get_bus_data(bus, "i", "zone")
                    if pv_area==area and pv_zone==zone:
                        pvs.append(pv)
        return tuple(pvs)

    def get_loads_with_constraints(self, area=0, zone=0):
        """
        Get all loads satisfying area and zone constraints.
        Args:
            (1) area: Area number. Retured loads must be in the area. Area constraint is ignored if area=0.
            (2) zone: Zone number. Retured loads must be in the zone. Zone constraint is ignored if zone=0.
        Rets:
            (1) Tuple of all loads in given area and zone. Empty tuple if none in given area and zone.
        """
        all_loads = self.get_all_loads()
        if area==0 and zone==0:
            return all_loads
        else:
            loads = []
            if area==0 and zone!=0:
                for load in all_loads:
                    bus = load[0]
                    load_zone = self.get_bus_data(bus, "i", "zone")
                    if load_zone==zone:
                        loads.append(load)
            elif area!=0 and zone==0:
                for load in all_loads:
                    bus = load[0]
                    load_area = self.get_bus_data(bus, "i", "area")
                    if load_area==area:
                        loads.append(load)
            else:
                for load in all_loads:
                    bus = load[0]
                    load_area = self.get_bus_data(bus, "i", "area")
                    load_zone = self.get_bus_data(bus, "i", "zone")
                    if load_area==area and load_zone==zone:
                        loads.append(load)
        return tuple(loads)
                
    def get_all_areas(self):
        """
        Get all areas in the database.
        Args: N/A
        Rets:
            (1) Tuple of all areas number. Empty tuple if no areas in the database.
        """
        global STEPS_LIB
        STEPS_LIB.api_initialize_area_search(self.toolkit_index)
        areas = []
        while True:
            area = STEPS_LIB.api_get_current_area_number(self.toolkit_index)
            if area==0:
                break
            areas.append(int(area))
            STEPS_LIB.api_goto_next_area(self.toolkit_index)
        return tuple(areas)
        
    def get_all_zones(self):
        """
        Get all zones in the database.
        Args: N/A
        Rets:
            (1) Tuple of all zones number. Empty tuple if no zones in the database.
        """
        global STEPS_LIB
        STEPS_LIB.api_initialize_zone_search(self.toolkit_index)
        zones = []
        while True:
            zone = STEPS_LIB.api_get_current_zone_number(self.toolkit_index)
            if zone==0:
                break
            zones.append(int(zone))
            STEPS_LIB.api_goto_next_zone(self.toolkit_index)
        return tuple(zones)
        
    def get_all_owners(self):
        """
        Get all owners in the database.
        Args: N/A
        Rets:
            (1) Tuple of all owners number. Empty tuple if no owners in the database.
        """
        global STEPS_LIB
        STEPS_LIB.api_initialize_owner_search(self.toolkit_index)
        owners = []
        while True:
            owner = STEPS_LIB.api_get_current_owner_number(self.toolkit_index)
            if owner==0:
                break
            owners.append(int(owner))
            STEPS_LIB.api_goto_next_owner(self.toolkit_index)
        return tuple(owners)

    def get_bus_data(self, bus, par_type, par_name):
        """
        Get bus data.
        Args:
            (1) bus: bus number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_bus_integer_data(bus, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_bus_float_data(bus, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_bus_boolean_data(bus, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_bus_string_data(bus, par_name, self.toolkit_index))
        return None

    def __get_source_data(self, source, par_type, par_name):
        """
        Private common function to get data of sources, including generator, wind turbine generator, PV unit, and energy storage.
        Args:
            (1) source: Source device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        bus, ickt = self.__extract_single_bus_device_id(source)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_source_integer_data(bus, ickt, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_source_float_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_source_boolean_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_source_string_data(bus, ickt, par_name, self.toolkit_index))
        return None

    def get_generator_data(self, generator, par_type, par_name):
        """
        Get generator data.
        Args:
            (1) generator: Generator device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        return self.__get_source_data(generator, par_type, par_name)

    def get_wt_generator_data(self, wt_generator, par_type, par_name):
        """
        Get wind turbine generator data.
        Args:
            (1) wt_generator: Wind turbine generator device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        return self.__get_source_data(wt_generator, par_type, par_name)

    def get_pv_unit_data(self, pv_unit, par_type, par_name):
        """
        Get PV unit data.
        Args:
            (1) pv_unit: PV unit device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        return self.__get_source_data(pv_unit, par_type, par_name)

    def get_energy_storage_data(self, energy_storage, par_type, par_name):
        """
        Get energy storage data.
        Args:
            (1) energy_storage: Energy storage device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        return self.__get_source_data(energy_storage, par_type, par_name)

    def get_load_data(self, load, par_type, par_name):
        """
        Get load data.
        Args:
            (1) load: Load device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        bus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_load_integer_data(bus, ickt, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_load_float_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_load_boolean_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_load_string_data(bus, ickt, par_name, self.toolkit_index))
        return None

    def get_fixed_shunt_data(self, fixed_shunt, par_type, par_name):
        """
        Get fixed shunt data.
        Args:
            (1) fixed_shunt: Fixed shunt device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        bus, ickt = self.__extract_single_bus_device_id(fixed_shunt)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_fixed_shunt_integer_data(bus, ickt, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_fixed_shunt_float_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_fixed_shunt_boolean_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_fixed_shunt_string_data(bus, ickt, par_name, self.toolkit_index))
        return None

    def get_equivalent_device_data(self, equivalent_device, par_type, par_name):
        """
        Get equivalent device data.
        Args:
            (1) equivalent_device: Equivalent device device id in format of (bus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        bus, ickt = self.__extract_single_bus_device_id(equivalent_device)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_equivalent_device_integer_data(bus, ickt, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_equivalent_device_float_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_equivalent_device_boolean_data(bus, ickt, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_equivalent_device_string_data(bus, ickt, par_name, self.toolkit_index))
        return None

    def get_line_data(self, line, par_type, par_name):
        """
        Get tranmission line data.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_line_integer_data(ibus, jbus, ickt, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_line_float_data(ibus, jbus, ickt, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_line_boolean_data(ibus, jbus, ickt, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_line_string_data(ibus, jbus, ickt, par_name, self.toolkit_index))
        return None

    def get_transformer_data(self, transformer, par_type, side, par_name):
        """
        Get transformer data.
        Args:
            (1) transformer: Transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) side: String of side. One of {"PRIMARY", "SECONDARY", "TERTIARY", "TRANSFORMER"}
            (4) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        side = side.upper()
        if side not in ['PRIMARY', 'SECONDARY', 'TERTIARY', 'TRANSFORMER']:
            return None
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
        ickt = self.__get_c_char_p_of_string(ickt)
        side = self.__get_c_char_p_of_string(side)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_transformer_integer_data(ibus, jbus, kbus, ickt, side, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_transformer_float_data(ibus, jbus, kbus, ickt, side, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_transformer_boolean_data(ibus, jbus, kbus, ickt, side, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_transformer_string_data(ibus, jbus, kbus, ickt, side, par_name, self.toolkit_index))
        return None

    def get_hvdc_data(self, hvdc, par_type, side, par_name):
        """
        Get HVDC link data.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt)
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) side: String of side. One of {"RECTIFIER", "INVERTER", "HVDC"}
            (4) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        side = side.upper()
        if side not in ['RECTIFIER', 'INVERTER', 'HVDC']:
            return None
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        side = self.__get_c_char_p_of_string(side)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_hvdc_integer_data(ibus, jbus, ickt, side, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_hvdc_float_data(ibus, jbus, ickt, side, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_hvdc_boolean_data(ibus, jbus, ickt, side, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_hvdc_string_data(ibus, jbus, ickt, side, par_name, self.toolkit_index))
        return None

    def get_area_data(self, area, par_type, par_name):
        """
        Get area data.
        Args:
            (1) area: Area number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_area_integer_data(area, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_area_float_data(area, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_area_boolean_data(area, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_area_string_data(area, par_name, self.toolkit_index))
        return None

    def get_zone_data(self, zone, par_type, par_name):
        """
        Get zone data.
        Args:
            (1) zone: Zone number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_zone_integer_data(zone, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_zone_float_data(zone, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_zone_boolean_data(zone, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_zone_string_data(zone, par_name, self.toolkit_index))
        return None
    
    def get_owner_data(self, owner, par_type, par_name):
        """
        Get owner data.
        Args:
            (1) owner: Owner number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_owner_integer_data(owner, par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_owner_float_data(owner, par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_owner_boolean_data(owner, par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_owner_string_data(owner, par_name, self.toolkit_index))
        return None

    def set_bus_data(self, bus, par_type, par_name, value):
        """
        Set bus data.
        Args:
            (1) bus: bus number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            STEPS_LIB.api_set_bus_integer_data(bus, par_name, value, self.toolkit_index)
            return
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_bus_float_data(bus, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_bus_boolean_data(bus, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_bus_string_data(bus, par_name, value, self.toolkit_index)
        return

    def __set_source_data(self, source, par_type, par_name, value):
        """
        Private common function to set data of source, including generator, wind turbine generator, PV unit, and energy storage.
        Args:
            (1) source: Source device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return        
        bus, ickt = self.__extract_single_bus_device_id(source)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_source_integer_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_source_float_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_source_boolean_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_source_string_data(bus, ickt, par_name, value, self.toolkit_index)
        return

    def set_generator_data(self, generator, par_type, par_name, value):
        """
        Set generator data.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        return self.__set_source_data(generator, par_type, par_name, value)

    def set_wt_generator_data(self, wt_generator, par_type, par_name, value):
        """
        Set wind turbine generator data.
        Args:
            (1) wt_generator: Wind turbine generator device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        return self.__set_source_data(wt_generator, par_type, par_name, value)

    def set_pv_unit_data(self, pv_unit, par_type, par_name, value):
        """
        Set PV unit data.
        Args:
            (1) pv_unit: PV unit device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        return self.__set_source_data(pv_unit, par_type, par_name, value)

    def set_energy_storage_data(self, energy_storage, par_type, par_name, value):
        """
        Set energy storage data.
        Args:
            (1) energy_storage: Energy storage device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        return self.__set_source_data(energy_storage, par_type, par_name, value)
    
    def set_generator_power(self, generator, s):
        """
        Set generator power.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) s: Complex power generation in MVA.
        Rets: N/A
        Tips: N/A
        Example: 
            set_generator_power((1,"#1"), 100+20j)
        """
        self.set_generator_data(generator, "F", "PGEN_MW", s.real)
        self.set_generator_data(generator, "F", "QGEN_MVAR", s.imag)
    
    def set_wt_generator_power(self, wt_generator, s):
        """
        Set wt generator power.
        Args:
            (1) wt_generator: WT generator device id in format of (bus, ickt).
            (2) s: Complex power generation in MVA.
        Rets: N/A
        Tips: N/A
        Example: 
            set_wt_generator_power((1,"#1"), 100+20j)
        """
        self.set_wt_generator_data(generator, "F", "PGEN_MW", s.real)
        self.set_wt_generator_data(generator, "F", "QGEN_MVAR", s.imag)
    
    def set_pv_unit_power(self, pv_unit, s):
        """
        Set pv unit power.
        Args:
            (1) pv_unit: PV unit device id in format of (bus, ickt).
            (2) s: Complex power generation in MVA.
        Rets: N/A
        Tips: N/A
        Example: 
            set_pv_unit_power((1,"#1"), 100+20j)
        """
        self.set_pv_unit_data(generator, "F", "PGEN_MW", s.real)
        self.set_pv_unit_data(generator, "F", "QGEN_MVAR", s.imag)
    
    def set_energy_storage_power(self, energy_storage, s):
        """
        Set energy storage power.
        Args:
            (1) energy_storage: Energy storage device id in format of (bus, ickt).
            (2) s: Complex power generation in MVA.
        Rets: N/A
        Tips: N/A
        Example: 
            set_energy_storage_power((1,"#1"), 100+20j)
        """
        self.set_energy_storage_data(energy_storage, "F", "PGEN_MW", s.real)
        self.set_energy_storage_data(energy_storage, "F", "QGEN_MVAR", s.imag)
        
    def set_load_data(self, load, par_type, par_name, value):
        """
        Set load data.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        bus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_load_integer_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_load_float_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_load_boolean_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_load_string_data(bus, ickt, par_name, value, self.toolkit_index)
        return

    def set_load_power(self, load, sp=None, si=None, sz=None):
        """
        Set load power.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) sp: Complex constant power load in MVA.
            (3) si: Complex constant current load in MVA.
            (4) sz: Complex constant impedance load in MVA.
        Rets: N/A
        Tips: 
            If the load component is None, the specific component is ignored.
        Example: 
            set_load_power((1,"#1"), 100+20j) # set constant power part only
            set_load_power((1,"#1"), sz = 60+10j) # set constant impedance part only
        """
        if sp!=None:
            self.set_load_data(load, "F", "PP0_MW",sp.real)
            self.set_load_data(load, "F", "QP0_MVAR",sp.imag)
        if si!=None:
            self.set_load_data(load, "F", "PI0_MW",si.real)
            self.set_load_data(load, "F", "QI0_MVAR",si.imag)
        if sz!=None:
            self.set_load_data(load, "F", "PZ0_MW",sz.real)
            self.set_load_data(load, "F", "QZ0_MVAR",sz.imag)
    
    def set_fixed_shunt_data(self, fixed_shunt, par_type, par_name, value):
        """
        Set fixed shunt data.
        Args:
            (1) fixed_shunt: Fixed shunt device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        bus, ickt = self.__extract_single_bus_device_id(fixed_shunt)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_fixed_shunt_integer_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_fixed_shunt_float_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_fixed_shunt_boolean_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_fixed_shunt_string_data(bus, ickt, par_name, value, self.toolkit_index)
        return

    def set_equivalent_device_data(self, equivalent_device, par_type, par_name, value):
        """
        Set equivalent device data.
        Args:
            (1) equivalent_device: Equivalent device device id in format of (bus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        bus, ickt = self.__extract_single_bus_device_id(equivalent_device)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_equivalent_device_integer_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_equivalent_device_float_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_equivalent_device_boolean_data(bus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_equivalent_device_string_data(bus, ickt, par_name, value, self.toolkit_index)
        return

    def set_line_data(self, line, par_type, par_name, value):
        """
        Set transmission line data.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_line_integer_data(ibus, jbus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_line_float_data(ibus, jbus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_line_boolean_data(ibus, jbus, ickt, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_line_string_data(ibus, jbus, ickt, par_name, value, self.toolkit_index)
        return

    def set_transformer_data(self, transformer, par_type, side, par_name, value):
        """
        Set transformer data.
        Args:
            (1) transformer: Transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) side: String of side. One of {"PRIMARY", "SECONDARY", "TERTIARY", "TRANSFORMER"}
            (4) par_name: String of parameter name.
            (5) value: Value of parameter.
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
        ickt = self.__get_c_char_p_of_string(ickt)
        side = self.__get_c_char_p_of_string(side)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_transformer_integer_data(ibus, jbus, kbus, ickt, side, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_transformer_float_data(ibus, jbus, kbus, ickt, side, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_transformer_boolean_data(ibus, jbus, kbus, ickt, side, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_transformer_string_data(ibus, jbus, kbus, ickt, side, par_name, value, self.toolkit_index)
        return

    def set_hvdc_data(self, hvdc, par_type, side, par_name, value):
        """
        Set HVDC link data.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) side: String of side. One of {"RECTIFIER", "INVERTER", "HVDC"}
            (4) par_name: String of parameter name.
            (5) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        side = self.__get_c_char_p_of_string(side)
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_hvdc_integer_data(ibus, jbus, ickt, side, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_hvdc_float_data(ibus, jbus, ickt, side, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_hvdc_boolean_data(ibus, jbus, ickt, side, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_hvdc_string_data(ibus, jbus, ickt, side, par_name, value, self.toolkit_index)
        return
    def set_hvdc_power(self, hvdc, p):
        """
        Set HVDC link power command.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) p: power command in MW.
        Rets: N/A
        Example:
            set_hvdc_power((1,2,"DC1"), 2000)
        """
        self.set_hvdc_data(hvdc, "F", "HVDC", "PDCN_MW", p)
        return
        
    def set_area_data(self, area, par_type, par_name, value):
        """
        Set area data.
        Args:
            (1) ownew: Area number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_area_integer_data(area, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_area_float_data(area, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_area_boolean_data(area, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_area_string_data(area, par_name, value, self.toolkit_index)
        return

    def set_zone_data(self, zone, par_type, par_name, value):
        """
        Set zone data.
        Args:
            (1) ownew: Zone number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_zone_integer_data(zone, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_zone_float_data(zone, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_zone_boolean_data(zone, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_zone_string_data(zone, par_name, value, self.toolkit_index)
        return

    def set_owner_data(self, owner, par_type, par_name, value):
        """
        Set owner data.
        Args:
            (1) ownew: Owner number.
            (2) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be done.
            The value MUST be consistent with the given parameter type. Otherwise, function may malfunction and package may exist with error.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_owner_integer_data(owner, par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_owner_float_data(owner, par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_owner_boolean_data(owner, par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_owner_string_data(owner, par_name, value, self.toolkit_index)
        return

    def set_dynamic_model(self, data, file_type):
        """
        Set dynamic model from string.
        Args:
            (1) data: String of model data.
            (2) file_type: Model data type.
        Rets: N/A
        """
        global STEPS_LIB
        data = self.__get_c_char_p_of_string(data)
        file_type = self.__get_c_char_p_of_string(file_type)        
        STEPS_LIB.api_set_dynamic_model(data, file_type, self.toolkit_index)
        return
    
    def get_generator_related_model_name(self, generator, model_type):
        """
        Get generator related model name.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) String of model name.
        Tips:
            If model type is not supported, empty string is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        model_name = self.__get_string_from_c_char_p(STEPS_LIB.api_get_generator_related_model_name(ibus, ickt, model_type, self.toolkit_index))
        if model_name=="":
            model_name = None
        return model_name

    def get_generator_related_model_data(self, generator, model_type, par_name):
        """
        Get generator related model data.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter
        Tips:
            If model type or parameter name is not supported, 0.0 is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_get_generator_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index)
        
    def set_generator_related_model_data(self, generator, model_type, par_name, value):
        """
        Set generator related model data.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            If model type or parameter name is not supported, nothing will be changed.
            If value is not a number, function may malfunction and package may exit with error.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_set_generator_related_model_float_parameter(ibus, ickt, model_type, par_name, value, self.toolkit_index)
    
    def get_generator_related_model_parameter_pair(self, generator, model_type):
        """
        Get generator related model parameter pair.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) Tuple of parameter name and value pairs. Each parameter name and value pair is in format of (string of parameter name, value of parameter).
        Tips:
            If model type is not supported, empty tuple is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        parameters = []
        n = STEPS_LIB.api_get_generator_related_model_float_parameter_count(ibus, ickt, model_type, self.toolkit_index)
        for parameter_index in range(n):
            par_name = STEPS_LIB.api_get_generator_related_model_float_parameter_name(ibus, ickt, model_type, parameter_index, self.toolkit_index)
            par_value = STEPS_LIB.api_get_generator_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index);
            par_name = self.__get_string_from_c_char_p(par_name)
            parameters.append((par_name, par_value))
        return tuple(parameters)
    
    def get_wt_generator_related_model_name(self, generator, model_type):
        """
        Get wind turbine generator related model name.
        Args:
            (1) generator: Wind turbine generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) String of model name.
        Tips:
            If model type is not supported, empty string is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        model_name = self.__get_string_from_c_char_p(STEPS_LIB.api_get_wt_generator_related_model_name(ibus, ickt, model_type, self.toolkit_index))
        if model_name=="":
            model_name = None
        return model_name

    def get_wt_generator_related_model_data(self, generator, model_type, par_name):
        """
        Get wind turbine generator related model data.
        Args:
            (1) generator: Wind turbine generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter
        Tips:
            If model type or parameter name is not supported, 0.0 is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_get_wt_generator_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index)
        
    def set_wt_generator_related_model_data(self, generator, model_type, par_name, value):
        """
        Set wind turbine generator related model data.
        Args:
            (1) generator: Wind turbine generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            If model type or parameter name is not supported, nothing will be changed.
            If value is not a number, function may malfunction and package may exit with error.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_set_wt_generator_related_model_float_parameter(ibus, ickt, model_type, par_name, value, self.toolkit_index)
        
    def get_wt_generator_related_model_parameter_pair(self, generator, model_type):
        """
        Get wind turbine generator related model parameter pair.
        Args:
            (1) generator: Wind turbine generator device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) Tuple of parameter name and value pairs. Each parameter name and value pair is in format of (string of parameter name, value of parameter).
        Tips:
            If model type is not supported, empty tuple is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        parameters = []
        n = STEPS_LIB.api_get_wt_generator_related_model_float_parameter_count(ibus, ickt, model_type, self.toolkit_index)
        for parameter_index in range(n):
            par_name = STEPS_LIB.api_get_wt_generator_related_model_float_parameter_name(ibus, ickt, model_type, parameter_index, self.toolkit_index)
            par_value = STEPS_LIB.api_get_wt_generator_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index);
            par_name = self.__get_string_from_c_char_p(par_name)
            parameters.append((par_name, par_value))
        return tuple(parameters)
        
    def get_pv_unit_related_model_name(self, pv_unit, model_type):
        """
        Get PV unit related model name.
        Args:
            (1) pv_unit: PV unit device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) String of model name.
        Tips:
            If model type is not supported, empty string is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(pv_unit)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        model_name = self.__get_string_from_c_char_p(STEPS_LIB.api_get_pv_unit_related_model_name(ibus, ickt, model_type, self.toolkit_index))
        if model_name=="":
            model_name = None
        return model_name

    def get_pv_unit_related_model_data(self, pv_unit, model_type, par_name):
        """
        Get PV unit related model data.
        Args:
            (1) pv_unit: PV unit device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter
        Tips:
            If model type or parameter name is not supported, 0.0 is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(pv_unit)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_get_pv_unit_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index)
        
    def set_pv_unit_related_model_data(self, pv_unit, model_type, par_name, value):
        """
        Set PV unit related model data.
        Args:
            (1) pv_unit: PV unit device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            If model type or parameter name is not supported, nothing will be changed.
            If value is not a number, function may malfunction and package may exit with error.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(pv_unit)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_set_pv_unit_related_model_float_parameter(ibus, ickt, model_type, par_name, value, self.toolkit_index)
        
    def get_pv_unit_related_model_parameter_pair(self, pv_unit, model_type):
        """
        Get pv unit related model parameter pair.
        Args:
            (1) pv_unit: PV unit device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) Tuple of parameter name and value pairs. Each parameter name and value pair is in format of (string of parameter name, value of parameter).
        Tips:
            If model type is not supported, empty tuple is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(pv_unit)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        parameters = []
        n = STEPS_LIB.api_get_pv_unit_related_model_float_parameter_count(ibus, ickt, model_type, self.toolkit_index)
        for parameter_index in range(n):
            par_name = STEPS_LIB.api_get_pv_unit_related_model_float_parameter_name(ibus, ickt, model_type, parameter_index, self.toolkit_index)
            par_value = STEPS_LIB.api_get_pv_unit_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index);
            par_name = self.__get_string_from_c_char_p(par_name)
            parameters.append((par_name, par_value))
        return tuple(parameters)
         
    def get_load_related_model_name(self, load, model_type):
        """
        Get load related model name.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) String of model name.
        Tips:
            If model type is not supported, empty string is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        model_name = self.__get_string_from_c_char_p(STEPS_LIB.api_get_load_related_model_name(ibus, ickt, model_type, self.toolkit_index))
        if model_name=="":
            model_name = None
        return model_name

    def get_load_related_model_data(self, load, model_type, par_name):
        """
        Get load related model data.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter
        Tips:
            If model type or parameter name is not supported, 0.0 is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_get_load_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index)
        
    def set_load_related_model_data(self, load, model_type, par_name, value):
        """
        Set load related model data.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            If model type or parameter name is not supported, nothing will be changed.
            If value is not a number, function may malfunction and package may exit with error.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_set_load_related_model_float_parameter(ibus, ickt, model_type, par_name, value, self.toolkit_index)
        
    def get_load_related_model_parameter_pair(self, load, model_type):
        """
        Get load related model parameter pair.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) Tuple of parameter name and value pairs. Each parameter name and value pair is in format of (string of parameter name, value of parameter).
        Tips:
            If model type is not supported, empty tuple is returned.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        parameters = []
        n = STEPS_LIB.api_get_load_related_model_float_parameter_count(ibus, ickt, model_type, self.toolkit_index)
        for parameter_index in range(n):
            par_name = STEPS_LIB.api_get_load_related_model_float_parameter_name(ibus, ickt, model_type, parameter_index, self.toolkit_index)
            par_value = STEPS_LIB.api_get_load_related_model_float_parameter(ibus, ickt, model_type, par_name, self.toolkit_index);
            par_name = self.__get_string_from_c_char_p(par_name)
            parameters.append((par_name, par_value))
        return tuple(parameters)
        
    def get_line_related_model_name(self, line, model_type):
        """
        Get transmission line related model name.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) String of model name.
        Tips:
            If model type is not supported, empty string is returned.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        model_name = self.__get_string_from_c_char_p(STEPS_LIB.api_get_line_related_model_name(ibus, jbus, ickt, model_type, self.toolkit_index))
        if model_name=="":
            model_name = None
        return model_name

    def get_line_related_model_data(self, line, model_type, par_name):
        """
        Get transmission line related model data.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter
        Tips:
            If model type or parameter name is not supported, 0.0 is returned.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_get_line_related_model_float_parameter(ibus, jbus, ickt, model_type, par_name, self.toolkit_index)
        
    def set_line_related_model_data(self, line, model_type, par_name, value):
        """
        Set transmission line related model data.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            If model type or parameter name is not supported, nothing will be changed.
            If value is not a number, function may malfunction and package may exit with error.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_set_line_related_model_float_parameter(ibus, jbus, ickt, model_type, par_name, value, self.toolkit_index)
        
    def get_line_related_model_parameter_pair(self, line, model_type):
        """
        Get transmission line related model parameter pair.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) Tuple of parameter name and value pairs. Each parameter name and value pair is in format of (string of parameter name, value of parameter).
        Tips:
            If model type is not supported, empty tuple is returned.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        parameters = []
        n = STEPS_LIB.api_get_line_related_model_float_parameter_count(ibus, jbus, ickt, model_type, self.toolkit_index)
        for parameter_index in range(n):
            par_name = STEPS_LIB.api_get_line_related_model_float_parameter_name(ibus, jbus, ickt, model_type, parameter_index, self.toolkit_index)
            par_value = STEPS_LIB.api_get_line_related_model_float_parameter(ibus, jbus, ickt, model_type, par_name, self.toolkit_index);
            par_name = self.__get_string_from_c_char_p(par_name)
            parameters.append((par_name, par_value))
        return tuple(parameters)
        
    def get_hvdc_related_model_name(self, hvdc, model_type):
        """
        Get HVDC link related model name.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) String of model name.
        Tips:
            If model type is not supported, empty string is returned.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        model_name = self.__get_string_from_c_char_p(STEPS_LIB.api_get_hvdc_related_model_name(ibus, jbus, ickt, model_type, self.toolkit_index))
        if model_name=="":
            model_name = None
        return model_name

    def get_hvdc_related_model_data(self, hvdc, model_type, par_name):
        """
        Get HVDC link related model data.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
        Rets:
            (1) Value of parameter
        Tips:
            If model type or parameter name is not supported, 0.0 is returned.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_get_hvdc_related_model_float_parameter(ibus, jbus, ickt, model_type, par_name, self.toolkit_index)
        
    def set_hvdc_related_model_data(self, hvdc, model_type, par_name, value):
        """
        Set HVDC linke related model data.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
            (3) par_name: String of parameter name.
            (4) value: Value of parameter.
        Rets: N/A
        Tips:
            If model type or parameter name is not supported, nothing will be changed.
            If value is not a number, function may malfunction and package may exit with error.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        par_name = self.__get_c_char_p_of_string(par_name)
        return STEPS_LIB.api_set_hvdc_related_model_float_parameter(ibus, jbus, ickt, model_type, par_name, value, self.toolkit_index)
        
    def get_hvdc_related_model_parameter_pair(self, hvdc, model_type):
        """
        Get HVDC link related model parameter pair.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) model_type: String of model type.
        Rets:
            (1) Tuple of parameter name and value pairs. Each parameter name and value pair is in format of (string of parameter name, value of parameter).
        Tips:
            If model type is not supported, empty tuple is returned.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        model_type = self.__get_c_char_p_of_string(model_type)
        parameters = []
        n = STEPS_LIB.api_get_hvdc_related_model_float_parameter_count(ibus, jbus, ickt, model_type, self.toolkit_index)
        for parameter_index in range(n):
            par_name = STEPS_LIB.api_get_hvdc_related_model_float_parameter_name(ibus, jbus, ickt, model_type, parameter_index, self.toolkit_index)
            par_value = STEPS_LIB.api_get_hvdc_related_model_float_parameter(ibus, jbus, ickt, model_type, par_name, self.toolkit_index);
            par_name = self.__get_string_from_c_char_p(par_name)
            parameters.append((par_name, par_value))
        return tuple(parameters)
        
    def get_powerflow_solver_parameter(self, par_type, par_name):
        """
        Get powerflow solver configuration parameter.
        Args:
            (1) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (2) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN']:
            return None
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_powerflow_solver_integer_parameter(par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_powerflow_solver_float_parameter(par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_powerflow_solver_boolean_parameter(par_name, self.toolkit_index)
        return None

    def set_powerflow_solver_parameter(self, par_type, par_name, value):
        """
        Set powerflow solver configuration parameter.
        Args:
            (1) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (2) par_name: String of parameter name.
            (3) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be changed.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN']:
            return
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_powerflow_solver_integer_parameter(par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_powerflow_solver_float_parameter(par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_powerflow_solver_boolean_parameter(par_name, value, self.toolkit_index)
        return
    
    def show_powerflow_solver_configuration(self):
        """
        Show powerflow solver configuration. Report is sent to log.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_show_powerflow_solver_configuration(self.toolkit_index)
        return
        
    def solve_powerflow(self, method):
        """
        Solve powerflow.
        Args:
            (1) method: String of powerflow solution method. Should be one of {"NR", "PQ"}
        Rets: N/A
        """
        global STEPS_LIB
        method = self.__get_c_char_p_of_string(method)
        STEPS_LIB.api_solve_powerflow(method, self.toolkit_index)
        return

    def is_powerflow_converged(self):
        """
        Check if powerflow is converged or not.
        Args: N/A
        Rets:
            (1) Boolean value. True for converged, False for not converged.
        """
        global STEPS_LIB
        return STEPS_LIB.api_is_powerflow_converged(self.toolkit_index)
    
    def get_powerflow_loss(self):
        """
        Get active power loss of solved powerflow.
        Args: N/A
        Rets:
            (1) System power loss in MW.
        Tips:
            If powerflow is not converged, the return result is meaningless.
        """
        global STEPS_LIB
        p_gen = 0.0
        gens = self.get_all_generators()
        for gen in gens:
            p_gen += self.get_generator_data(gen, 'd', 'Pgen_MW')
            
        gens = self.get_all_wt_generators()
        for gen in gens:
            p_gen += self.get_wt_generator_data(gen, 'd', 'Pgen_MW')
            
        pvs = self.get_all_pv_units()
        for pv in pvs:
            p_gen += self.get_pv_unit_data(pv, 'd', 'Pgen_MW')
            
        eses = self.get_all_energy_storages()
        for es in eses:
            p_gen += self.get_energy_storage_data(es, 'd', 'Pgen_MW')

        p_load = 0.0
        loads = self.get_all_loads()
        for load in loads:
            p_load += self.get_load_data(load, 'd', 'P_MW')
            
        return p_gen-p_load
        
            
    def show_powerflow_result(self):
        """
        Show powerflow result in log.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_show_powerflow_result(self.toolkit_index)
        return
        
    def save_powerflow_result(self, file):
        """
        Save powerflow result to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        Tips:
            The result exported by save_powerflow_result() is briefer than that exported by save_extended_powerflow_result().
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_powerflow_result(file, self.toolkit_index)
        return
    
    def save_extended_powerflow_result(self, file):
        """
        Save extended powerflow result to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        Tips:
            The result exported by save_extended_powerflow_result() is more detailed than that exported by save_powerflow_result().
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_extended_powerflow_result(file, self.toolkit_index)
        return
        
    def save_jacobian_matrix(self, file):
        """
        Save jacobian matrix of powerflow solver to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_jacobian_matrix(file, self.toolkit_index)
        return

    def build_network_Y_matrix(self):
        """
        Build newwork complex Y matrix for powerflow solution.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_build_network_Y_matrix(self.toolkit_index)
        return

    def build_decoupled_network_B_matrix(self):
        """
        Build newwork real B' and B" matrix for decoupled powerflow solution.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_build_decoupled_network_B_matrix(self.toolkit_index)
        return

    def build_dc_network_B_matrix(self):
        """
        Build newwork real B matrix for DC powerflow solution.
        Args: N/A
        Rets: N/A
        Tips:
            DC powerflow solution is not supported.
        """
        global STEPS_LIB
        STEPS_LIB.api_build_dc_network_B_matrix(self.toolkit_index)
        return

    def build_dynamic_network_Y_matrix(self):
        """
        Build newwork complex Y matrix for dynamic simulation.
        Args: N/A
        Rets: N/A
        Tips:
            The faults and source impedance are included in the Y matrix.
        """
        global STEPS_LIB
        STEPS_LIB.api_build_dynamic_network_Y_matrix(self.toolkit_index)
        return

    def build_network_Z_matrix(self):
        """
        Build newwork complex Z matrix.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_build_network_Z_matrix(self.toolkit_index)
        return
        
    def save_network_Y_matrix(self, file):
        """
        Save newwork complex Y matrix to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_network_Y_matrix(file, self.toolkit_index)
        return
        
    def save_decoupled_network_B_matrix(self, file):
        """
        Save newwork decoupled real B' and B" matrix to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_decoupled_network_B_matrix(file, self.toolkit_index)
        return
        
    def save_dc_network_B_matrix(self, file):
        """
        Save newwork real DC B matrix to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_dc_network_B_matrix(file, self.toolkit_index)
        return
        
    def save_dynamic_network_Y_matrix(self, file):
        """
        Save newwork dynamic complex Y matrix to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_dynamic_network_Y_matrix(file, self.toolkit_index)
        return
        
    def save_network_Z_matrix(self, file):
        """
        Save newwork complex Z matrix to file.
        Args:
            (1) file: String of target file name.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        STEPS_LIB.api_save_network_Z_matrix(file, self.toolkit_index)
        return
        
        
    def get_dynamic_simulator_parameter(self, par_type, par_name):
        """
        Get dynamic simulator configuration parameter.
        Args:
            (1) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (2) par_name: String of parameter name.
        Rets:
            (1) Value of parameter.
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, 0, 0.0, "", or False will be returned.
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return int(STEPS_LIB.api_get_dynamic_simulator_integer_parameter(par_name, self.toolkit_index))
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_get_dynamic_simulator_float_parameter(par_name, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_get_dynamic_simulator_boolean_parameter(par_name, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            return self.__get_string_from_c_char_p(STEPS_LIB.api_get_dynamic_simulator_string_parameter(par_name, self.toolkit_index))
        return None

    def set_dynamic_simulator_parameter(self, par_type, par_name, value):
        """
        Set dynamic simulator configuration parameter.
        Args:
            (1) par_type: String of parameter type. Choose one from {"I", "F", "D", "S", "B"}.
            (2) par_name: String of parameter name.
            (3) value: Value of parameter.
        Rets: N/A
        Tips:
            The par_type meaning: "I": integer number, "F" or "D": float number, "S": string, "B": boolean data.
            The type of given parameter MUST be consistent with the given parameter type. Otherwise, nothing will be changed
        """
        global STEPS_LIB
        par_type = par_type.upper()
        if par_type not in ['I', 'INT', 'INTEGER', 'F', 'D', 'FLOAT', 'DOUBLE', 'B', 'BOOL', 'BOOLEAN', 'S', 'STRING']:
            return None
        par_name = self.__get_c_char_p_of_string(par_name)
        if par_type in ['I', 'INT', 'INTEGER']:
            return STEPS_LIB.api_set_dynamic_simulator_integer_parameter(par_name, value, self.toolkit_index)
        if par_type in ['F', 'D', 'FLOAT', 'DOUBLE']:
            return STEPS_LIB.api_set_dynamic_simulator_float_parameter(par_name, value, self.toolkit_index)
        if par_type in ['B', 'BOOL', 'BOOLEAN']:
            return STEPS_LIB.api_set_dynamic_simulator_boolean_parameter(par_name, value, self.toolkit_index)
        if par_type in ['S', 'STRING']:
            value = self.__get_c_char_p_of_string(value)
            return STEPS_LIB.api_set_dynamic_simulator_string_parameter(par_name, value, self.toolkit_index)
        return None
        
    def get_dynamic_simulator_output_file(self):
        """
        Get dynamic simulator output file name.
        Args: N/A
        Rets:
            (1) String of output file name.
        """
        global STEPS_LIB
        return self.__get_string_from_c_char_p(STEPS_LIB.api_get_dynamic_simulator_output_file(self.toolkit_index))
        
    def set_dynamic_simulator_output_file(self, file):
        """
        Set dynamic simulator output file name.
        Args:
            (1) file: String of output file name.
        Rets: N/A
        """
        global STEPS_LIB
        file = self.__get_c_char_p_of_string(file)
        return STEPS_LIB.api_set_dynamic_simulator_output_file(file, self.toolkit_index)
        
    def get_dynamic_simulation_time_step(self):
        """
        Get dynamic simulation time step.
        Args: N/A
        Rets:
            (1) Value of dynamic simulation time step in seconds.
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_dynamic_simulation_time_step(self.toolkit_index)
        
    def set_dynamic_simulation_time_step(self, step):
        """
        Set dynamic simulation time step.
        Args:
            (1) step: Dynamic simulation time step in seconds.
        Rets: N/A
        Tips:
            The time step MUST be less than 1/2 of the least time constant of all dynamic models. It is general practice to set time step to 1/4 of the least time constant.
            Run check_least_dynamic_time_constants() to report the least time constants.
        """
        global STEPS_LIB
        return STEPS_LIB.api_set_dynamic_simulation_time_step(step, self.toolkit_index)

    def show_dynamic_simulation_configuration(self):
        """
        Show dynamic simulation configuration. Report is sent to log.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_show_dynamic_simulation_configuration(self.toolkit_index)
        return
    
    def get_dynamic_simulation_time(self):
        """
        Get current dynamic simulation time.
        Args: N/A
        Rets:
            (1) Value of dynamic simulation time in seconds.
        Tips:
            In STEPS, the minimum simulation time is -2*simulation time step.
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_dynamic_simulation_time(self.toolkit_index)
        
    def clear_meters(self):
        """
        Clear all meters in the current simulator.
        Args: N/A
        Rets: N/A
        Tips:
            If STEPS() is created with is_default=True, this api can help to clear all meters to avoid adding duplicate meters. 
        """
        global STEPS_LIB
        STEPS_LIB.api_clear_meters(self.toolkit_index)
        return
  
    def prepare_meters(self, device_type):
        """
        Automatically prepare general meters of all devices of specific device type.
        Args:
            (1) device_type: String of device type.
        Rets: N/A
        Tips:
            The device type should be one of {"ALL", "BUS", "GENERATOR", "WT GENERATOR", "PV UNIT", "ENERGY STORAGE", "LOAD", "LINE", "TRANSFORMER", "HVDC", "EQUIVALENT DEVICE"}.
            If "ALL" is set, all general meters of {"BUS", "GENERATOR", "WT GENERATOR", "PV UNIT", "ENERGY STORAGE", "LOAD", "LINE", "TRANSFORMER", "HVDC", "EQUIVALENT DEVICE"} are set.
            For the supported general meters, see implementation of the following functions of STEPS:
                DYNAMIC_SIMULATOR::prepare_bus_related_meters()
                DYNAMIC_SIMULATOR::prepare_generator_related_meters()
                DYNAMIC_SIMULATOR::prepare_wt_generator_related_meters()
                DYNAMIC_SIMULATOR::prepare_pv_unit_related_meters()
                DYNAMIC_SIMULATOR::prepare_energy_storage_related_meters()
                DYNAMIC_SIMULATOR::prepare_load_related_meters()
                DYNAMIC_SIMULATOR::prepare_line_related_meters()
                DYNAMIC_SIMULATOR::prepare_transformer_related_meters()
                DYNAMIC_SIMULATOR::prepare_hvdc_related_meters()
                DYNAMIC_SIMULATOR::prepare_equivalent_device_related_meters()                
        """
        global STEPS_LIB
        device_type = device_type.upper()
        if device_type not in ['ALL', 'BUS', 'GENERATOR', 'WT GENERATOR', 'PV UNIT', 'ENERGY STORAGE', 'LOAD', 'LINE', 'TRANSFORMER', 'HVDC', 'EQUIVALENT DEVICE']:
            return
        if device_type in ['ALL']:
            STEPS_LIB.api_prepare_meters(self.toolkit_index)
            return
        if device_type in ['BUS']:
            STEPS_LIB.api_prepare_bus_related_meters(self.toolkit_index)
            return
        if device_type in ['GENERATOR']:
            STEPS_LIB.api_prepare_generator_related_meters(self.toolkit_index)
            return
        if device_type in ['WT GENERATOR']:
            STEPS_LIB.api_prepare_wt_generator_related_meters(self.toolkit_index)
            return
        if device_type in ['PV UNIT']:
            STEPS_LIB.api_prepare_pv_unit_related_meters(self.toolkit_index)
            return
        if device_type in ['ENERGY STORAGE']:
            STEPS_LIB.api_prepare_energy_storage_related_meters(self.toolkit_index)
            return
        if device_type in ['LOAD']:
            STEPS_LIB.api_prepare_load_related_meters(self.toolkit_index)
            return
        if device_type in ['LINE']:
            STEPS_LIB.api_prepare_line_related_meters(self.toolkit_index)
            return
        if device_type in ['TRANSFORMER']:
            STEPS_LIB.api_prepare_transformer_related_meters(self.toolkit_index)
            return
        if device_type in ['HVDC']:
            STEPS_LIB.api_prepare_hvdc_related_meters(self.toolkit_index)
            return
        if device_type in ['EQUIVALENT DEVICE']:
            STEPS_LIB.api_prepare_equivalent_device_related_meters(self.toolkit_index)
            return
        return

    def prepare_bus_meter(self, bus, meter_type):
        """
        Prepare specific bus meter.
        Args:
            (1) bus: Bus number.
            (2) meter_type: String of bus type.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_bus_related_meter() 
        """
        global STEPS_LIB
        meter_type = self.__get_c_char_p_of_string(meter_type)
        STEPS_LIB.api_prepare_bus_related_meter(bus, meter_type, self.toolkit_index)
        return

    def prepare_generator_meter(self, generator, meter_type, var_name=""):
        """
        Prepare specific generator meter.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) meter_type: String of bus type.
            (3) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_generator_related_meter()
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_generator_related_meter(bus, ickt, meter_type, var_name, self.toolkit_index)
        return

    def prepare_wt_generator_meter(self, generator, meter_type, var_name=""):
        """
        Prepare specific wind turbine generator meter.
        Args:
            (1) generator: Wind turbine generator device id in format of (bus, ickt).
            (2) meter_type: String of bus type.
            (3) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_wt_generator_related_meter()
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_wt_generator_related_meter(bus, ickt, meter_type, var_name, self.toolkit_index)
        return

    def prepare_pv_unit_meter(self, pvunit, meter_type, var_name=""):
        """
        Prepare specific PV unit meter.
        Args:
            (1) pvunit: PV unit device id in format of (bus, ickt).
            (2) meter_type: String of bus type.
            (3) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_pv_unit_related_meter()
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(pvunit)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_pv_unit_related_meter(bus, ickt, meter_type, var_name, self.toolkit_index)
        return

    def prepare_energy_storage_meter(self, estorage, meter_type, var_name=""):
        """
        Prepare specific energy storage meter.
        Args:
            (1) estorage: Energy storage device id in format of (bus, ickt).
            (2) meter_type: String of bus type.
            (3) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_energy_storage_related_meter()
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(estorage)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_energy_storage_related_meter(bus, ickt, meter_type, var_name, self.toolkit_index)
        return

    def prepare_load_meter(self, load, meter_type, var_name=""):
        """
        Prepare specific load meter.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) meter_type: String of bus type.
            (3) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_load_related_meter()
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_load_related_meter(bus, ickt, meter_type, var_name, self.toolkit_index)
        return

    def prepare_line_meter(self, line, meter_type, side, var_name=""):
        """
        Prepare specific transmission line meter.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) meter_type: String of bus type.
            (3) side: String of line side. One of {"SENDING", "RECEIVING"} or {"S", "R"}.
            (4) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_line_related_meter()
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        side = self.__get_c_char_p_of_string(side)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_line_related_meter(ibus, jbus, ickt, meter_type, side, var_name, self.toolkit_index)
        return

    def prepare_transformer_meter(self, trans, meter_type, side, var_name=""):
        """
        Prepare specific transformer meter.
        Args:
            (1) trans: Transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
            (2) meter_type: String of bus type.
            (3) side: String of transformer side. One of {"PRIMARY", "SECONDARY", "TERTIARY"} or {"P", "S", "T"}.
            (4) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_transformer_related_meter()
        """
        global STEPS_LIB
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(trans)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        side = self.__get_c_char_p_of_string(side)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_transformer_related_meter(ibus, jbus, kbus, ickt, meter_type, side, var_name, self.toolkit_index)
        return

    def prepare_hvdc_meter(self, hvdc, meter_type, side, var_name=""):
        """
        Prepare specific HVDC link meter.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) meter_type: String of bus type.
            (3) side: String of converter side. One of {"RECTIFIER", "INVERTER"} or {"R", "I"}.
            (4) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_hvdc_related_meter()
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        side = self.__get_c_char_p_of_string(side)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_hvdc_related_meter(ibus, jbus, ickt, meter_type, side, var_name, self.toolkit_index)
        return

    def prepare_equivalent_device_meter(self, edevice, meter_type, var_name=""):
        """
        Prepare specific equivalent device meter.
        Args:
            (1) edevice: Equivalent device device id in format of (bus, ickt).
            (2) meter_type: String of bus type.
            (3) var_name: String of internal variable name. Only valid when meter type is internal variable of dynamic models.
        Rets: N/A
        Tips:
            For the supported meter types, see implementation of the following function of STEPS:
                DYNAMIC_SIMULATOR::prepare_equivalent_device_related_meter()
        """
        global STEPS_LIB
        bus, ickt = self.__extract_single_bus_device_id(equivalent_device)
        ickt = self.__get_c_char_p_of_string(ickt)
        meter_type = self.__get_c_char_p_of_string(meter_type)
        var_name = self.__get_c_char_p_of_string(var_name)
        STEPS_LIB.api_prepare_equivalent_device_related_meter(bus, ickt, meter_type, var_name, self.toolkit_index)
        return

    def start_dynamic_simulation(self):
        """
        Start dynamic simulation. Dynamic initialization is performed.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_start_dynamic_simulation(self.toolkit_index)
        return

    def stop_dynamic_simulation(self):
        """
        Stop dynamic simulation. No further dynamic simulation should be performed once dynamic simulation is stopped.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_stop_dynamic_simulation(self.toolkit_index)
        return

    def run_dynamic_simulation_to_time(self, time):
        """
        Run dynamic simulation to time.
        Args:
            (1) time: Time in second.
        Rets: N/A
        Tips:
            The input time is the time when the dynamic simulation is paused. For example, if the current dynamic simulation time returned from get_dynamic_simulation_time() is 1.0s, and the returned time of get_dynamic_simulation_time() will become 1.5s after run_dynamic_simulation_to_time(1.5) is called.
        """
        global STEPS_LIB
        STEPS_LIB.api_run_simulation_to_time(time, self.toolkit_index)
        return

    def run_a_step(self):
        """
        Run a dynamic simulation step. The dynamic simulation time is increased by one time step once the function is called.
        Args: N/A
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_run_a_step(self.toolkit_index)
        return

    def is_system_angular_stable(self):
        """
        Check if the system is angular stable or not. It is only VALID when system rotor angle stability surveillance flag is enabled.
        If the surveillance flag is not enabled, True is always returned.
        Args: N/A
        Rets:
            (1) flag: True if system is angular stable, and False if unstable.
        Tips:
            If the surveillance flag is enabled, False is returned if the maximum rotor angle difference in any island exceeds the threshold.
            Other, True is returned.
        """
        global STEPS_LIB
        return STEPS_LIB.api_get_system_angular_stable_flag(self.toolkit_index)

    def set_bus_fault(self, bus, fault_type, fault_shunt):
        """
        Set bus fault.
        Args:
            (1) bus: Bus number.
            (2) fault_type: String of fault type. Currently, only "THREE PHASE FAULT" is supported.
            (3) fault_shunt: Complex per unit fault shunt in the form of (g+jb).
        Rets: N/A
        Tips:
            The fault shunt is represented as conductance and susceptance based on system base power and bus base voltage.
            The susceptance is usually set as NEGATIVE to mimic the voltage drop due to fault.
            The absolute value of the fault shunt should not be too great. Otherwise, network solution may fail to converge. Typically, |b|<1e6.
        """
        global STEPS_LIB
        fault_type = self.__get_c_char_p_of_string(fault_type)
        STEPS_LIB.api_set_bus_fault(bus, fault_type, fault_shunt[0], fault_shunt[1], self.toolkit_index)
        return

    def clear_bus_fault(self, bus, fault_type):
        """
        Clear bus fault without tripping bus.
        Args:
            (1) bus: Bus number.
            (2) fault_type: String of fault type. Currently, only "THREE PHASE FAULT" is supported.
        Rets: N/A
        """
        global STEPS_LIB
        fault_type = self.__get_c_char_p_of_string(fault_type)
        STEPS_LIB.api_clear_bus_fault(bus, fault_type, self.toolkit_index)
        return

    def trip_bus(self, bus):
        """
        Trip bus. All devices connecting to the bus are disconnected.
        Args:
            (1) bus: Bus number.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_trip_bus(bus, self.toolkit_index)
        return

    def set_line_fault(self, line, fault_type, fault_location, fault_shunt):
        """
        Set transmission line fault.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) fault_type: String of fault type. Currently, only "THREE PHASE FAULT" is supported.
            (3) fault_location: Relative fault location to ibus.
            (4) fault_shunt: Complex per unit fault shunt in the form of (g+jb).
        Rets: N/A
        Tips:
            The fault location should be in the range of [0, 1.0], including 0 and 1.0. It represent the relative location of the fault on the line to the ibus.
            For example, 0.5 means the fault is set at the middle of the line. 0 means the fault is set at exactly ibus. 1.0 means the fault is set at exactly jbus.
            The fault shunt is represented as conductance and susceptance based on system base power and bus base voltage.
            The susceptance is usually set as NEGATIVE to mimic the voltage drop due to fault.
            The absolute value of the fault shunt should not be too great. Otherwise, network solution may fail to converge. Typically, |b|<1e6.
            Multiple faults are supported on single line at different fault locations.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        fault_type = self.__get_c_char_p_of_string(fault_type)
        STEPS_LIB.api_set_line_fault(ibus, jbus, ickt, fault_type, fault_location, fault_shunt[0], fault_shunt[1], self.toolkit_index)
        return

    def clear_line_fault(self, line, fault_type, fault_location):
        """
        Clear transmission line fault without tripping the line.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) fault_type: String of fault type. Currently, only "THREE PHASE FAULT" is supported.
            (3) fault_location: Relative fault location to ibus.
        Rets: N/A
        Tips:
            The fault location should be in the range of [0, 1.0], including 0 and 1.0. It represent the relative location of the fault on the line to the ibus.
            For example, 0.5 means the fault at the middle of the line will be cleared. 0 means the fault at ibus will be cleared. 1.0 means the fault at jbus will be cleared.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        fault_type = self.__get_c_char_p_of_string(fault_type)
        STEPS_LIB.api_clear_line_fault(ibus, jbus, ickt, fault_type, fault_location, self.toolkit_index)
        return

    def trip_line(self, line):
        """
        Trip transmission line. Breakers at the two sides of the line are both tripped.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_trip_line(ibus, jbus, ickt, self.toolkit_index)
        return

    def trip_line_breaker(self, line, side):
        """
        Trip transmission line breaker at specific side.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) side: String of transmission line side. One of {"SENDING", "RECEIVING"} or {"S", "R"}.
        Rets: N/A
        Tips:
            The sending side bus is not necessarily ibus. The receiving bus is not necessarily jbus.
            It is up to the user to check which side to trip.
        """
        global STEPS_LIB
        if side not in line:
            return
        else:
            ibus, jbus, ickt = self.__extract_single_bus_device_id(line)
            ickt = self.__get_c_char_p_of_string(ickt)
            
            if ibus==side:
                STEPS_LIB.api_trip_line_breaker(ibus, jbus, ickt, self.toolkit_index)
            else:
                STEPS_LIB.api_trip_line_breaker(jbus, ibus, ickt, self.toolkit_index)
        return
        

    def close_line(self, line):
        """
        Close transmission line. Breakers at the two sides of the line are both closed.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(line)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_close_line(ibus, jbus, ickt, self.toolkit_index)
        return

    def close_line_breaker(self, line, side):
        """
        Close transmission line breaker at specific side.
        Args:
            (1) line: Transmission line device id in format of (ibus, jbus, ickt).
            (2) side: String of transmission line side. One of {"SENDING", "RECEIVING"} or {"S", "R"}.
        Rets: N/A
        Tips:
            The sending side bus is not necessarily ibus. The receiving bus is not necessarily jbus.
            It is up to the user to check which side to close.
        """
        global STEPS_LIB
        if side not in line:
            return
        else:
            ibus, jbus, ickt = self.__extract_single_bus_device_id(line)
            ickt = self.__get_c_char_p_of_string(ickt)
            
            if ibus==side:
                STEPS_LIB.api_close_line_breaker(ibus, jbus, ickt, self.toolkit_index)
            else:
                STEPS_LIB.api_close_line_breaker(jbus, ibus, ickt, self.toolkit_index)
        return
        

    def trip_transformer(self, transformer):
        """
        Trip transformer. Breakers at the two or three winding sides of the transformer are all tripped.
        Args:
            (1) transformer: Transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
        """
        global STEPS_LIB
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_trip_transformer(ibus, jbus, kbus, ickt, self.toolkit_index)
        return

    def trip_transformer_breaker(self, transformer, side):
        """
        Trip transformer breaker at specific side.
        Args:
            (1) transformer: Transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
            (2) side: String of transformer winding side. One of {"PRIMARY", "SECONDARY", "TERTIARY"} or {"P", "S", "T"}.
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
            The primary side bus is not necessarily ibus. The secondary bus is not necessarily jbus. The tertiary bus is not necessarily kbus.
            It is up to the user to check which side to trip.
        """
        global STEPS_LIB
        if side not in transformer or side==0:
            return
        else:
            ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
            ickt = self.__get_c_char_p_of_string(ickt)
            if ibus == side:
                STEPS_LIB.api_trip_transformer_breaker(ibus, jbus, kbus, ickt, self.toolkit_index)
            elif jbus == side:
                STEPS_LIB.api_trip_transformer_breaker(jbus, ibus, kbus, ickt, self.toolkit_index)
            else:
                STEPS_LIB.api_trip_transformer_breaker(kbus, ibus, jbus, ickt, self.toolkit_index)
        return
        

    def close_transformer(self, transformer):
        """
        Close transformer. Breakers at the two or three winding sides of the transformer are all closed.
        Args:
            (1) transformer: Transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
        """
        global STEPS_LIB
        ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_close_transformer(ibus, jbus, kbus, ickt, self.toolkit_index)
        return

    def close_transformer_breaker(self, transformer, side):
        """
        Close transformer breaker at specific side.
        Args:
            (1) transformer: Transformer device id in format of (ibus, jbus, ickt) or (ibus, jbus, kbus, ickt).
            (2) side: String of transformer winding side. One of {"PRIMARY", "SECONDARY", "TERTIARY"} or {"P", "S", "T"}.
        Rets: N/A
        Tips:
            kbus can be omitted if kbus=0, a.k.a., (ibus, jbus, 0, ickt) can be simplified as (ibus, jbus, ickt).
            The primary side bus is not necessarily ibus. The secondary bus is not necessarily jbus. The tertiary bus is not necessarily kbus.
            It is up to the user to check which side to close.
        """
        global STEPS_LIB
        if side not in transformer or side==0:
            return
        else:
            ibus, jbus, kbus, ickt = self.__extract_triple_bus_device_id(transformer)
            ickt = self.__get_c_char_p_of_string(ickt)
            if ibus == side:
                STEPS_LIB.api_close_transformer_breaker(ibus, jbus, kbus, ickt, self.toolkit_index)
            elif jbus == side:
                STEPS_LIB.api_close_transformer_breaker(jbus, ibus, kbus, ickt, self.toolkit_index)
            else:
                STEPS_LIB.api_trip_tapi_close_transformer_breakerransformer_breaker(kbus, ibus, jbus, ickt, self.toolkit_index)
        return
        
    def trip_generator(self, generator):
        """
        Trip generator.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_trip_generator(ibus, ickt, self.toolkit_index)
        return

    def shed_generator(self, generator, percent):
        """
        Shed generator by percent.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) percent: Per unit percent of the generator to shed.
        Rets: N/A
        Tips:
            The percent is USUALLY in range [0, 1.0] including 0 and 1.0. If percent=0.0, generator is not shed at all. If percent=1.0, the generator will be tripped.
            The percent CAN be set as negative to mimic increase of generation. But it is rarely used.
            If a generator with MBASE=100MVA is shed by 0.2, its MBASE becomes 80MVA. If it is then shed by 0.3, its MBASE becomes 56MVA.            
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_shed_generator(ibus, ickt, percent, self.toolkit_index)
        return
        
    def trip_wt_generator(self, generator, n):
        """
        Trip wind turbine generator.
        Args:
            (1) generator: Wind turbine generator device id in format of (bus, ickt).
            (2) n: Number of lumped wind turbine generators to trip.
        Rets: N/A
        Tips:
            The number of lunmped wind turbine generators should be less than the available lumped wind turbine generators.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_trip_wt_generator(ibus, ickt, n, self.toolkit_index)
        return

    def shed_generator(self, generator, percent):
        """
        Shed wind turbine generator by percent.
        Args:
            (1) generator: Wind turbine generator device id in format of (bus, ickt).
            (2) percent: Per unit percent of the wind turbine generator to shed.
        Rets: N/A
        Tips:
            The percent is USUALLY in range [0, 1.0] including 0 and 1.0. If percent=0.0, wind turbine generator is not shed at all. If percent=1.0, the wind turbine generator will be totally tripped.
            The percent CAN be set as negative to mimic increase of wind turbine generation. But it is rarely used.
            If a wind turbine generator with MBASE=100MVA is shed by 0.2, its MBASE becomes 80MVA. If it is then shed by 0.3, its MBASE becomes 56MVA.            
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_shed_wt_generator(ibus, ickt, percent, self.toolkit_index)
        return

    def trip_load(self, load):
        """
        Trip load.
        Args:
            (1) load: Load device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_trip_load(ibus, ickt, self.toolkit_index)
        return

    def close_load(self, load):
        """
        Close load.
        Args:
            (1) load: Load device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_close_load(ibus, ickt, self.toolkit_index)
        return

    def scale_load(self, load, percent):
        """
        Scale load by percent.
        Args:
            (1) load: Load device id in format of (bus, ickt).
            (2) percent: Per unit percent of the load to scale. Positve for scaling up, and Negative for scaling down.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(load)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_scale_load(ibus, ickt, percent, self.toolkit_index)
        return

    def scale_all_loads(self, percent):
        """
        Scale all loads by percent.
        Args:
            (1) percent: Per unit percent of all loads to scale. Positve for scaling up, and Negative for scaling down.
        Rets: N/A
        """
        global STEPS_LIB
        STEPS_LIB.api_scale_all_loads(percent, self.toolkit_index)
        return

    def trip_fixed_shunt(self, shunt):
        """
        Trip fixed shunt.
        Args:
            (1) shunt: Fixed shunt device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(shunt)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_trip_fixed_shunt(ibus, ickt, self.toolkit_index)
        return

    def close_fixed_shunt(self, shunt):
        """
        Close fixed shunt.
        Args:
            (1) shunt: Fixed shunt device id in format of (bus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(shunt)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_close_fixed_shunt(ibus, ickt, self.toolkit_index)
        return

    def manually_bypass_hvdc(self, hvdc):
        """
        Manually bypass HVDC link.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
        Rets: N/A
        Tips:
            The HVDC link won't recover unless manually_unbypass_hvdc() is called.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_manually_bypass_hvdc(ibus, jbus, ickt, self.toolkit_index)
        return

    def manually_block_hvdc(self, hvdc):
        """
        Manually block HVDC link.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
        Rets: N/A
        Tips:
            The HVDC link won't recover unless manually_unblock_hvdc() is called.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_manually_block_hvdc(ibus, jbus, ickt, self.toolkit_index)
        return

    def manually_unbypass_hvdc(self, hvdc):
        """
        Manually unbypass HVDC link.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_manually_unbypass_hvdc(ibus, jbus, ickt, self.toolkit_index)
        return

    def manually_unblock_hvdc(self, hvdc):
        """
        Manually unblock HVDC link.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        STEPS_LIB.api_manually_unblock_hvdc(ibus, jbus, ickt, self.toolkit_index)
        return

    def get_generator_voltage_reference_in_pu(self, generator):
        """
        Get generator voltage reference of exciter model. If there is no exciter model for the generator, 0 will be returned.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
        Rets:
            (1) Voltage reference in pu.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_get_generator_voltage_reference_in_pu(ibus, ickt, self.toolkit_index)

    def get_generator_mechanical_power_reference_in_pu(self, generator):
        """
        Get generator mechanical power reference of turbine governor model. If there is no turbine governor model for the generator, 0 will be returned.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
        Rets:
            (1) Mechanical power reference in pu based on generator MBASE.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_get_generator_mechanical_power_reference_in_pu_based_on_mbase(ibus, ickt, self.toolkit_index)

    def get_generator_mechanical_power_reference_in_MW(self, generator):
        """
        Get generator mechanical power reference of turbine governor model. If there is no turbine governor model for the generator, 0 will be returned.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
        Rets:
            (1) Mechanical power reference in MW.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_get_generator_mechanical_power_reference_in_MW(ibus, ickt, self.toolkit_index)

    def set_generator_voltage_reference_in_pu(self, generator, value):
        """
        Set generator voltage reference of exciter model. If there is no exciter model for the generator, nothing will be changed.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) value: New voltage reference in pu.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_set_generator_voltage_reference_in_pu(ibus, ickt, value, self.toolkit_index)

    def set_generator_mechanical_power_reference_in_pu(self, generator, value):
        """
        Set generator mechanical power reference of turbine governor model. If there is no turbine governor model for the generator, nothing will be changed.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) value: New mechanical power reference in pu based on generator MBASE.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_set_generator_mechanical_power_reference_in_pu_based_on_mbase(ibus, ickt, value, self.toolkit_index)
        
    def set_generator_mechanical_power_reference_in_MW(self, generator, value):
        """
        Set generator mechanical power reference of turbine governor model. If there is no turbine governor model for the generator, nothing will be changed.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) value: New mechanical power reference in MW.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_set_generator_mechanical_power_reference_in_MW(ibus, ickt, value, self.toolkit_index)
        
    def get_generator_excitation_voltage_in_pu(self, generator):
        """
        Get generator excitation voltage.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
        Rets:
            (1) Excitation voltage in pu.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_get_generator_excitation_voltage_in_pu(ibus, ickt, self.toolkit_index)

    def get_generator_mechanical_power_in_pu(self, generator):
        """
        Get generator mechanical power.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
        Rets:
            (1) Mechanical power in pu based on generator MBASE.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_get_generator_mechanical_power_in_pu_based_on_mbase(ibus, ickt, self.toolkit_index)

    def get_generator_mechanical_power_in_MW(self, generator):
        """
        Get generator mechanical power.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
        Rets:
            (1) Mechanical power in MW.
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_get_generator_mechanical_power_in_MW(ibus, ickt, self.toolkit_index)

    def set_generator_excitation_voltage_in_pu(self, generator, value):
        """
        Set generator excitation voltage. If exciter model exists for the generator, nothing will be changed.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) value: New excitation voltage in pu.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_set_generator_excitation_voltage_in_pu(ibus, ickt, value, self.toolkit_index)

    def set_generator_mechanical_power_in_pu(self, generator, value):
        """
        Set generator mechanical power. If turbine governor model exists for the generator, nothing will be changed.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) value: New mechanical power in pu based on generator MBASE.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_set_generator_mechanical_power_in_pu_based_on_mbase(ibus, ickt, value, self.toolkit_index)
        
    def set_generator_mechanical_power_in_MW(self, generator, value):
        """
        Set generator mechanical power. If turbine governor model exists for the generator, nothing will be changed.
        Args:
            (1) generator: Generator device id in format of (bus, ickt).
            (2) value: New mechanical power in MW.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, ickt = self.__extract_single_bus_device_id(generator)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_set_generator_mechanical_power_in_MW(ibus, ickt, value, self.toolkit_index)

    def get_hvdc_power_order_in_MW(self, hvdc):
        """
        Get HVDC link power order.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
        Rets:
            (1) Power order in MW.
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_get_hvdc_power_order_in_MW(ibus, jbus, ickt, self.toolkit_index)
        
    def set_hvdc_power_order_in_MW(self, hvdc, value):
        """
        Set HVDC link power order.
        Args:
            (1) hvdc: HVDC link device id in format of (ibus, jbus, ickt).
            (2) value: New power order in MW.
        Rets: N/A
        """
        global STEPS_LIB
        ibus, jbus, ickt = self.__extract_double_bus_device_id(hvdc)
        ickt = self.__get_c_char_p_of_string(ickt)
        return STEPS_LIB.api_set_hvdc_power_order_in_MW(ibus, jbus, ickt, value, self.toolkit_index)
        