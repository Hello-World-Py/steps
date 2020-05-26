#include "header/basic/test_macro.h"
#include "header/model/sg_models/stabilizer_model/PSASPS6_test.h"
#include "header/basic/utility.h"
#include "header/steps_namespace.h"

#ifdef ENABLE_STEPS_TEST
using namespace std;

PSASPS6_TEST::PSASPS6_TEST() : STABILIZER_MODEL_TEST()
{
    TEST_ADD(PSASPS6_TEST::test_get_model_name);
    TEST_ADD(PSASPS6_TEST::test_set_get_parameters);

}

void PSASPS6_TEST::setup()
{
    STABILIZER_MODEL_TEST::setup();

    GENERATOR* genptr = get_test_generator();
    PSASPS6 model(default_toolkit);
    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    model.set_device_id(genptr->get_device_id());

    dmdb.add_model(&model);
}

void PSASPS6_TEST::tear_down()
{
    STABILIZER_MODEL_TEST::tear_down();

    DYNAMIC_MODEL_DATABASE& dmdb = default_toolkit.get_dynamic_model_database();
    dmdb.remove_the_last_model();
}


void PSASPS6_TEST::test_get_model_name()
{
    show_test_information_for_function_of_class(__FUNCTION__,"PSASPS6_TEST");

    PSASPS6* model = (PSASPS6*) get_test_stabilizer_model();
    TEST_ASSERT(model->get_model_name()=="PSASPS6");
}

void PSASPS6_TEST::test_set_get_parameters()
{
    show_test_information_for_function_of_class(__FUNCTION__,"PSASPS6_TEST");

    PSASPS6* model = (PSASPS6*) get_test_stabilizer_model();

    model->set_Kw(1.0);
    TEST_ASSERT(fabs(model->get_Kw()-1.0)<FLOAT_EPSILON);

    model->set_Trw_in_s(0.1);
    TEST_ASSERT(fabs(model->get_Trw_in_s()-0.1)<FLOAT_EPSILON);

    model->set_T5_in_s(0.5);
    TEST_ASSERT(fabs(model->get_T5_in_s()-0.5)<FLOAT_EPSILON);

    model->set_T6_in_s(0.6);
    TEST_ASSERT(fabs(model->get_T6_in_s()-0.6)<FLOAT_EPSILON);

    model->set_T7_in_s(0.7);
    TEST_ASSERT(fabs(model->get_T7_in_s()-0.7)<FLOAT_EPSILON);

    model->set_Kr(1.5);
    TEST_ASSERT(fabs(model->get_Kr()-1.5)<FLOAT_EPSILON);

    model->set_Trp_in_s(0.12);
    TEST_ASSERT(fabs(model->get_Trp_in_s()-0.12)<FLOAT_EPSILON);

    model->set_Tw_in_s(0.22);
    TEST_ASSERT(fabs(model->get_Tw_in_s()-0.22)<FLOAT_EPSILON);

    model->set_Tw1_in_s(0.13);
    TEST_ASSERT(fabs(model->get_Tw1_in_s()-0.13)<FLOAT_EPSILON);

    model->set_Tw2_in_s(0.23);
    TEST_ASSERT(fabs(model->get_Tw2_in_s()-0.23)<FLOAT_EPSILON);

    model->set_Ks(2.5);
    TEST_ASSERT(fabs(model->get_Ks()-2.5)<FLOAT_EPSILON);

    model->set_Kp(1.5);
    TEST_ASSERT(fabs(model->get_Kp()-1.5)<FLOAT_EPSILON);

    model->set_T1_in_s(0.2);
    TEST_ASSERT(fabs(model->get_T1_in_s()-0.2)<FLOAT_EPSILON);

    model->set_T2_in_s(0.3);
    TEST_ASSERT(fabs(model->get_T2_in_s()-0.3)<FLOAT_EPSILON);

    model->set_T13_in_s(0.41);
    TEST_ASSERT(fabs(model->get_T13_in_s()-0.41)<FLOAT_EPSILON);

    model->set_T14_in_s(0.51);
    TEST_ASSERT(fabs(model->get_T14_in_s()-0.51)<FLOAT_EPSILON);

    model->set_T3_in_s(0.4);
    TEST_ASSERT(fabs(model->get_T3_in_s()-0.4)<FLOAT_EPSILON);

    model->set_T4_in_s(0.5);
    TEST_ASSERT(fabs(model->get_T4_in_s()-0.5)<FLOAT_EPSILON);

    model->set_Vsmax(3.0);
    TEST_ASSERT(fabs(model->get_Vsmax()-3.0)<FLOAT_EPSILON);

    model->set_Vsmin(2.0);
    TEST_ASSERT(fabs(model->get_Vsmin()-2.0)<FLOAT_EPSILON);
}

#endif
