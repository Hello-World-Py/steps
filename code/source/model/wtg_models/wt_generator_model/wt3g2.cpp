#include "header/model/wtg_models/wt_generator_model/wt3g2.h"
#include "header/basic/utility.h"
#include "header/steps_namespace.h"
#include <cstdio>
#include <istream>
#include <iostream>
using namespace std;

WT3G2::WT3G2()
{
    clear();
}

WT3G2::~WT3G2()
{
    clear();
}

void WT3G2::clear()
{
    prepare_model_variable_table();

    set_current_source_flag(true);

    active_current_commander.set_limiter_type(NO_LIMITER);

    reactive_voltage_commander.set_limiter_type(NO_LIMITER);
    reactive_voltage_commander.set_K(1.0);

    PLL_frequency_integrator.set_limiter_type(NON_WINDUP_LIMITER);

    PLL_angle_integrator.set_limiter_type(NO_LIMITER);

    LVPL_voltage_sensor.set_limiter_type(NO_LIMITER);
    LVPL_voltage_sensor.set_K(1.0);
}

void WT3G2::copy_from_const_model(const WT3G2& model)
{
    clear();
    set_current_source_flag(model.get_current_source_flag());
    set_converter_activer_current_command_T_in_s(model.get_converter_activer_current_command_T_in_s());
    set_LVPL_max_rate_of_active_current_change(model.get_LVPL_max_rate_of_active_current_change());
    set_LVPL_voltage_sensor_T_in_s(model.get_LVPL_voltage_sensor_T_in_s());
    set_LVPL(model.get_LVPL());

    set_converter_reactiver_voltage_command_T_in_s(model.get_converter_reactiver_voltage_command_T_in_s());
    set_HVRC_voltage_in_pu(model.get_HVRC_voltage_in_pu());
    set_HVRC_current_in_pu(model.get_HVRC_current_in_pu());

    set_KPLL(model.get_KPLL());
    set_KIPLL(model.get_KIPLL());
    set_PLLmax(model.get_PLLmax());
    set_PLLmin(model.get_PLLmin());
}

WT3G2::WT3G2(const WT3G2& model):WT_GENERATOR_MODEL()
{
    copy_from_const_model(model);
}

WT3G2& WT3G2::operator=(const WT3G2& model)
{
    if(this==&model)
        return *this;

    copy_from_const_model(model);

    return (*this);
}

void WT3G2::set_converter_activer_current_command_T_in_s(double t)
{
    active_current_commander.set_T_in_s(t);
}

void WT3G2::set_converter_reactiver_voltage_command_T_in_s(double t)
{
    reactive_voltage_commander.set_T_in_s(t);
}

void WT3G2::set_KPLL(double K)
{
    KPLL = K;
}

void WT3G2::set_KIPLL(double K)
{
    PLL_frequency_integrator.set_T_in_s(1.0/K);
}

void WT3G2::set_PLLmax(double pmax)
{
    PLL_frequency_integrator.set_upper_limit(pmax);
}

void WT3G2::set_PLLmin(double pmin)
{
    PLL_frequency_integrator.set_lower_limit(pmin);
}

void WT3G2::set_LVPL(const LVPL& lvpl)
{
    this->lvpl = lvpl;
}

void WT3G2::set_HVRC_voltage_in_pu(double v)
{
    HVRCR_voltage = v;
}

void WT3G2::set_HVRC_current_in_pu(double i)
{
    HVRCR_current = i;
}

void WT3G2::set_LVPL_max_rate_of_active_current_change(double rate)
{
    LVPL_active_power_change_rate = rate;
}

void WT3G2::set_LVPL_voltage_sensor_T_in_s(double t)
{
    LVPL_voltage_sensor.set_T_in_s(t);
}

double WT3G2::get_converter_activer_current_command_T_in_s() const
{
    return active_current_commander.get_T_in_s();
}

double WT3G2::get_converter_reactiver_voltage_command_T_in_s() const
{
    return reactive_voltage_commander.get_T_in_s();
}

double WT3G2::get_KPLL() const
{
    return KPLL;
}

