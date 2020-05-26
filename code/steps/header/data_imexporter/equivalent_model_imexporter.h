#ifndef EQUIVALENT_MODEL_IMEXPORTER_H
#define EQUIVALENT_MODEL_IMEXPORTER_H

#include "header/power_system_database.h"
#include <vector>
class EQUIVALENT_MODEL_IMEXPORTER
{
    public:
        EQUIVALENT_MODEL_IMEXPORTER(STEPS& toolkit);
        ~EQUIVALENT_MODEL_IMEXPORTER();
        STEPS& get_toolkit() const;

        void load_equivalent_model(string file);
    private:
        void load_data_into_ram(string file);
        METER get_meter_from_data(const vector<string> & data_line, unsigned int& delay, double& coefficient);
        void add_equivalent_device(vector< vector<string> >& model_data);
        void load_ARXL_model(vector< vector<string> >& model_data);
    private:
        STEPS* toolkit;
        vector< vector< vector<string> > > data_in_ram;

};

#endif // POWERFLOW_ASSEMBLER_H
