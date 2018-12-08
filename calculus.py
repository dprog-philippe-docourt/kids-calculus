"""
This is the Kids Calculus module.

Kids Calculus is a generator of arithmetic expressions for kids. The generator provides expressions using the
operators `+`, `-`, and `*`. The command line version provides 10 levels of difficulties. Subtraction and then
multiplication are introduced as the difficulty increases.
"""

import argparse
import datetime
import json
import random
import sys

ALLOWED_OPERATORS = ('+', '-', '*')
MAX_NUMBER = 1000
MAX_ABSOLUTE_RESULT = 100 * 1000
MAX_COUNT = 100
MAX_OPERAND_COUNT = 6
MIN_LEVEL = 1
MAX_LEVEL = 10


class CalculusOptions(object):
    """Represents the set of options available for generating arithmetic expressions with `CalculusGenerator`."""
    def __init__(self, min_number=0, max_number=10, allows_negative_result=False, max_absolute_result=30,
                 operators=('+', '-'), min_operand_count=2, max_operand_count=3):
        for op in operators:
            if op not in ALLOWED_OPERATORS:
                raise ValueError('Operator must be one of %s.' % ', '.join(ALLOWED_OPERATORS))
        if max_number > MAX_NUMBER or max_number < 3:
            raise ValueError('Max number must be within [3; %i].' % MAX_NUMBER)
        if min_number >= max_number or min_number < 0:
            raise ValueError('Min number must be within [0; %i[.' % max_number)
        if max_absolute_result < 10 or max_absolute_result > MAX_ABSOLUTE_RESULT:
            raise ValueError('Max absolute result must be within [10; %i].' % MAX_ABSOLUTE_RESULT)
        if max_operand_count < 2 or max_operand_count > MAX_OPERAND_COUNT:
            raise ValueError('Max operand count must be within [2; %i].' % MAX_OPERAND_COUNT)
        if min_operand_count < 2 or min_operand_count > max_operand_count:
            raise ValueError('Min operand count must be within [2; %i].' % max_operand_count)
        if type(allows_negative_result) is not bool:
            raise ValueError('Parameter allows_negative_result must be a boolean.')
        self.min_number = min_number
        self.max_number = max_number
        self.allows_negative_result = allows_negative_result
        self.max_absolute_result = max_absolute_result
        self.operators = operators
        self.min_operand_count = min_operand_count
        self.max_operand_count = max_operand_count

    def __str__(self):
        data = dict(
            min_number=self.min_number,
            max_number=self.max_number,
            allows_negative_result=self.allows_negative_result,
            max_absolute_result=self.max_absolute_result,
            operators=self.operators,
            min_operand_count=self.min_operand_count,
            max_operand_count=self.max_operand_count,
        )
        return json.dumps(data)