double WT3G2::get_KIPLL() const
{
    return 1.0/PLL_frequency_integrator.get_T_in_s();
}

double WT3G2::get_PLLmax() const
{
    return PLL_frequency_integrator.get_upper_limit();
}

double WT3G2::get_PLLmin() const
{
    return PLL_frequency_integrator.get_lower_limit();
}

LVPL WT3G2::get_LVPL() const
{
    return lvpl;
}

double WT3G2::get_HVRC_voltage_in_pu() const
{
    return HVRCR_voltage;
}

double WT3G2::get_HVRC_current_in_pu() const
{
    return HVRCR_current;
}

double WT3G2::get_LVPL_max_rate_of_active_current_change() const
{
    return LVPL_active_power_change_rate;
}

double WT3G2::get_LVPL_voltage_sensor_T_in_s() const
{
    return LVPL_voltage_sensor.get_T_in_s();
}


string WT3G2::get_model_name() const
{
    return "WT3G2";
}

double WT3G2::get_model_data_with_index(size_t index) const
{
    ostringstream osstream;
    osstream<<get_model_name()<<"::"<<__FUNCTION__<<"() has not been implemented. Input index is provided: "<<index;
    show_information_with_leading_time_stamp(osstream);
    return 0.0;
}

double WT3G2::get_model_data_with_name(string par_name) const
{
    par_name = string2upper(par_name);
    if(par_name=="")
        return 0.0;

    return 0.0;
}

void WT3G2::set_model_data_with_index(size_t index, double value)
{
    ostringstream osstream;
    osstream<<get_model_name()<<"::"<<__FUNCTION__<<"() has not been implemented. Input (index, value) is provided: ("<<index<<", "<<value<<").";
    show_information_with_leading_time_stamp(osstream);
    return;
}

void WT3G2::set_model_data_with_name(string par_name, double value)
{
    ostringstream osstream;
    osstream<<get_model_name()<<"::"<<__FUNCTION__<<"() has not been implemented. Input (par_name, value) is provided: ("<<par_name<<", "<<value<<").";
    show_information_with_leading_time_stamp(osstream);
    return;
}

bool WT3G2::setup_model_with_steps_string(string data)
{
    ostringstream osstream;
    osstream<<get_model_name()<<"::"<<__FUNCTION__<<"() is not fully supported to set up model with following data:"<<endl
            <<data;
    show_information_with_leading_time_stamp(osstream);
    return false;
}

