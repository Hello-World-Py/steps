# stepspy

> stepspy

stepspy is a Python module of Simulation Toolkit for Electrical Power Systems (STEPS).

## Table of Contents

- [Background](#background)
- [Release Note](#release-note)
- [Install](#install)
- [Usage](#usage)
- [Examples](#examples)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

stepspy is a Python module of Simulation Toolkit for Electrical Power Systems (STEPS). It provides wrapper of APIs of STEPS in a dynamic library.

STEPS is a simulation toolkit for powerflow and dynamic simulation of large-scale power systems. It provides detailed models of bus, line, transformer, HVDC, generator, wind turbine generator, load, and fixed shunt. For more information about STEPS, see (https://github.com/changgang/steps).

## Realse Note

- 1.1.0. Apr. 22, 2020. Add new API: get_(lines/transformers/hvdcs)_between_lines(), set_(generator/wt_generator/pv_unit/energy_storage/load/hvdc)_power(), and is_system_angular_stable().  STEPS kernel version should be >=1.3.
- 1.0.0. Apr. 22, 2020. Add new API: clear_meters() to clear all meters for dynamic simulation. STEPS kernel version should be >=1.2.
- 0.13.0-alpha. Mar.  9, 2020. Add new APIs: change_bus_number() and change_bus_number_with_file(). get_areas(), get_zones(), and get_owners() are marked as deprecated. STEPS kernel version should be >=1.1.1.
- 0.12.0. Feb.  8, 2020. Add new APIs: check_dynamic_least_time_constants(). Recover the save_powerflow_data() API of v0.9.0.
- 0.11.5. Jan. 20, 2020. Add new APIs: set/get_dynamic_model_database_capacity().
- 0.11.4. Jan.  2, 2020. Fix bug of c_unit in pylibsteps.py. 
- 0.11.3. Dec. 27, 2019. Add API to set toolkit log file: set_toolkit_log_file(log_file, log_file_append_mode). This version has fatal bug. DONOT use it. Use new version instead.
- 0.11.2. Dec. 19, 2019. Update 'is' to '==' when comparing string in stepspy.py.
- 0.11.1. Dec. 18, 2019. Add POUCH_CSV and POUCH_STEPS to stepspy for loading dynamic simulation result.
- 0.11.0. Nov. 18, 2019. Modify API of building and saving network matix. Add new API to build and save Z matrix. Not compatible with previous STEPS.
- 0.10.2. Nov. 13, 2019. Add new API get/set_hvdc_power_order_in_MW() for changing HVDC power order in dynamic simulation.
- 0.10.1. Oct. 29, 2019. Add new API load_powerflow_result() to load solved powerflow result for new non-flat start powerflow solution.
- 0.10.0. Oct. 26, 2019. Remove loading of libSTEPS-p.so/dll. Use libSTEPS.so/dll for building STEPS.
- 0.9.1. Oct. 21, 2019. Fix bug by changing c_unit to c_uint. Add warning to get_buses_with_constraints if old version is called.
- 0.9.0. Oct. 19, 2019. Add APIs save_powerflow_data_in_keep_mode/ordered_mode/optimized_mode. save_powerflow_data_in_optimized_mode() is suggested for improving performance. Add APIs of get_all_areas/zones/owners. Update get_buses_with_constraints.
- 0.8.6.1. Oct. 12, 2019. Change returned model name as None if dynamic model does not exist when calling get_xxx_related_model_name().
- 0.8.6. Oct. 12, 2019. Add API check_missing_models(), and get_all_xxxs() for getting all devices of the same type. Add new API check_powerflow_data() to replace check_database().
- 0.8.5. Oct.  9, 2019. Add API to retrieve model dynamic data pair, including generator, wt generator, pv unit, load, line, and HVDC.
- 0.8.4. Sep. 27, 2019. Add API to set/get generator voltage/mechanical power reference, and excitation voltage/mechanical power.
- 0.8.3. Sep. 25, 2019. Add API to get generator/wt_generator/pv_unit/loads with constraints of area and zone number.
- 0.8.2. Sep. 22, 2019. Update close/trip line/transformer breaker APIs, set prepare transformer meter APIs in stepspy.
- 0.8.1. Sep. 18, 2019. Update and README.
- 0.8.0. Sep. 18, 2019. Update to enable both parallel and serial library. Since STEPS 0.6.3.
- 0.7.1. Sep. 18, 2019. Fix API to set and get parallel thread number.
- 0.7.0. Sep. 18, 2019. Add new API to set parallel thread number. Update README.
- 0.6.1. Aug. 27, 2019
- 0.6.0. Aug. 25, 2019


## Install

### Install stepspy

To install stepspy, you can run the following codes on your computer or server:

```python
python -m pip install stepspy
```

To update stepspy, you can run the following codes on your computer or server:

```python
python -m pip install --upgrade stepspy
```

If you want to manually install stepspy, follow the instructions:

1. Go to https://github.com/changgang/steps to download or fork the latest version of STEPS.
2. Go to python/ folder of STEPS, and copy the latest version of stepspy/ to PYTHONPATH/Lib/site-packages/.

### Install dynamic library

After install the stepspy, you still need to compile and install the dynamic library of STEPS.

1. Go to [steps](https://github.com/changgang/steps) to download or fork the latest version of STEPS. The latest version is usually the [work] branch.
2. Compile STEPS into dynamic library following instructions of STEPS.
3, Move the dynamic library of STEPS to stepspy/libsteps/ in the PYTHONPATH/Lib/site-packages/.
4, If the VC runtime is missing, download and install Microsoft Visual C++ 2017 Redistributable of 32 or 64 bit version.
5, If VC runtime or Mingw Runtime is missing, install vcredit or copy libwinpthread-1.dll from mingw compiler/bin/ to c:/windows/system32 and c:/windows/SysWOW64
6, For Windows platform, Python 3.7 and 3.8 may suffer path searching problem for some unknown reason. In this case, copy all dlls in the mingw/bin folder to the same folder of libsteps.dll.


## Usage

## Examples


## Maintainers

[@changgang](https://github.com/changgang) <lichgang@sdu.edu.cn> from the School of Electrical Engineering, Shandong University, China

## Contributing

Feel free to dive in! [Open an issue](https://github.com/changgang/steps/issues/new).

## License

[MIT](LICENSE) @ Changgang Li