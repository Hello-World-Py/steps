#ifndef WT3E1_TEST_H
#define WT3E1_TEST_H


#include <cstdlib>
#include <cstring>
#include <istream>
#include <iostream>

#ifdef _MSC_VER
	#pragma warning (disable: 4290)
#endif

#include "cpptest.h"
#include "header/basic/test_macro.h"

#include "header/model/wtg_models/wt_electrical_model/wt3e1.h"
#include "header/model/wtg_models/wt_electrical_model/wt_electrical_model_test.h"
using namespace std;

class WT3E1_TEST : public WT_ELECTRICAL_MODEL_TEST
{
    public:
        WT3E1_TEST();
    protected:
        virtual void setup();
        virtual void tear_down();
    protected:
        virtual void test_get_model_name();
        virtual void test_set_get_parameters();
        virtual void test_initialize();
    private:
};

#endif//WT3E1_TEST_H