bool WT3G2::setup_model_with_psse_string(string data)
{
    ostringstream osstream;

    bool is_successful = false;
    vector<string> dyrdata = split_string(data,",");

    if(dyrdata.size()<18)
        return is_successful;

    string model_name = get_string_data(dyrdata[1],"");
    if(model_name!=get_model_name())
        return is_successful;

    size_t ibus;
    string id;
    size_t n_lumped_turbine;
    double t_EQcmd, t_IPcmd, kpll, kipll, pllmax, pllmin, prate, lvpl_v1, lvpl_v2, lvpl_g,
           hvrc_v, hvrc_i, lvpl_rate, t_lvpl;

    ibus = size_t(get_integer_data(dyrdata[0],"0"));
    id = get_string_data(dyrdata[2],"");

    size_t i=3;
    n_lumped_turbine = size_t(get_integer_data(dyrdata[i],"1")); i++;
    prate = get_double_data(dyrdata[i],"0.0"); i++;
    t_IPcmd = get_double_data(dyrdata[i],"0.0"); i++;
    lvpl_rate = get_double_data(dyrdata[i],"0.0"); i++;
    t_lvpl = get_double_data(dyrdata[i],"0.0"); i++;
    lvpl_v1 = get_double_data(dyrdata[i],"0.0"); i++;
    lvpl_v2 = get_double_data(dyrdata[i],"0.0"); i++;
    lvpl_g = get_double_data(dyrdata[i],"0.0"); i++;
    t_EQcmd = get_double_data(dyrdata[i],"0.0"); i++;
    hvrc_v = get_double_data(dyrdata[i],"0.0"); i++;
    hvrc_i = get_double_data(dyrdata[i],"0.0"); i++;
    kpll = get_double_data(dyrdata[i],"0.0"); i++;
    kipll = get_double_data(dyrdata[i],"0.0"); i++;
    pllmax = get_double_data(dyrdata[i],"0.0"); i++;
    pllmin = get_double_data(dyrdata[i],"0.0");

    DEVICE_ID did = get_wt_generator_device_id(ibus, id);
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    WT_GENERATOR* gen = psdb.get_wt_generator(did);
    if(gen==NULL)
    {
        osstream<<"Error when loading data to build "<<get_model_name()<<" model for "<<did.get_device_name()<<endl
               <<"No such wt generator exists in the power system database.";
        show_information_with_leading_time_stamp(osstream);
        return is_successful;
    }

    gen->set_number_of_lumped_wt_generators(n_lumped_turbine);
    gen->set_rated_power_per_wt_generator_in_MW(prate);

    set_converter_activer_current_command_T_in_s(t_IPcmd);
    set_LVPL_max_rate_of_active_current_change(lvpl_rate);
    set_LVPL_voltage_sensor_T_in_s(t_lvpl);
    LVPL lvpl;
    lvpl.set_low_voltage_in_pu(lvpl_v1);
    lvpl.set_high_voltage_in_pu(lvpl_v2);
    lvpl.set_gain_at_high_voltage(lvpl_g);
    set_LVPL(lvpl);

    set_converter_reactiver_voltage_command_T_in_s(t_EQcmd);
    set_HVRC_voltage_in_pu(hvrc_v);
    set_HVRC_current_in_pu(hvrc_i);
    set_KPLL(kpll);
    set_KIPLL(kipll);
    set_PLLmax(pllmax);
    set_PLLmin(pllmin);

    is_successful = true;

    return is_successful;
}

bool WT3G2::setup_model_with_bpa_string(string data)
{
    ostringstream osstream;
    osstream<<get_model_name()<<"::"<<__FUNCTION__<<"() is not fully supported to set up model with following data:"<<endl
            <<data;
    show_information_with_leading_time_stamp(osstream);
    return false;
}

