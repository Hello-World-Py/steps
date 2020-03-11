#include "header/basic/test_macro.h"
#include "header/model/sg_models/exciter_model/IEEET1_test.h"
#include "header/basic/utility.h"
#include "header/steps_namespace.h"

#ifdef ENABLE_STEPS_TEST
using namespace std;
IEEET1_TEST::IEEET1_TEST() : EXCITER_MODEL_TEST()
{
    TEST_ADD(IEEET1_TEST::test_get_model_name);
    TEST_ADD(IEEET1_TEST::test_set_get_parameters);
    TEST_ADD(IEEET1_TEST::test_initialize);
}

void IEEET1_TEST::setup()
{
    EXCITER_MODEL_TEST::setup();

    GENERATOR* genptr = get_test_generator();

    IEEET1 model(default_toolkit);
    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    model.set_device_id(genptr->get_device_id());

    model.set_TR_in_s(0.06);
    model.set_KA(40.0);
    model.set_TA_in_s(0.1);
    model.set_VRmax_in_pu(1.0);
    model.set_VRmin_in_pu(-1.0);
    model.set_KE(-0.06);
    model.set_TE_in_s(0.67);
    model.set_KF(0.12);
    model.set_TF_in_s(1.0);
    model.set_E1_in_pu(3.0);
    model.set_SE1_in_pu(0.09);
    model.set_E2_in_pu(4.0);
    model.set_SE2_in_pu(0.368);

    dmdb.add_model(&model);
}

void IEEET1_TEST::tear_down()
{
    EXCITER_MODEL_TEST::tear_down();

    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    dmdb.remove_the_last_model();
}

void IEEET1_TEST::test_get_model_name()
{
    show_test_information_for_function_of_class(__FUNCTION__,"IEEET1_TEST");

    EXCITER_MODEL* model = get_test_exciter_model();

    TEST_ASSERT(model->get_model_name()=="IEEET1");
}

void IEEET1_TEST::test_set_get_parameters()
{
    show_test_information_for_function_of_class(__FUNCTION__,"IEEET1_TEST");

    IEEET1* model = (IEEET1*) get_test_exciter_model();

    TEST_ASSERT(fabs(model->get_TR_in_s()-0.06)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_KA()-40.0)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_TA_in_s()-0.1)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_VRmax_in_pu()-1.0)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_VRmin_in_pu()-(-1.0))<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_KE()-(-0.06))<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_TE_in_s()-0.67)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_KF()-0.12)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_TF_in_s()-1.0)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_E1_in_pu()-3.0)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_SE1_in_pu()-0.09)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_E2_in_pu()-4.0)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_SE2_in_pu()-0.368)<FLOAT_EPSILON);
}

void IEEET1_TEST::test_initialize()
{
    show_test_information_for_function_of_class(__FUNCTION__,"IEEET1_TEST");

    GENERATOR* genptr = get_test_generator();
    SYNC_GENERATOR_MODEL* genmodel = genptr->get_sync_generator_model();
    genmodel->initialize();

    IEEET1* model = (IEEET1*) get_test_exciter_model();

    model->set_SE1_in_pu(0.0);
    model->set_SE2_in_pu(0.0);


    double Efd0 = genmodel->get_initial_excitation_voltage_in_pu();
    double Ecomp = model->get_compensated_voltage_in_pu();

    model->initialize();

    TEST_ASSERT(fabs(model->get_excitation_voltage_in_pu()-Efd0)<FLOAT_EPSILON);
    double Vref = Efd0*model->get_KE()/model->get_KA()+Ecomp;
    TEST_ASSERT(fabs(model->get_voltage_reference_in_pu()-Vref)<FLOAT_EPSILON);
    TEST_ASSERT(fabs(model->get_stabilizing_signal_in_pu()-0.0)<FLOAT_EPSILON);
}


#endif
