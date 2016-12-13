import os
import unittest

import java_sk.main
import java_sk.util
from . import TestCommon

pwd = os.path.dirname(__file__)
tests = os.path.join(pwd, "new_ast")

class TestJava(TestCommon):
    def __test(self, fs):
        _fs = map(lambda f: os.path.join(tests, f), fs)
        ret = java_sk.main.main(_fs)
        self.assertEqual(ret, 0)
        
    def test_Args(self):
        self.__test(["Args.java"])

    def test_Array(self):
        self.__test(["Array.java"])

    def test_BooMoo(self):
        self.__test(["BooMoo.java"])

    def test_Calls(self):
        self.__test(["Calls.java"])

    def test_CallTypes(self):
        self.__test(["CallTypes.java"])

    def test_ClassField(self):
        self.__test(["ClassField.java"])

    def test_Construct(self):
        self.__test(["Construct.java"])

    def test_Creation(self):
        self.__test(["Creation.java"])

    def test_Fields(self):
        self.__test(["Fields.java"])
        
    def test_Generators(self):
        self.__test(["Generators.java"])
        
    def test_Hole(self):
        self.__test(["Hole.java"])
        
    def test_IdentifyLoose(self):
        self.__test(["IdentifyLoose.java"])
        
    def test_IdentifyStrict(self):
        self.__test(["IdentifyStrict.java"])
        
    def test_Iface(self):
        self.__test(["Iface.java"])
        
    def test_IfaceTypes(self):
        self.__test(["IfaceTypes.java"])
        
    def test_LocalStaticCalls(self):
        self.__test(["LocalStaticCalls.java"])
        
    def test_NestedClasses(self):
        self.__test(["NestedClasses.java"])
        
    def test_NonLocalCalls(self):
        self.__test(["NonLocalCalls.java"])
        
    def test_Override(self):
        self.__test(["Override.java"])
        
    def test_SimpleArray(self):
        self.__test(["SimpleArray.java"])
        
    def test_StaticCalls(self):
        self.__test(["StaticCalls.java"])
        
    def test_Static(self):
        self.__test(["Static.java"])
        
    def test_SubclassParamCalls(self):
        self.__test(["SubclassParamCalls.java"])

    def test_SuperCalls(self):
        self.__test(["SuperCalls.java"])

    def test_Super(self):
        self.__test(["Super.java"])
        
    def test_Switch(self):
        self.__test(["Switch.java"])
        
    def test_This(self):
        self.__test(["This.java"])
        
    def test_ThisCalls(self):
        self.__test(["ThisCalls.java"])

if __name__ == '__main__':
  unittest.main()