void WT3G2::initialize()
{
    ostringstream oosstream;
    if(is_model_initialized())
        return;

    WT_GENERATOR* wt_generator = get_wt_generator_pointer();
    if(wt_generator==NULL)
        return;

    size_t n_lumped = get_number_of_lumped_wt_generators();
    double fbase = get_bus_base_frequency_in_Hz();
    double wbase = 2.0*PI*fbase;

    double kipll = get_KIPLL();
    if(kipll!=0.0)
    {
        PLL_frequency_integrator.set_T_in_s(1.0/kipll);
        double pllmax = get_PLLmax();
        PLL_frequency_integrator.set_upper_limit(pllmax);
        PLL_frequency_integrator.set_lower_limit(-pllmax);
    }

    PLL_angle_integrator.set_T_in_s(1.0/wbase);

    double mbase = get_mbase_in_MVA();
    mbase /= n_lumped;

    complex<double> Zsource = get_source_impedance_in_pu_based_on_mbase();
    double xeq = Zsource.imag();

    double P = wt_generator->get_p_generation_in_MW()/n_lumped;
    double Q = wt_generator->get_q_generation_in_MVar()/n_lumped;
    complex<double> S(P/mbase,Q/mbase);


    complex<double> Vxy = get_terminal_complex_voltage_in_pu();
    double V = steps_fast_complex_abs(Vxy);
    double angle_in_rad = atan2(Vxy.imag(), Vxy.real());
    // ignore voltage angle
    complex<double> Ixy = conj(S/Vxy);
    complex<double> Isource = Ixy + Vxy/Zsource;

    double Ix = Isource.real();
    double Iy = Isource.imag();

    double IP = Ix*cos(angle_in_rad) + Iy*sin(angle_in_rad);
    double IQ =-Ix*sin(angle_in_rad) + Iy*cos(angle_in_rad);
    //complex<double> IPQ = xy2dq_with_angle_in_rad(Isource, angle_in_rad);
    //double IP = IPQ.real();
    //double IQ = IPQ.imag();

    double EQ = IQ*(-xeq);

    active_current_commander.set_output(IP);
    active_current_commander.initialize();

    reactive_voltage_commander.set_output(EQ);
    reactive_voltage_commander.initialize();

    if(kipll!=0.0)
    {
        PLL_frequency_integrator.set_output(0.0);
        PLL_frequency_integrator.initialize();
    }

    PLL_angle_integrator.set_output(angle_in_rad);
    PLL_angle_integrator.initialize();

    LVPL_voltage_sensor.set_output(V);
    LVPL_voltage_sensor.initialize();

    set_initial_active_current_command_in_pu_based_on_mbase(IP);
    set_initial_reactive_current_command_in_pu_based_on_mbase(IQ);

    set_flag_model_initialized_as_true();

    oosstream<<get_model_name()<<" model of "<<get_device_name()<<" is initialized."<<endl
            <<"(1) Initial active current command = "<<get_initial_active_current_command_in_pu_based_on_mbase()<<endl
            <<"(2) Initial reactive current command = "<<get_initial_reactive_current_command_in_pu_based_on_mbase()<<endl
            <<"(3) States of blocks"<<endl
            <<"    active_current_commander block state: "<<active_current_commander.get_state()<<endl
            <<"    reactive_voltage_commander block state: "<<reactive_voltage_commander.get_state()<<endl
            <<"    PLL_frequency_integrator block state: "<<PLL_frequency_integrator.get_state()<<endl
            <<"    PLL_angle_integrator block state: "<<PLL_angle_integrator.get_state()<<endl
            <<"    LVPL_voltage_sensor block state: "<<LVPL_voltage_sensor.get_state()<<endl
            <<"(4) active power generation :"<<get_terminal_active_power_in_MW()<<"MW"<<endl
            <<"(5) reactive power generation :"<<get_terminal_reactive_power_in_MVar()<<"MVar"<<endl
            <<"(6) terminal current :"<<get_terminal_current_in_pu_based_on_mbase()<<"pu";
    show_information_with_leading_time_stamp(oosstream);
}

void WT3G2::run(DYNAMIC_MODE mode)
{
    WT_GENERATOR* wt_generator = get_wt_generator_pointer();
    if(wt_generator==NULL)
        return;

    double fbase = get_bus_base_frequency_in_Hz();
    double wbase = 2.0*PI*fbase;
    complex<double> Zsource = get_source_impedance_in_pu_based_on_mbase();
    double Xeq = Zsource.imag();

    //complex<double> Zsource = get_source_impedance_in_pu_based_on_mbase();

    complex<double> Vxy = get_terminal_complex_voltage_in_pu();
    double V = steps_fast_complex_abs(Vxy);
    double angle_in_rad = atan2(Vxy.imag(), Vxy.real());
    double angle_in_deg = rad2deg(angle_in_rad);

    LVPL_voltage_sensor.set_input(V);
    LVPL_voltage_sensor.run(mode);

    double lvpl_order = lvpl.get_LVPL_order(LVPL_voltage_sensor.get_output());

    double IP = get_active_current_command_in_pu_based_on_mbase();

    double input = active_current_commander.get_output();
    if(input>lvpl_order)
        input = lvpl_order;

    input = IP - input;
    double lvpl_rate_max = get_LVPL_max_rate_of_active_current_change();
    if(input>lvpl_rate_max)
        input = lvpl_rate_max;

    active_current_commander.set_input(input);
    active_current_commander.run(mode);

    double IQ = get_reactive_current_command_in_pu_based_on_mbase();

    double EQ = IQ*(-Xeq);
    reactive_voltage_commander.set_input(EQ);
    reactive_voltage_commander.run(mode);

    double kpll = get_KPLL();
    double kipll = get_KIPLL();
    if(kpll==0.0 and kipll==0.0)
    {
        set_pll_angle_in_deg(angle_in_deg);
    }
    else
    {
        double Vr = Vxy.real();
        double Vi = Vxy.imag();

        double angle = get_pll_angle_in_rad();
        double Vy = -Vr*sin(angle)+Vi*cos(angle);

        input = Vy*kpll/wbase;
        PLL_frequency_integrator.set_input(input);
        PLL_frequency_integrator.run(mode);

        double output = PLL_frequency_integrator.get_output();
        input += output;

        double pllmax = get_PLLmax();
        if(input>pllmax)
            input = pllmax;
        if(input<-pllmax)
            input = -pllmax;

        PLL_angle_integrator.set_input(input);
        PLL_angle_integrator.run(mode);
    }
    IP = get_active_current_command_in_pu_based_on_mbase();

    if(mode==UPDATE_MODE)
        set_flag_model_updated_as_true();
}

