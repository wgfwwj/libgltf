import sys
import os
import argparse
import logging
import json

from c11types import BuildC11Type
from c11types.c11typestruct import C11TypeStruct

logging.basicConfig(level=logging.DEBUG, format=u'%(asctime)s [%(name)s][%(levelname)s](%(filename)s:%(lineno)d) %(message)s')
logger = logging.getLogger(name=u'JSONSchemaToC11')

class C11TypeLibrary(object):
    def __init__(self):
        self.c11Types = dict()

    def addC11Type(self, schemaName, c11Type):
        if schemaName in self.c11Types:
            return (1, u'already have %s in c11 type library' % schemaName)
        self.c11Types[schemaName] = c11Type
        return (0, u'')

    def addSchema(self, rootPath, schemaFileName):
        schemaFilePath = os.path.join(rootPath, schemaFileName)
        with open(schemaFilePath, u'r') as schemaFile:
            schema = json.load(schemaFile)
            if schema == None:
                return (1, u'Can\'t parse the schema file %s' % schemaFilePath)
            (c11Type, errorCode, errorMessage) = BuildC11Type(schemaFileName, schema)
            if errorCode != 0:
                return (errorCode, u'Has error when build - %s' % errorMessage)
            (errorCode, errorMessage) = self.addC11Type(schemaFileName, c11Type)
            if errorCode != 0:
                return (errorCode, u'Has error when add - %s' % errorMessage)
        return (0, u'')

    def addSchemaDirectory(self, schemaDirectory):
        if not os.path.isdir(schemaDirectory):
            return (1, u'The schema directory (%s) is not a valid directory' % schemaDirectory)
        
        for rootPath, directionNames, fileNames in os.walk(schemaDirectory, topdown=False):
            for fileName in fileNames:
                if not fileName.endswith(u'schema.json'):
                    continue
                (errorCode, errorMessage) = self.addSchema(rootPath, fileName)
                if errorCode != 0:
                    return (errorCode, errorMessage)
        return (0, u'')

    def codeHeaderParser(self):
        codeLines = []
        codeLines.append(u'struct SGlTF;')
        codeLines.append(u'bool ParseByString(const std::wstring& _sContent, std::shared_ptr<SGlTF>& _pGlTF);')
        return codeLines

    def preprocess(self):
        for key in self.c11Types:
            (errorCode, errorMessage) = self.c11Types[key].revise(self.c11Types)
            if errorCode != 0:
                return (errorCode, errorMessage)
        return (0, u'')

    def generate(self, headerFileName, sourceFileName, outputHeaderPath=None, outputSourcePath=None, namespace=None):
        headerFilePath = headerFileName
        sourceFilePath = sourceFileName
        if outputHeaderPath != None:
            headerFilePath = os.path.join(outputHeaderPath, headerFileName)
        if outputSourcePath != None:
            sourceFilePath = os.path.join(outputSourcePath, sourceFileName)

        with open(headerFilePath, u'w') as headerFile:
            headerFile.write(u'#pragma once\n')
            headerFile.write(u'\n')
            headerFile.write(u'#include <stdint.h>\n')
            headerFile.write(u'#include <vector>\n')
            headerFile.write(u'#include <string>\n')
            headerFile.write(u'#include <memory>\n')
            headerFile.write(u'\n')

            beginSpace = u''
            if namespace != None:
                headerFile.write(u'namespace %s\n' % namespace)
                headerFile.write(u'{\n')
                beginSpace = u'    '

            codeHeaderParserLines = self.codeHeaderParser()
            for codeHeaderParserLine in codeHeaderParserLines:
                codeHeaderParserLine = u'%s%s\n' % (beginSpace, codeHeaderParserLine)
                headerFile.write(codeHeaderParserLine)
            if len(codeHeaderParserLines) > 0:
                headerFile.write(u'\n')

            parentTypeNames = []
            for key in self.c11Types:
                c11Type = self.c11Types[key]
                if c11Type.codeTypeName() in parentTypeNames:
                    continue

                c11TypeCodeLines = c11Type.codeHeader(parentTypeNames)
                for c11TypeCodeLine in c11TypeCodeLines:
                    if len(c11TypeCodeLine) > 0:
                        c11TypeCodeLine = u'%s%s' % (beginSpace, c11TypeCodeLine)
                    headerFile.write(u'%s\n' % c11TypeCodeLine)
                headerFile.write(u'\n')

                parentTypeNames.append(c11Type.codeTypeName())
                if isinstance(c11Type, C11TypeStruct):
                    for c11TypeParentTypeName in c11Type.getParentTypeNames():
                        parentTypeNames.append(c11TypeParentTypeName)

            if namespace != None:
                headerFile.write(u'}\n')

        with open(sourceFilePath, u'w') as sourceFile:
            sourceFile.write(u'#include "%s"\n' % headerFileName)
            sourceFile.write(u'\n')

            beginSpace = u''
            if namespace != None:
                sourceFile.write(u'namespace %s\n' % namespace)
                sourceFile.write(u'{\n')
                beginSpace = u'    '

            parentTypeNames = []
            for key in self.c11Types:
                c11Type = self.c11Types[key]
                if c11Type.codeTypeName() in parentTypeNames:
                    continue

                c11TypeCodeLines = c11Type.codeSource(parentTypeNames)
                for c11TypeCodeLine in c11TypeCodeLines:
                    if len(c11TypeCodeLine) > 0:
                        c11TypeCodeLine = u'%s%s' % (beginSpace, c11TypeCodeLine)
                    sourceFile.write(u'%s\n' % c11TypeCodeLine)
                sourceFile.write(u'\n')

                parentTypeNames.append(c11Type.codeTypeName())
                if isinstance(c11Type, C11TypeStruct):
                    for c11TypeParentTypeName in c11Type.getParentTypeNames():
                        parentTypeNames.append(c11TypeParentTypeName)

            if namespace != None:
                sourceFile.write(u'}\n')

        return (0, u'')

