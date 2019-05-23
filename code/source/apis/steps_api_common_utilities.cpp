#include "header/apis/steps_api.h"
#include "header/basic/utility.h"
#include "header/steps_namespace.h"

void api_set_default_toolkit_log_file(char* log_fie)
{
    string log_file_name = "";
    if(log_fie!=NULL)
        log_file_name = log_fie;
    default_toolkit.open_log_file(log_file_name);
}

size_t api_generate_new_toolkit(char* log_fie)
{
    string log_file_name = "";
    if(log_fie!=NULL)
        log_file_name = log_fie;
    size_t index = generate_new_toolkit(log_file_name);
    return index;
}

void api_delete_toolkit(size_t toolkit_index)
{
    delete_toolkit(toolkit_index);
}


void api_initialize_toolkit(size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    toolkit.clear();
}

void api_clear_toolkit(size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    toolkit.get_power_system_database().clear();
    toolkit.get_dynamic_simulator().clear();
}
double api_get_toolkit_float_data(char* parameter_name, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();

    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="SBASE")
        return psdb.get_system_base_power_in_MVA();

    show_parameter_not_supported_with_api(PARAMETER_NAME, __FUNCTION__);
    return 0.0;
}

void api_set_toolkit_float_data(char* parameter_name, double value, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();

    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="SBASE")
        return psdb.set_system_base_power_in_MVA(value);

    show_parameter_not_supported_with_api(PARAMETER_NAME, __FUNCTION__);
}


const char* api_get_toolkit_string_data(char* parameter_name, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    snprintf(toolkit.steps_char_buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "%s","");
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();

    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="TOOLKIT NAME")
    {
        snprintf(toolkit.steps_char_buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "%s", (toolkit.get_toolkit_name()).c_str());
        return toolkit.steps_char_buffer;
    }
    if(PARAMETER_NAME=="CASE INFORMATION")
    {
        snprintf(toolkit.steps_char_buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "%s", (psdb.get_case_information()).c_str());
        return toolkit.steps_char_buffer;
    }
    if(PARAMETER_NAME=="CASE ADDITIONAL INFORMATION")
    {
        snprintf(toolkit.steps_char_buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "%s", (psdb.get_case_additional_information()).c_str());
        return toolkit.steps_char_buffer;
    }

    show_parameter_not_supported_with_api(PARAMETER_NAME, __FUNCTION__);
    return toolkit.steps_char_buffer;
}

void api_set_toolkit_string_data(char* parameter_name, char* value, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();

    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="TOOLKIT NAME")
        return toolkit.set_toolkit_name(value);
    if(PARAMETER_NAME=="CASE INFORMATION")
        return psdb.set_case_information(value);
    if(PARAMETER_NAME=="CASE ADDITIONAL INFORMATION")
        return psdb.set_case_additional_information(value);

    show_parameter_not_supported_with_api(PARAMETER_NAME, __FUNCTION__);
    return;
}

bool api_get_toolkit_bool_data(char* parameter_name, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    snprintf(toolkit.steps_char_buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "%s","");
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();

    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="DETAILED LOG LOGIC")
    {
        return toolkit.is_detailed_log_enabled();
    }

    show_parameter_not_supported_with_api(PARAMETER_NAME, __FUNCTION__);
    return toolkit.steps_char_buffer;
}

void api_set_toolkit_bool_data(char* parameter_name, bool value, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();

    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="DETAILED LOG LOGIC")
    {
        if(value==true)
            return toolkit.enable_detailed_log();
        else
            return toolkit.disable_detailed_log();
    }

    show_parameter_not_supported_with_api(PARAMETER_NAME, __FUNCTION__);
    return;
}

void show_side_not_supported_for_device_with_api(string side, DEVICE_ID did, string api_func, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Side '%s' is not supported for %s with api %s.\n"
             "Nothing will be chaged.\n"
             "If return value is expected, 0/0.0/False/EMPTY STRING will be returned",
             side.c_str(), (did.get_device_name()).c_str(), api_func.c_str());
    toolkit.show_information_with_leading_time_stamp(buffer);
}

void show_parameter_not_supported_for_device_with_api(string par_name, DEVICE_ID did, string api_func, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Parameter '%s' is not supported for %s with api %s.\n"
             "Nothing will be chaged.\n"
             "If return value is expected, 0/0.0/False/EMPTY STRING will be returned",
             par_name.c_str(), (did.get_device_name()).c_str(), api_func.c_str());
    toolkit.show_information_with_leading_time_stamp(buffer);
}

void show_parameter_not_supported_with_api(string par_name, string api_func, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Parameter '%s' is not supported with api %s.\n"
             "Nothing will be chaged.\n"
             "If return value is expected, 0/0.0/False/EMPTY STRING will be returned",
             par_name.c_str(), api_func.c_str());
    toolkit.show_information_with_leading_time_stamp(buffer);
}