complex<double> WT3G2::get_source_Norton_equivalent_complex_current_in_pu_in_xy_axis_based_on_sbase()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    double sbase = psdb.get_system_base_power_in_MVA();
    double mbase = get_mbase_in_MVA();

    complex<double> Vxy = get_terminal_complex_voltage_in_pu();
    double V = steps_fast_complex_abs(Vxy);

    complex<double> Zsource = get_source_impedance_in_pu_based_on_mbase();
    double Xeq = Zsource.imag();

    // low voltage active current logic
    double V_LVACR_high = V;
    double V_LVACR_low = 0.4;
    if(V<=V_LVACR_low)
        V_LVACR_low = V;
    if(V<=0.8)
        V_LVACR_high = 0.8;

    double Ip = active_current_commander.get_output();

    double lvpl_order = lvpl.get_LVPL_order(LVPL_voltage_sensor.get_output());
    if(Ip>lvpl_order)
        Ip =lvpl_order;

    Ip = Ip*(V-V_LVACR_low)/(V_LVACR_high-V_LVACR_low);

    // high voltage reactive current logic
    /*double v_hvrc = get_HVRC_voltage_in_pu();
    double overvoltage_correction_factor = 0.0;
    if(V>=v_hvrc)
        overvoltage_correction_factor=0.7*(V-v_hvrc);


    double Iq = -reactive_voltage_commander.get_output()/Xeq + overvoltage_correction_factor/V;*/
    double Iq = -reactive_voltage_commander.get_output()/Xeq;
    double hvrc_i = get_HVRC_current_in_pu();
    if(Iq<-hvrc_i)
        Iq = -hvrc_i;

    double pll_angle = get_pll_angle_in_rad();

    //complex<double> Ipq(Ip, Iq);
    //complex<double> Ixy = dq2xy_with_angle_in_rad(Ipq, pll_angle);

    double Ix = Ip*cos(pll_angle) - Iq*sin(pll_angle);
    double Iy = Ip*sin(pll_angle) + Iq*cos(pll_angle);

    complex<double> Ixy(Ix, Iy);
    //cout<<"Norton Ixy based on mbase = "<<Ixy<<endl;

    return Ixy*mbase/sbase;
}

complex<double> WT3G2::get_terminal_complex_current_in_pu_in_xy_axis_based_on_mbase()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    double sbase = psdb.get_system_base_power_in_MVA();
    double mbase = get_mbase_in_MVA();
    complex<double> Ixy = get_terminal_complex_current_in_pu_in_xy_axis_based_on_sbase();
    return Ixy*sbase/mbase;
}

complex<double> WT3G2::get_terminal_complex_current_in_pu_in_xy_axis_based_on_sbase()
{
    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    double sbase = psdb.get_system_base_power_in_MVA();
    double mbase = get_mbase_in_MVA();

    complex<double> Zsource = get_source_impedance_in_pu_based_on_mbase();
    Zsource /= mbase;
    Zsource *= sbase;

    complex<double> Ixy_norton = get_source_Norton_equivalent_complex_current_in_pu_in_xy_axis_based_on_sbase();
    complex<double> Vxy = get_terminal_complex_voltage_in_pu();
    complex<double> Ixy_term = Ixy_norton - Vxy/Zsource;
    //cout<<"based on MBASE, Ixy norton = "<<Ixy_norton<<", Ishunt = "<<Vxy/Zsource<<", Iterminal = "<<Ixy_term<<endl;
    return Ixy_term;
}

