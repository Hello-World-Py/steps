#include "header/basic/test_macro.h"
#include "header/model/sg_models/stabilizer_model/PSASPS5_test.h"
#include "header/basic/utility.h"

#ifdef ENABLE_STEPS_TEST
using namespace std;

PSASPS5_TEST::PSASPS5_TEST() : STABILIZER_MODEL_TEST()
{
    TEST_ADD(PSASPS5_TEST::test_get_model_name);
    TEST_ADD(PSASPS5_TEST::test_set_get_parameters);

}

void PSASPS5_TEST::setup()
{
    STABILIZER_MODEL_TEST::setup();

    GENERATOR* genptr = get_test_generator();
    PSASPS5 model(default_toolkit);
    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    model.set_device_id(genptr->get_device_id());

    dmdb.add_model(&model);
}

void PSASPS5_TEST::tear_down()
{
    STABILIZER_MODEL_TEST::tear_down();

    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    dmdb.remove_the_last_model();
}


void PSASPS5_TEST::test_get_model_name()
{
    show_test_information_for_function_of_class(__FUNCTION__,"PSASPS5_TEST");

    PSASPS5* model = (PSASPS5*) get_test_stabilizer_model();
    TEST_ASSERT(model->get_model_name()=="PSASPS5");
}

void PSASPS5_TEST::test_set_get_parameters()
{
    show_test_information_for_function_of_class(__FUNCTION__,"PSASPS5_TEST");

    PSASPS5* model = (PSASPS5*) get_test_stabilizer_model();
    model->set_K1(1.0);
    TEST_ASSERT(fabs(model->get_K1()-1.0)<FLOAT_EPSILON);

    model->set_T1_in_s(0.1);
    TEST_ASSERT(fabs(model->get_T1_in_s()-0.1)<FLOAT_EPSILON);

    model->set_K2(2.0);
    TEST_ASSERT(fabs(model->get_K2()-2.0)<FLOAT_EPSILON);

    model->set_T2_in_s(0.2);
    TEST_ASSERT(fabs(model->get_T2_in_s()-0.2)<FLOAT_EPSILON);

    model->set_T3_in_s(0.3);
    TEST_ASSERT(fabs(model->get_T3_in_s()-0.3)<FLOAT_EPSILON);

    model->set_T4_in_s(0.4);
    TEST_ASSERT(fabs(model->get_T4_in_s()-0.4)<FLOAT_EPSILON);

    model->set_T5_in_s(0.5);
    TEST_ASSERT(fabs(model->get_T5_in_s()-0.5)<FLOAT_EPSILON);

    model->set_T6_in_s(0.6);
    TEST_ASSERT(fabs(model->get_T6_in_s()-0.6)<FLOAT_EPSILON);

    model->set_T7_in_s(0.7);
    TEST_ASSERT(fabs(model->get_T7_in_s()-0.7)<FLOAT_EPSILON);

    model->set_T8_in_s(0.8);
    TEST_ASSERT(fabs(model->get_T8_in_s()-0.8)<FLOAT_EPSILON);

    model->set_T9_in_s(0.9);
    TEST_ASSERT(fabs(model->get_T9_in_s()-0.9)<FLOAT_EPSILON);

    model->set_T10_in_s(1.0);
    TEST_ASSERT(fabs(model->get_T10_in_s()-1.0)<FLOAT_EPSILON);
}

#endif