def JSONSchemaToC11(argv):
    parser = argparse.ArgumentParser(description=u'Generate c11 code by json schema.')
    parser.add_argument(u'schemaDirectory', metavar=u'schema_directory', type=type(u''), help=u'The directory contains all schema files')
    parser.add_argument(u'codeFileName', metavar=u'code_file_name', type=type(u''), help=u'The output filename of c11 code')
    parser.add_argument(u'--output_header_path', type=type(u''), help=u'Set the output header path')
    parser.add_argument(u'--output_source_path', type=type(u''), help=u'Set the output source path')
    parser.add_argument(u'--namespace', type=type(u''), help=u'Set the namespace')
    args = parser.parse_args(argv)

    if args.output_header_path != None and not os.path.exists(args.output_header_path):
        return (1, u'Invalid output header path')
    if args.output_source_path != None and not os.path.exists(args.output_source_path):
        return (1, u'Invalid output source path')
    if args.output_header_path == None:
        args.output_header_path = u'./'
    if args.output_source_path == None:
        args.output_source_path = u'./'

    c11TypeLibrary = C11TypeLibrary()
    (errorCode, errorMessage) = c11TypeLibrary.addSchemaDirectory(args.schemaDirectory)
    if errorCode != 0:
        return (errorCode, errorMessage)
    (errorCode, errorMessage) = c11TypeLibrary.preprocess()
    if errorCode != 0:
        return (errorCode, errorMessage)
    (errorCode, errorMessage) = c11TypeLibrary.generate(u'%s.h' % args.codeFileName, u'%s.cpp' % args.codeFileName, outputHeaderPath=args.output_header_path, outputSourcePath=args.output_source_path, namespace=args.namespace)
    if errorCode != 0:
        return (errorCode, errorMessage)
    return (0, u'')

if __name__ == u'__main__':
    (errorCode, errorMessage) = JSONSchemaToC11(sys.argv[1:])
    if errorCode != 0:
        logger.error(errorMessage)
    else:
        logger.info(u'Success')
    exit(errorCode)