double WT3G2::get_terminal_current_in_pu_based_on_mbase()
{
    return steps_fast_complex_abs(get_terminal_complex_current_in_pu_in_xy_axis_based_on_mbase());
}

double WT3G2::get_terminal_current_in_pu_based_on_sbase()
{
    return steps_fast_complex_abs(get_terminal_complex_current_in_pu_in_xy_axis_based_on_sbase());
}


void WT3G2::check()
{
    ;
}

void WT3G2::report()
{
    ostringstream osstream;
    osstream<<get_standard_model_string();
    show_information_with_leading_time_stamp(osstream);
}

void WT3G2::save()
{
    ;
}

string WT3G2::get_standard_model_string() const
{
    ostringstream osstream;
    DEVICE_ID did = get_device_id();
    size_t bus = did.get_device_terminal().get_buses()[0];
    string identifier = did.get_device_identifier();

    LVPL lvpl = get_LVPL();

    osstream<<setw(8)<<bus<<", "
      <<"'"<<get_model_name()<<"', "
      <<"'"<<identifier<<"', "
      <<setw(4)<<get_number_of_lumped_wt_generators()<<", "
      <<setw(8)<<setprecision(6)<<get_rated_power_per_wt_generator_in_MW()<<", "
      <<setw(8)<<setprecision(6)<<get_converter_activer_current_command_T_in_s()<<", "
      <<setw(8)<<setprecision(6)<<get_LVPL_max_rate_of_active_current_change()<<", "
      <<setw(8)<<setprecision(6)<<get_LVPL_voltage_sensor_T_in_s()<<", "
      <<setw(8)<<setprecision(6)<<lvpl.get_low_voltage_in_pu()<<", "
      <<setw(8)<<setprecision(6)<<lvpl.get_high_voltage_in_pu()<<", "
      <<setw(8)<<setprecision(6)<<lvpl.get_gain_at_hig_voltage()<<", "
      <<setw(8)<<setprecision(6)<<get_converter_reactiver_voltage_command_T_in_s()<<", "
      <<setw(8)<<setprecision(6)<<get_HVRC_voltage_in_pu()<<", "
      <<setw(8)<<setprecision(6)<<get_HVRC_current_in_pu()<<", "
      <<setw(8)<<setprecision(6)<<get_KPLL()<<", "
      <<setw(8)<<setprecision(6)<<get_KIPLL()<<", "
      <<setw(8)<<setprecision(6)<<get_PLLmax()<<", "
      <<setw(8)<<setprecision(6)<<get_PLLmin()<<" /";

    return osstream.str();
}

