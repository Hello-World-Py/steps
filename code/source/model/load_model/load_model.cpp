#include "header/model/load_model/load_model.h"
#include "header/power_system_database.h"
#include "header/basic/utility.h"
#include "header/STEPS.h"
#include <cstdio>

LOAD_MODEL::LOAD_MODEL()
{
    set_allowed_device_type_CAN_ONLY_BE_CALLED_BY_SPECIFIC_MODEL_CONSTRUCTOR("LOAD");
}

LOAD_MODEL::~LOAD_MODEL()
{
    ;
}

LOAD* LOAD_MODEL::get_load_pointer() const
{
    return (LOAD*) get_device_pointer();
}


void LOAD_MODEL::set_voltage_source_flag(bool flag)
{
    voltage_source_flag = flag;
}

bool LOAD_MODEL::get_voltage_source_flag() const
{
    return voltage_source_flag;
}

bool LOAD_MODEL::is_voltage_source() const
{
    return voltage_source_flag==true;
}

string LOAD_MODEL::get_model_type() const
{
    return "LOAD CHARACTERISTICS";
}


void LOAD_MODEL::synchronize_bus_voltage_and_frequency()
{
    LOAD* load = get_load_pointer();
    if(load!=NULL)
    {
        BUS* bus = load->get_bus_pointer();
        if(bus!=NULL)
        {
            voltage_pu = bus->get_positive_sequence_voltage_in_pu();
            complex_voltage_pu = bus->get_positive_sequence_complex_voltage_in_pu();
            frequency_deviation_pu = bus->get_frequency_deviation_in_pu();
        }
    }
}

double LOAD_MODEL::get_bus_positive_sequence_voltage_in_pu() const
{
    return voltage_pu;

    LOAD* load = get_load_pointer();
    if(load!=NULL)
    {
        BUS* bus = load->get_bus_pointer();
        if(bus!=NULL)
            return bus->get_positive_sequence_voltage_in_pu();
        else
            return 0.0;
    }
    else
        return 0.0;
}

double LOAD_MODEL::get_bus_positive_sequence_voltage_in_kV() const
{
    LOAD* load = get_load_pointer();
    if(load!=NULL)
    {
        BUS* bus = load->get_bus_pointer();
        if(bus!=NULL)
            return bus->get_positive_sequence_voltage_in_kV();
        else
            return 0.0;
    }
    else
        return 0.0;
}

complex<double> LOAD_MODEL::get_bus_positive_sequence_complex_voltage_in_pu() const
{
    return complex_voltage_pu;

    LOAD* load = get_load_pointer();
    if(load!=NULL)
    {
        BUS* bus = load->get_bus_pointer();
        if(bus!=NULL)
            return bus->get_positive_sequence_complex_voltage_in_pu();
        else
            return 0.0;
    }
    else
        return 0.0;
}

double LOAD_MODEL::get_bus_frequency_deviation_in_pu() const
{
    return frequency_deviation_pu;

    LOAD* load = get_load_pointer();
    if(load!=NULL)
    {
        BUS* bus = load->get_bus_pointer();
        if(bus!=NULL)
            return bus->get_frequency_deviation_in_pu();
        else
            return 0.0;
    }
    else
        return 0.0;
}

double LOAD_MODEL::get_bus_base_frequency_in_Hz() const
{
    LOAD* load = get_load_pointer();
    if(load!=NULL)
    {
        BUS* bus = load->get_bus_pointer();
        if(bus!=NULL)
            return bus->get_base_frequency_in_Hz();
        else
            return 0.0;
    }
    else
        return 0.0;
}

void LOAD_MODEL::set_subsystem_type(SUBSYSTEM_TYPE subtype)
{
    subsystem_type = subtype;
}

SUBSYSTEM_TYPE LOAD_MODEL::get_subsystem_type() const
{
    return subsystem_type;
}

string LOAD_MODEL::get_detailed_model_name() const
{
    string model_name = get_model_name();
    switch(get_subsystem_type())
    {
        case BUS_SUBSYSTEM_TYPE:
        {
            model_name += "BL";
            break;
        }
        case AREA_SUBSYSTEM_TYPE:
        {
            model_name += "AR";
            break;
        }
        case ZONE_SUBSYSTEM_TYPE:
        {
            model_name += "ZN";
            break;
        }
        case OWNER_SUBSYSTEM_TYPE:
        {
            model_name += "OW";
            break;
        }
        default:
        {
            model_name += "AL";
            break;
        }
    }
    return model_name;
}