void show_device_not_exist_with_api(DEVICE_ID did, string api_func, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Device %s does not exist in database with api %s.\n"
             "Nothing will be chaged.\n"
             "If return value is expected, 0/0.0/False/EMPTY STRING will be returned",
             (did.get_device_name()).c_str(), api_func.c_str());
    toolkit.show_information_with_leading_time_stamp(buffer);
}


void show_parameter_not_supported_for_area_zone_owner_with_api(string par_name, size_t no, string api_func, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Parameter '%s' is not supported for Area/Zone/Owner %lu with api %s.\n"
             "Nothing will be chaged.\n"
             "If return value is expected, 0/0.0/False/EMPTY STRING will be returned",
             par_name.c_str(), no, api_func.c_str());
    toolkit.show_information_with_leading_time_stamp(buffer);
}

void show_area_zone_owner_not_exist_with_api(size_t no, string api_func, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Area/Zone/Owner %lu does not exist in database with api %s.\n"
             "Nothing will be chaged.\n"
             "If return value is expected, 0/0.0/False/EMPTY STRING will be returned",
             no, api_func.c_str());
    toolkit.show_information_with_leading_time_stamp(buffer);
}

size_t get_owner_of_device(DEVICE* device, string parameter_name, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="OWNER1")
    {
        return device->get_owner_of_index(0);
    }

    if(PARAMETER_NAME=="OWNER2")
    {
        return device->get_owner_of_index(1);
    }

    if(PARAMETER_NAME=="OWNER3")
    {
        return device->get_owner_of_index(2);
    }

    if(PARAMETER_NAME=="OWNER4")
    {
        return device->get_owner_of_index(3);
    }
    show_parameter_not_supported_for_device_with_api(PARAMETER_NAME, device->get_device_id(), __FUNCTION__);
    return 0;
}

void set_owner_of_device(DEVICE* device, string parameter_name, int value, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    string PARAMETER_NAME = string2upper(parameter_name);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    if(PARAMETER_NAME=="OWNER1")
    {
        size_t n = device->get_owner_count();
        if(n>=1)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 1 already set and will not be set again for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os;
        os.append_owner_and_its_fraction(value, 0.0);
        device->set_ownership(os);
        return;
    }

    if(PARAMETER_NAME=="OWNER2")
    {
        size_t n = device->get_owner_count();
        if(n>=2)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 2 already set and will not be set again for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os = device->get_ownership();
        os.append_owner_and_its_fraction(value, 0.0);
        device->set_ownership(os);
        return;
    }

    if(PARAMETER_NAME=="OWNER3")
    {
        size_t n = device->get_owner_count();
        if(n>=3)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 3 already set and will not be set again for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os = device->get_ownership();
        os.append_owner_and_its_fraction(value, 0.0);
        device->set_ownership(os);
        return;
    }

    if(PARAMETER_NAME=="OWNER4")
    {
        size_t n = device->get_owner_count();
        if(n>=4)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 4 already set and will not be set again for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os = device->get_ownership();
        os.append_owner_and_its_fraction(value, 0.0);
        device->set_ownership(os);
        return;
    }
    show_parameter_not_supported_for_device_with_api(PARAMETER_NAME, device->get_device_id(), __FUNCTION__);
    return;
}

double get_owner_fraction_of_device(DEVICE* device, string parameter_name, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    string PARAMETER_NAME = string2upper(parameter_name);
    if(PARAMETER_NAME=="FRAC1")
    {
        return device->get_fraction_of_owner_of_index(0);
    }

    if(PARAMETER_NAME=="FRAC2")
    {
        return device->get_fraction_of_owner_of_index(1);
    }

    if(PARAMETER_NAME=="FRAC3")
    {
        return device->get_fraction_of_owner_of_index(2);
    }

    if(PARAMETER_NAME=="FRAC4")
    {
        return device->get_fraction_of_owner_of_index(3);
    }
    show_parameter_not_supported_for_device_with_api(PARAMETER_NAME, device->get_device_id(), __FUNCTION__);
    return 0;
}