void WT3G2::prepare_model_variable_table()
{
    size_t i=0;
    add_model_variable_name_and_index_pair("PLL ANGLE IN DEG", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL P IN PU ON MBASE", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL P IN MW", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL Q IN PU ON MBASE", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL Q IN MVAR", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL S IN PU ON MBASE", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL S IN MVA", i); i++;
    add_model_variable_name_and_index_pair("INTERNAL VOLTAGE IN PU", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL CURRENT IN PU", i); i++;
    add_model_variable_name_and_index_pair("TERMINAL CURRENT IN KA", i); i++;
    add_model_variable_name_and_index_pair("ACTIVE CURRENT COMMAND IN PU", i); i++;
    add_model_variable_name_and_index_pair("REACTIVE CURRENT COMMAND IN PU", i); i++;
    add_model_variable_name_and_index_pair("REACTIVE VOLTAGE COMMAND IN PU", i); i++;
    add_model_variable_name_and_index_pair("STATE@ACTIVE CURRENT COMMAND BLOCK", i); i++;
    add_model_variable_name_and_index_pair("STATE@REACTIVE VOLTAGE COMMAND BLOCK", i); i++;
    add_model_variable_name_and_index_pair("STATE@PLL FREQUENCY BLOCK", i); i++;
    add_model_variable_name_and_index_pair("STATE@PLL ANGLE BLOCK", i); i++;
    add_model_variable_name_and_index_pair("STATE@LVPL VOLTAGE SENSOR", i); i++;
}

double WT3G2::get_variable_with_name(string var_name)
{
    var_name = string2upper(var_name);
    if(var_name == "PLL ANGLE IN DEG")
        return get_pll_angle_in_deg();
    if(var_name == "TERMINAL P IN PU ON MBASE")
        return get_terminal_active_power_in_pu_based_on_mbase();
    if(var_name == "TERMINAL P IN MW")
        return get_terminal_active_power_in_pu_based_on_mbase()*get_mbase_in_MVA();
    if(var_name == "TERMINAL Q IN PU ON MBASE")
        return get_terminal_reactive_power_in_pu_based_on_mbase();
    if(var_name == "TERMINAL Q IN MW")
        return get_terminal_reactive_power_in_pu_based_on_mbase()*get_mbase_in_MVA();
    if(var_name == "TERMINAL S IN PU ON MBASE")
        return steps_fast_complex_abs(get_terminal_complex_power_in_pu_based_on_mbase());
    if(var_name == "TERMINAL S IN MVA")
        return steps_fast_complex_abs(get_terminal_complex_power_in_pu_based_on_mbase())*get_mbase_in_MVA();
    if(var_name == "ACTIVE CURRENT COMMAND IN PU")
        return get_active_current_command_in_pu_based_on_mbase();
    if(var_name == "REACTIVE CURRENT COMMAND IN PU")
        return get_reactive_current_command_in_pu_based_on_mbase();
    if(var_name == "REACTIVE VOLTAGE COMMAND IN PU")
    {
        double Xeq = get_source_impedance_in_pu_based_on_mbase().imag();
        return get_reactive_current_command_in_pu_based_on_mbase()*(-Xeq);
    }
    if(var_name == "INTERNAL VOLTAGE IN PU")
        return steps_fast_complex_abs(get_internal_voltage_in_pu_in_xy_axis());
    if(var_name == "TERMINAL CURRENT IN PU")
        return get_terminal_current_in_pu_based_on_mbase();
    if(var_name == "TERMINAL CURRENT IN KA")
    {
        POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
        WT_GENERATOR* generator = get_wt_generator_pointer();
        size_t bus = generator->get_generator_bus();
        double vbase = psdb.get_bus_base_voltage_in_kV(bus);
        double mbase = generator->get_mbase_in_MVA();
        double ibase = mbase/sqrt(3.0)/vbase;
        return get_terminal_current_in_pu_based_on_mbase()*ibase;
    }
    if(var_name == "STATE@ACTIVE CURRENT COMMAND BLOCK")
        return active_current_commander.get_state();
    if(var_name == "STATE@REACTIVE VOLTAGE COMMAND BLOCK")
        return reactive_voltage_commander.get_state();
    if(var_name == "STATE@PLL FREQUENCY BLOCK")
        return PLL_frequency_integrator.get_state();
    if(var_name == "STATE@PLL ANGLE BLOCK")
        return PLL_angle_integrator.get_state();
    if(var_name == "STATE@LVPL VOLTAGE SENSOR")
        return LVPL_voltage_sensor.get_state();


    return 0.0;
}

complex<double> WT3G2::get_terminal_complex_power_in_pu_based_on_mbase()
{
    complex<double> Vxy = get_terminal_complex_voltage_in_pu();
    complex<double> Ixy = get_terminal_complex_current_in_pu_in_xy_axis_based_on_mbase();
    //cout<<"at time "<<STEPS::TIME<<" terminal Ixy  based on mbase = "<<Ixy<<", Vxy = "<<Vxy<<", S = "<<Vxy*conj(Ixy)*get_mbase_in_MVA()<<endl;

    complex<double> S = Vxy*conj(Ixy);
    return S;
}

complex<double> WT3G2::get_terminal_complex_power_in_MVA()
{
    return get_terminal_complex_power_in_pu_based_on_mbase()*get_mbase_in_MVA();
}

double WT3G2::get_terminal_active_power_in_pu_based_on_mbase()
{
    return get_terminal_complex_power_in_pu_based_on_mbase().real();
}

double WT3G2::get_terminal_active_power_in_MW()
{
    return get_terminal_complex_power_in_MVA().real();
}

double WT3G2::get_terminal_reactive_power_in_pu_based_on_mbase()
{
    return get_terminal_complex_power_in_pu_based_on_mbase().imag();
}

double WT3G2::get_terminal_reactive_power_in_MVar()
{
    return get_terminal_complex_power_in_MVA().imag();
}

double WT3G2::get_active_power_generation_including_stator_loss_in_pu_based_on_mbase()
{
    return get_active_power_generation_including_stator_loss_in_MW()/get_mbase_in_MVA();
}

double WT3G2::get_active_power_generation_including_stator_loss_in_MW()
{
    double pterm = get_terminal_active_power_in_MW();
    double rsource = get_source_impedance_in_pu_based_on_mbase().real();
    double iterm = steps_fast_complex_abs(get_terminal_complex_current_in_pu_in_xy_axis_based_on_mbase());
    double mbase = get_mbase_in_MVA();

    return pterm+rsource*iterm*iterm*mbase;
}

double WT3G2::get_pll_angle_in_rad()
{
    double kpll = get_KPLL();
    double kipll = get_KIPLL();
    if(kpll==0.0 and kipll==0.0)
    {
        complex<double> Vxy = get_terminal_complex_voltage_in_pu();
        double angle = atan2(Vxy.imag(), Vxy.real());
        return angle;
    }
    else
        return PLL_angle_integrator.get_output();
}

double WT3G2::get_pll_angle_in_deg()
{
    return rad2deg(get_pll_angle_in_rad());
}

double WT3G2::get_pll_frequency_deviation_in_pu()
{
    double fbase = get_bus_base_frequency_in_Hz();
    double wbase = 2.0*PI*fbase;

    complex<double> Vxy = get_terminal_complex_voltage_in_pu();

    double kpll = get_KPLL();
    double kipll = get_KIPLL();
    if(kpll==0.0 and kipll==0.0)
        return 0.0;
    else
    {
        double Vr = Vxy.real();
        double Vi = Vxy.imag();

        double angle = get_pll_angle_in_rad();
        double Vy = -Vr*sin(angle)+Vi*cos(angle);

        double input = Vy*kpll/wbase;

        double output = PLL_frequency_integrator.get_output();

        return input+output;
    }
}

double WT3G2::get_pll_frequency_deviation_in_Hz()
{
    double fbase = get_bus_base_frequency_in_Hz();

    return fbase*get_pll_frequency_deviation_in_pu();
}

double WT3G2::get_pll_frequency_in_pu()
{
    return 1.0+get_pll_frequency_deviation_in_pu();
}

double WT3G2::get_pll_frequency_in_Hz()
{
    double fbase = get_bus_base_frequency_in_Hz();

    return fbase*get_pll_frequency_in_pu();
}

complex<double> WT3G2::get_internal_voltage_in_pu_in_xy_axis()
{
    complex<double> Ixy = get_source_Norton_equivalent_complex_current_in_pu_in_xy_axis_based_on_sbase();
    complex<double> Z = get_source_impedance_in_pu_based_on_mbase();

    POWER_SYSTEM_DATABASE& psdb = get_default_power_system_database();
    double sbase = psdb.get_system_base_power_in_MVA();
    double mbase = get_mbase_in_MVA();

    Z = Z/mbase*sbase;

    return Ixy*Z;
}



void WT3G2::set_pll_angle_in_deg(double angle)
{
    PLL_angle_integrator.set_output(deg2rad(angle));
    PLL_angle_integrator.initialize();// the initialize function is used to update STORE
}


string WT3G2::get_dynamic_data_in_psse_format() const
{
    return "";
}

string WT3G2::get_dynamic_data_in_bpa_format() const
{
    return get_dynamic_data_in_psse_format();
}

string WT3G2::get_dynamic_data_in_steps_format() const
{
    return get_dynamic_data_in_psse_format();
}
