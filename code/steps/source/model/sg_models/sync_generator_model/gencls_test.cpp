#include "header/basic/test_macro.h"
#include "header/model/sg_models/sync_generator_model/gencls_test.h"
#include "header/basic/utility.h"
#include "header/steps_namespace.h"
#include <cstdlib>
#include <cstring>
#include <istream>
#include <iostream>
#include <cstdio>
#include <cmath>

#ifdef ENABLE_STEPS_TEST
using namespace std;

GENCLS_TEST::GENCLS_TEST()
{
    TEST_ADD(GENCLS_TEST::test_get_model_name);
    TEST_ADD(GENCLS_TEST::test_update_source_impedance);

    TEST_ADD(GENCLS_TEST::test_initialize_and_get_initialized_inputs);


    TEST_ADD(GENCLS_TEST::test_set_get_rotor_angle);
    TEST_ADD(GENCLS_TEST::test_set_get_rotor_speed);
}

void GENCLS_TEST::setup()
{
    SYNC_GENERATOR_MODEL_TEST::setup();

    GENERATOR* genptr = get_test_generator();

    GENCLS model(default_toolkit);
    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    model.set_device_id(genptr->get_device_id());

    model.set_H_in_s(3.0);
    model.set_D(2.0);
    model.set_Xdp(0.2);

    dmdb.add_model(&model);
}

void GENCLS_TEST::tear_down()
{
    SYNC_GENERATOR_MODEL_TEST::tear_down();

    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    dmdb.remove_the_last_model();

    show_test_end_information();
}


void GENCLS_TEST::test_get_model_name()
{
    show_test_information_for_function_of_class(__FUNCTION__,"GENCLS_TEST");

    SYNC_GENERATOR_MODEL* model = (GENCLS*) get_test_sync_generator_model();

    TEST_ASSERT(model->get_model_name()=="GENCLS");
}

void GENCLS_TEST::test_update_source_impedance()
{
    show_test_information_for_function_of_class(__FUNCTION__,"GENCLS_TEST");


    GENERATOR* genptr = get_test_generator();
    SYNC_GENERATOR_MODEL* model = (GENCLS*) get_test_sync_generator_model();
    model->update_source_impedance();

    complex<double> Z = genptr->get_source_impedance_in_pu();

    TEST_ASSERT(fabs(model->get_Rs()-Z.real())<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_Xdp()-Z.imag())<FLOAT_EPSILON);
}

void GENCLS_TEST::test_initialize_and_get_initialized_inputs()
{
    show_test_information_for_function_of_class(__FUNCTION__,"GENCLS_TEST");

    GENERATOR* genptr = get_test_generator();
    POWER_SYSTEM_DATABASE& psdb = default_toolkit.get_power_system_database();

    complex<double> V=psdb.get_bus_positive_sequence_complex_voltage_in_pu(1);

    SYNC_GENERATOR_MODEL* model = (GENCLS*) get_test_sync_generator_model();

    complex<double> Z=genptr->get_source_impedance_in_pu();
    complex<double> S(genptr->get_p_generation_in_MW(), genptr->get_q_generation_in_MVar());
    double mbase = genptr->get_mbase_in_MVA();
    S = S/mbase;

    model->set_Tj_in_s(6.0);
    model->set_D(1.0);

    model->initialize();

    complex<double> I, E, SS;
    I = conj(S/V);
    E = V+I*Z;
    SS = S+ steps_fast_complex_abs(I)*steps_fast_complex_abs(I)*Z;

    TEST_ASSERT(fabs(model->get_rotor_angle_in_deg()-rad2deg(steps_fast_complex_arg(E)))<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_rotor_speed_deviation_in_pu()-0.0)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_initial_excitation_voltage_in_pu()-abs(E))<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_initial_mechanical_power_in_pu_based_on_mbase()-SS.real())<FLOAT_EPSILON);
}




void GENCLS_TEST::test_set_get_rotor_angle()
{
    show_test_information_for_function_of_class(__FUNCTION__,"GENCLS_TEST");

    GENCLS* model = (GENCLS*) get_test_sync_generator_model();
    model->set_Tj_in_s(6.0);
    model->set_D(1.0);
    model->initialize();

    model->set_rotor_angle_in_deg(10.0);
    TEST_ASSERT(fabs(model->get_rotor_angle_in_deg()-10.0)<FLOAT_EPSILON);
}

void GENCLS_TEST::test_set_get_rotor_speed()
{
    show_test_information_for_function_of_class(__FUNCTION__,"GENCLS_TEST");

    GENCLS* model = (GENCLS*) get_test_sync_generator_model();
    model->set_Tj_in_s(6.0);
    model->set_D(1.0);

    model->initialize();

    model->set_rotor_speed_deviation_in_pu(0.1);
    TEST_ASSERT(fabs(model->get_rotor_speed_deviation_in_pu()-0.1)<FLOAT_EPSILON);
}

#endif
