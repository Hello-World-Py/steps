#include "header/apis/steps_api.h"
#include "header/basic/utility.h"
#include "header/steps_namespace.h"
#include "header/data_imexporter/psse_imexporter.h"
#include "header/data_imexporter/bpa_imexporter.h"

size_t api_get_device_count(const char* device_type)
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    string DEVICE_TYPE = string2upper(device_type);

    if(DEVICE_TYPE=="BUS")
        return psdb.get_bus_count();
    if(DEVICE_TYPE=="GENERATOR")
        return psdb.get_generator_count();
    if(DEVICE_TYPE=="WT GENERATOR")
        return psdb.get_wt_generator_count();
    if(DEVICE_TYPE=="PV UNIT")
        return psdb.get_pv_unit_count();
    if(DEVICE_TYPE=="LOAD")
        return psdb.get_load_count();
    if(DEVICE_TYPE=="FIXED SHUNT")
        return psdb.get_fixed_shunt_count();
    if(DEVICE_TYPE=="LINE")
        return psdb.get_line_count();
    if(DEVICE_TYPE=="TRANSFORMER")
        return psdb.get_transformer_count();
    if(DEVICE_TYPE=="HVDC")
        return psdb.get_hvdc_count();
    if(DEVICE_TYPE=="EQUIVALENT DEVICE")
        return psdb.get_equivalent_device_count();
    if(DEVICE_TYPE=="ENERGY STORAGE")
        return psdb.get_energy_storage_count();

    show_parameter_not_supported_with_api(DEVICE_TYPE, __FUNCTION__);
    return 0;
}

size_t api_get_area_count()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    return psdb.get_area_count();
}

size_t api_get_zone_count()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    return psdb.get_zone_count();
}

size_t api_get_owner_count()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    return psdb.get_owner_count();
}

size_t api_get_in_service_bus_count()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    return psdb.get_in_service_bus_count();
}


void api_update_overshadowed_buses()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    psdb.update_overshadowed_bus_count();
}

void api_set_all_buses_un_overshadowed()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    psdb.set_all_buses_un_overshadowed();
}

size_t api_get_overshadowed_bus_count()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    psdb.update_overshadowed_bus_count();
    return psdb.get_overshadowed_bus_count();
}

