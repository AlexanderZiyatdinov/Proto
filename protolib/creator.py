from typing import List
import logging
from pyparsing import nestedExpr
from protolib.definitions import WIRE_TYPES

logging.basicConfig(level=logging.DEBUG)


class Creator:
    """Return .py file with dataclass which generate from .proto file"""

    def __init__(self, input_file, output_file=None):
        self.__input_file: str = input_file
        self.__output_file: str = output_file
        self.__template = """# Result of code generation
from dataclasses import dataclass
from protolib.dataclasses_ import field
from protolib import types\n\n"""
        self.__tab_index = 0
        self.tab = '    '
        self.added_classes = []

    def proto2python(self) -> None:
        """Create .py file from .proto"""
        logging.info(' | File to deserialize: %s', self.__input_file)
        with open(self.__input_file) as f:
            proto_text = f.read()
        parser = _Parser(proto_text=proto_text)
        tokens = parser.parse()
        self.__generate_python_text(tokens[0])
        output_filename = (self.__output_file + '_proto.py'
                           if self.__output_file
                           else '_proto.py')
        with open(output_filename, 'w') as output:
            output.write(self.__template)
        logging.info(' | Generated file: %s', output_filename)

    def __generate_python_text(self, tokens: List[str | List[str]]) -> None:
        # Todo rewrite this method for all cases
        pointer = 0
        while pointer != len(tokens):
            if tokens[pointer] == 'message':
                classname = tokens[pointer + 1]
                content = tokens[pointer + 2]
                pointer += 2
                self.__template += '\n' + self.tab*self.__tab_index + "@dataclass\n"
                self.__template += self.tab*self.__tab_index + f"class {classname}:\n"
                self.added_classes.append(classname)
                self.__tab_index += 1
                self.__generate_python_text(content)
                self.__tab_index -= 1
            elif tokens[pointer] in WIRE_TYPES or tokens[pointer] in self.added_classes:
                if tokens[pointer] in self.added_classes:
                    type = tokens[pointer]
                else:
                    type = f"types.{tokens[pointer]}"
                name = tokens[pointer + 1]
                value = int(tokens[pointer + 3][:-1])
                pointer += 3

                self.__template += self.tab*self.__tab_index + f"{name}: {type} = field({value})\n"
            pointer += 1


class _Parser:
    """Parse .proto file text to .py text view"""

    def __init__(self, proto_text: str):
        self.proto_text: str = proto_text

    def parse(self) -> List[str | List[str]]:
        pattern = '{' + self.proto_text + '}'
        return nestedExpr('{', '}').parseString(pattern).asList()
