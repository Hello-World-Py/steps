#ifndef WT_AERODYNAMIC_MODEL_TEST_H
#define WT_AERODYNAMIC_MODEL_TEST_H

#include <istream>
#include <cstdlib>
#include <cstring>
#include <iostream>

#ifdef _MSC_VER
	#pragma warning (disable: 4290)
#endif

#include "header/model/wtg_models/wtg_model_test.h"
#include "header/power_system_database.h"
#include "header/STEPS.h"

using namespace std;

class WT_AERODYNAMIC_MODEL_TEST : public WTG_MODEL_TEST
{
    public:
        WT_AERODYNAMIC_MODEL_TEST();
    protected:
        virtual void setup();
        virtual void tear_down();
    protected:
        void test_get_model_type();

        void test_get_damping_in_pu();

        void test_set_get_number_of_pole_pairs();
        void test_set_get_generator_to_turbine_gear_ratio();
        void test_set_get_gear_efficiency();
        void test_set_get_turbine_blade_radius();
        void test_set_get_nominal_wind_speed();
        void test_set_get_nominal_air_density();

        void test_get_nominal_turbine_speed();

        void test_set_get_initial_wind_speed();
        void test_set_get_initial_pitch_angle();
        void test_set_get_initial_turbine_speed();

        void test_set_get_air_density();
        void test_set_get_turbine_speed_mode();
        void test_set_get_max_steady_state_turbine_speed();
        void test_set_get_min_steady_state_turbine_speed();

        void test_get_wind_speed();
        void test_get_pitch_angle();
        void test_get_turbine_frequency();
        void test_get_turbine_speed();

        void test_get_standard_psse_string();


        void test_initialize_and_get_initialized_inputs_with_underspeed_mode();
        void test_initialize_and_get_initialized_inputs_with_mppt_mode();
        void test_initialize_and_get_initialized_inputs_with_overspeed_mode();
        void test_list_Cp_and_mechanical_power_data_of_different_wind_speed();

        void test_get_turbine_speed_reference();
        void test_set_as_typical_wt_generator();

        virtual void test_get_model_name() = 0;
        virtual void test_set_get_parameters() = 0;
};

#endif//WT_AERODYNAMIC_MODEL_TEST_H
