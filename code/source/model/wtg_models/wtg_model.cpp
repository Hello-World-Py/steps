#include "header/model/wtg_models/wtg_model.h"
#include "header/basic/utility.h"
#include "header/power_system_database.h"
WTG_MODEL::WTG_MODEL()
{
    set_allowed_device_type_CAN_ONLY_BE_CALLED_BY_SPECIFIC_MODEL_CONSTRUCTOR("WT GENERATOR");
}

WTG_MODEL::~WTG_MODEL()
{
    ;
}

WT_GENERATOR* WTG_MODEL::get_wt_generator_pointer() const
{
    return (WT_GENERATOR*) get_device_pointer();
}

double WTG_MODEL::get_mbase_in_MVA() const
{
    WT_GENERATOR* gen = get_wt_generator_pointer();
    if(gen!=NULL)
        return gen->get_mbase_in_MVA();
    else
        return 0.0;
}

complex<double> WTG_MODEL::get_terminal_complex_voltage_in_pu() const
{
    WT_GENERATOR* gen = get_wt_generator_pointer();
    if(gen==NULL)
        return 0.0;

    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();

    size_t bus = gen->get_generator_bus();
    complex<double> Vxy = psdb.get_bus_complex_voltage_in_pu(bus);
    return Vxy;
}

size_t WTG_MODEL::get_number_of_lumped_wt_generators() const
{
    WT_GENERATOR* gen = get_wt_generator_pointer();
    if(gen==NULL)
        return 0;
    return gen->get_number_of_lumped_wt_generators();
}

double WTG_MODEL::get_rated_power_per_wt_generator_in_MW() const
{
    WT_GENERATOR* gen = get_wt_generator_pointer();
    if(gen==NULL)
        return 0.0;
    return gen->get_rated_power_per_wt_generator_in_MW();
}

double WTG_MODEL::get_bus_base_frequency_in_Hz() const
{
    WT_GENERATOR* gen = get_wt_generator_pointer();
    if(gen==NULL)
        return 0.0;

    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();

    return psdb.get_bus_base_frequency_in_Hz(gen->get_generator_bus());
}

complex<double> WTG_MODEL::get_source_impedance_in_pu_based_on_mbase() const
{
    WT_GENERATOR* wt_generator = get_wt_generator_pointer();
    if(wt_generator==NULL)
        return 0.0;
    else
        return wt_generator->get_source_impedance_in_pu();
}