class CalculusGenerator(object):
    """A generator of random, simple arithmetic expressions."""
    ALLOWED_FORMATS = ['html', 'text']

    def __init__(self, options, title=None, subtitle=None):
        self.options = options
        self.title = title or 'Calculus'
        self.subtitle = subtitle or str(datetime.date.today())

    def generate_expressions(self, count=10):
        if count < 1 or count > MAX_COUNT:
            raise ValueError('Count must be within [1; %i].' % MAX_COUNT)
        for i in range(0, count):
            value = random.randint(0, self.options.max_number)
            calculus = str(value)
            operand_count = random.randint(self.options.min_operand_count - 1, self.options.max_operand_count - 1)
            op_i = 0
            while op_i < operand_count:
                operator = random.choice(self.options.operators)
                if operator == '*':
                    # Do not use too big values for second operand of multiplication, and reduce probability to have 0
                    # as operand.
                    value = random.randint(1, min(self.options.max_number // 2, 20))
                else:
                    value = random.randint(0, self.options.max_number)
                temp_calculus = calculus + ' %s %i' % (operator, value)
                result = eval(temp_calculus)
                if not self.options.allows_negative_result and result < 0:
                    continue
                if abs(result) > self.options.max_absolute_result:
                    continue
                calculus = temp_calculus
                op_i += 1
            calculus += ' ='
            yield calculus

    def _print_html_header(self, stream):
        stream.write('<!DOCTYPE html>\n<meta http-equiv="content-type" content="text/html; charset=utf-8"><title>{0}</title></meta>\n<html>\n<body>\n'.format(self.title))
        if self.title:
            stream.write('<h1>{0}</h1>\n'.format(self.title))
        if self.subtitle:
            stream.write('<h2>{0}</h2>\n'.format(self.subtitle))

    def _print_text_header(self, stream):
        if self.title:
            stream.write('{0}\n=====\n\n'.format(self.title))
        if self.subtitle:
            stream.write('{0}\n-----\n\n'.format(self.subtitle))

    def _print_html_footer(self, stream):
        stream.write('</body>\n</html>\n')

    def print_calculus_as_html(self, stream=sys.stdout, count=10, include_header=True, include_footer=True):
        if include_header:
            self._print_html_header(stream)
        for calculus in self.generate_expressions(count):
            stream.write('<p>%s</p>\n' % calculus)
        if include_footer:
            self._print_html_footer(stream)

    def print_calculus_as_plain_text(self, stream=sys.stdout, count=10, include_header=True):
        if include_header:
            self._print_text_header(stream)
        for expression in self.generate_expressions(count):
            stream.write(expression + '\n')

    def print_calculus(self, stream=sys.stdout, count=10):
        if args.format == 'html':
            self.print_calculus_as_html(stream=stream, count=count)
        else:
            self.print_calculus_as_plain_text(stream=stream, count=count)


def get_options_for_level(level):
    """
    Empirical heuristic for picking an appropriate option set according to the requested level of difficulty.

    This code is internal API and may change at any time in order to provide a smoother progression in the difficulty.
    """
    if level > MAX_LEVEL or level < MIN_LEVEL:
        raise ValueError('Level must be within [%i; %i].' % (MIN_LEVEL, MAX_LEVEL))
    max_number = [3, 5, 6, 8, 10, 15, 20, 25, 50, 100][level - 1]
    min_number = 0 if level > 1 else 1
    if level < 4:
        max_absolute_result = 3 * level + 10
    elif level < 6:
        max_absolute_result = 10 * level + 20
    else:
        max_absolute_result = 2 * (level * level) + 10 * level
    if level < 3:
        max_operand_count = 2
    else:
        max_operand_count = (level + 1) - level // 2
    min_operand_count = 2
    if level > 5:
        min_operand_count = 3
    allows_negative_result = level > 6
    if level <= 2:
        operators = ('+',)
    elif level <= 5:
        operators = ('+', '-')
    else:
        operators = ALLOWED_OPERATORS
    return CalculusOptions(min_number=min_number, max_number=max_number, allows_negative_result=allows_negative_result, min_operand_count=min_operand_count, max_operand_count=max_operand_count, max_absolute_result=max_absolute_result, operators=operators)


if __name__ == '__main__':
    app = argparse.ArgumentParser(prog='Kids Calculus', description='A generator of arithmetic expressions for kids.')
    app.add_argument('-l', '--level', default=1, type=int, choices=range(MIN_LEVEL, MAX_LEVEL + 1), required=False, help="Level of difficulty in range [1; 10]. 1 to 3 is meant for 4 to 5 years old. 4 to 5 is meant for 6 to 8 years old. 6 to 8 is meant for 8 to 12 years old. 9 to 10 is meant for 12 years old and more.")
    app.add_argument('-c', '--count', default=10, type=int, required=False, help="The number of arithmetic expressions to generate.")
    app.add_argument('-f', '--format', default='text', type=str, required=False, choices=CalculusGenerator.ALLOWED_FORMATS, help="The output format.")
    app.add_argument('-o', '--output', type=str, required=False, help="The file path used to output the generated arithmetic expressions. Default to stdout if none given.")
    app.add_argument('-t', '--title', type=str, required=False, help="A custom title for the generated content. A default title is automatically generated, unless an explicit empty string is given.")
    app.add_argument('-s', '--subtitle', type=str, required=False, help="A custom subtitle for the generated content. A default subtitle is automatically generated, unless an explicit empty string is given.")
    args = app.parse_args()

    subtitle = args.subtitle or 'Level %i/%i, %s' % (args.level, MAX_LEVEL, datetime.date.today())
    generator = CalculusGenerator(get_options_for_level(args.level), title=args.title, subtitle=subtitle)

    if args.output:
        with open(args.output, mode='wt', encoding='utf-8') as f:
            generator.print_calculus(stream=f, count=args.count)
    else:
        generator.print_calculus(count=args.count)
