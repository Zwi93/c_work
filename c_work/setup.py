from distutils.core import setup, Extension

module1 = Extension('test1',
                    sources = ['testmodule.c'])

setup (name = 'TestPackage1',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
       