void set_owner_fraction_of_device(DEVICE* device, string parameter_name, double value, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    string PARAMETER_NAME = string2upper(parameter_name);
    char buffer[MAX_TEMP_CHAR_BUFFER_SIZE];
    if(PARAMETER_NAME=="FRAC1")
    {
        size_t n = device->get_owner_count();
        if(n<1)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 1 does not exist and owner fraction will not be set for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os = device->get_ownership();
        size_t owner = device->get_owner_of_index(0);
        double frac = device->get_fraction_of_owner_of_index(0);
        os.append_owner_and_its_fraction(owner, -frac+value);
        device->set_ownership(os);
        return;
    }

    if(PARAMETER_NAME=="FRAC2")
    {
        size_t n = device->get_owner_count();
        if(n<2)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 2 does not exist and owner fraction will not be set for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os = device->get_ownership();
        size_t owner = device->get_owner_of_index(1);
        double frac = device->get_fraction_of_owner_of_index(1);
        os.append_owner_and_its_fraction(owner, -frac+value);
        device->set_ownership(os);
        return;
    }

    if(PARAMETER_NAME=="FRAC3")
    {
        size_t n = device->get_owner_count();
        if(n<3)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 3 does not exist and owner fraction will not be set for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os = device->get_ownership();
        size_t owner = device->get_owner_of_index(2);
        double frac = device->get_fraction_of_owner_of_index(2);
        os.append_owner_and_its_fraction(owner, -frac+value);
        device->set_ownership(os);
        return;
    }

    if(PARAMETER_NAME=="FRAC4")
    {
        size_t n = device->get_owner_count();
        if(n<4)
        {
            snprintf(buffer, MAX_TEMP_CHAR_BUFFER_SIZE, "Owner 4 does not exist and owner fraction will not be set for %s.",
                     (device->get_device_name()).c_str());
            toolkit.show_information_with_leading_time_stamp(buffer);
            return;
        }
        OWNERSHIP os = device->get_ownership();
        size_t owner = device->get_owner_of_index(3);
        double frac = device->get_fraction_of_owner_of_index(3);
        os.append_owner_and_its_fraction(owner, -frac+value);
        device->set_ownership(os);
        return;
    }
    show_parameter_not_supported_for_device_with_api(PARAMETER_NAME, device->get_device_id(), __FUNCTION__);
}

size_t api_get_allowed_maximum_bus_number(size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    return psdb.get_allowed_max_bus_number();
}

void api_set_allowed_maximum_bus_number(size_t max_bus, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    psdb.set_allowed_max_bus_number(max_bus);
}


size_t api_get_device_capacity(const char* device_type, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    string DEVICE_TYPE = string2upper(device_type);

    if(DEVICE_TYPE=="BUS")
        return psdb.get_bus_capacity();
    if(DEVICE_TYPE=="GENERATOR")
        return psdb.get_generator_capacity();
    if(DEVICE_TYPE=="WT GENERATOR")
        return psdb.get_wt_generator_capacity();
    if(DEVICE_TYPE=="PV UNIT")
        return psdb.get_pv_unit_capacity();
    if(DEVICE_TYPE=="LOAD")
        return psdb.get_load_capacity();
    if(DEVICE_TYPE=="FIXED SHUNT")
        return psdb.get_fixed_shunt_capacity();
    if(DEVICE_TYPE=="LINE")
        return psdb.get_line_capacity();
    if(DEVICE_TYPE=="TRANSFORMER")
        return psdb.get_transformer_capacity();
    if(DEVICE_TYPE=="HVDC")
        return psdb.get_hvdc_capacity();
    if(DEVICE_TYPE=="EQUIVALENT DEVICE")
        return psdb.get_equivalent_device_capacity();
    if(DEVICE_TYPE=="ENERGY STORAGE")
        return psdb.get_energy_storage_capacity();

    show_parameter_not_supported_with_api(DEVICE_TYPE, __FUNCTION__);
    return 0;
}


size_t api_get_area_capacity(size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    return psdb.get_area_capacity();
}

size_t api_get_zone_capacity(size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    return psdb.get_zone_capacity();
}

size_t api_get_owner_capacity(size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    return psdb.get_owner_capacity();
}


void api_set_device_capacity(const char* device_type, size_t cap, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    string DEVICE_TYPE = string2upper(device_type);

    if(DEVICE_TYPE=="BUS")
        return psdb.set_bus_capacity(cap);
    if(DEVICE_TYPE=="GENERATOR")
        return psdb.set_generator_capacity(cap);
    if(DEVICE_TYPE=="WT GENERATOR")
        return psdb.set_wt_generator_capacity(cap);
    if(DEVICE_TYPE=="PV UNIT")
        return psdb.set_pv_unit_capacity(cap);
    if(DEVICE_TYPE=="LOAD")
        return psdb.set_load_capacity(cap);
    if(DEVICE_TYPE=="FIXED SHUNT")
        return psdb.set_fixed_shunt_capacity(cap);
    if(DEVICE_TYPE=="LINE")
        return psdb.set_line_capacity(cap);
    if(DEVICE_TYPE=="TRANSFORMER")
        return psdb.set_transformer_capacity(cap);
    if(DEVICE_TYPE=="HVDC")
        return psdb.set_hvdc_capacity(cap);
    if(DEVICE_TYPE=="EQUIVALENT DEVICE")
        return psdb.set_equivalent_device_capacity(cap);
    if(DEVICE_TYPE=="ENERGY STORAGE")
        return psdb.set_energy_storage_capacity(cap);

    show_parameter_not_supported_with_api(DEVICE_TYPE, __FUNCTION__);
}

void api_set_area_capacity(size_t cap, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    return psdb.set_area_capacity(cap);
}

void api_set_zone_capacity(size_t cap, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    return psdb.set_zone_capacity(cap);
}

void api_set_owner_capacity(size_t cap, size_t toolkit_index)
{
    STEPS& toolkit = get_toolkit(toolkit_index);
    POWER_SYSTEM_DATABASE& psdb = toolkit.get_power_system_database();
    return psdb.set_owner_capacity(cap);
}


