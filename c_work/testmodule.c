#define PY_SSIZE_T_CLEAN
#include "Python.h"

double add_two (double a, double b);
double average (int size_of_array, double start_number, double end_number);

double add_two (double a, double b)
{
    double sum = a + b;

    return sum;
}


double average (int size_of_array, double start_number, double end_number)
{

    double array[size_of_array];

    double increment = (end_number - start_number)/size_of_array; 
    
    int index;

    for (index = 0; index < size_of_array; index++)
    {
        array[index] = start_number + index*increment;
    }

    double average = 0.0;
    for (index = 0; index < size_of_array; index++)
    {
        average += array[index];
    }

    average = average/size_of_array;

    return average;

}

static PyObject *get_sum(PyObject *self, PyObject *args)
{
    double a;
    double b;

    if (!PyArg_ParseTuple(args, "dd", &a, &b))
        return NULL;
    double sum;
    sum = add_two(a, b);
    
    return Py_BuildValue("d", sum);
}


static PyObject *get_average(PyObject *self, PyObject *args)
{
    int size_of_array;
    double start;
    double end;

    if (!PyArg_ParseTuple(args, "idd", &size_of_array, &start, &end))
        return NULL;
    double mean;
    mean = average(size_of_array, start, end);

    return Py_BuildValue("d", mean); 
}

static PyMethodDef TestMethods[] = {
    {"get_sum",  (PyCFunction) get_sum, METH_O,
     "Convert C Sum function into python sum function."},
    {"get_average", (PyCFunction) get_average, METH_O, "Convert C Average function into python average function."},
    {NULL}        /* Sentinel */
};

static struct PyModuleDef testmodule = {
    PyModuleDef_HEAD_INIT,
    "test1",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    TestMethods,
    NULL
};

PyMODINIT_FUNC
PyInit_test1(void)
{
    return PyModule_Create(&testmodule);
}