from c11type import C11Type

class C11TypeBool(C11Type):
    def __init__(self):
        C11Type.__init__(self)
        self.typeName = u'bool'

    def setSchema(self, schemaName, schemaValue):
        C11Type.setSchema(self, schemaName, schemaValue)

    @classmethod
    def codeDefaultValue(cls, schemaDefaultValue):
        if schemaDefaultValue is not None and schemaDefaultValue is True:
            return u'true'
        return u'false'

    @classmethod
    def codeDefaultValueArray(cls, schemaDefaultValues):
        if schemaDefaultValues is None\
            or not isinstance(schemaDefaultValues, list)\
            or len(schemaDefaultValues) <= 0:
            return u''
        code_default_value = u''
        for schema_value in schemaDefaultValues:
            if len(code_default_value) > 0:
                code_default_value = code_default_value + u', '
            if schema_value == True:
                code_default_value = code_default_value + u'true'
            else:
                code_default_value = code_default_value + u'false'
        return u'{ %s }' % code_default_value

    @classmethod
    def codeJsonCheck(cls):
        return u'IsBool()'

    @classmethod
    def codeJsonSet(cls, dataName, variableName):
        return u'%s.%s = _JsonValue[GLTFTEXT("%s")].GetBool();' % (dataName, variableName, variableName)

    @classmethod
    def codeJsonGet(cls, dataName, variableName):
        return u'_JsonValue[GLTFTEXT("%s")].SetBool(%s.%s);' % (variableName, dataName, variableName)
