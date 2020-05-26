#ifndef IEEET1_TEST_H
#define IEEET1_TEST_H


#include <cstdlib>
#include <cstring>
#include <iostream>

#ifdef _MSC_VER
	#pragma warning (disable: 4290)
#endif

#include "thirdparty/cpptest/cpptest.h"

#include "header/model/exciter_model/IEEET1.h"
#include "header/model/exciter_model/exciter_model_test.h"
using namespace std;

class IEEET1_TEST : public EXCITER_MODEL_TEST
{
    public:
        IEEET1_TEST();
    protected:
        virtual void setup();
        virtual void tear_down();
    protected:
        virtual void test_get_model_type();
        virtual void test_get_model_name();
        virtual void test_set_get_parameters();
        virtual void test_initialize();
        virtual void test_set_get_voltage_reference();
        virtual void test_step_response();
        virtual void test_get_standard_model_string();
    private:
        IEEET1* model;
};

#endif//IEEET1_TEST_H
