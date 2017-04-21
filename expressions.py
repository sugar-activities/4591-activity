#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Command usage:
# expressions.py expression
# Example:
# python expressions.py "3x^6(x^6/25.9)"

def convert(expression):
    #Multiplication
    expression = expression.replace('0x', '0*x')
    expression = expression.replace('1x', '1*x')
    expression = expression.replace('2x', '2*x')
    expression = expression.replace('3x', '3*x')
    expression = expression.replace('4x', '4*x')
    expression = expression.replace('5x', '5*x')
    expression = expression.replace('6x', '6*x')
    expression = expression.replace('7x', '7*x')
    expression = expression.replace('8x', '8*x')
    expression = expression.replace('9x', '9*x')
    expression = expression.replace(')(', ')*(')
    expression = expression.replace(')x', ')*x')
    expression = expression.replace(')0', ')*0')
    expression = expression.replace(')1', ')*1')
    expression = expression.replace(')2', ')*2')
    expression = expression.replace(')3', ')*3')
    expression = expression.replace(')4', ')*4')
    expression = expression.replace(')5', ')*5')
    expression = expression.replace(')6', ')*6')
    expression = expression.replace(')7', ')*7')
    expression = expression.replace(')8', ')*8')
    expression = expression.replace(')9', ')*9')
    expression = expression.replace('0(', '0*(')
    expression = expression.replace('1(', '1*(')
    expression = expression.replace('2(', '2*(')
    expression = expression.replace('3(', '3*(')
    expression = expression.replace('4(', '4*(')
    expression = expression.replace('5(', '5*(')
    expression = expression.replace('6(', '6*(')
    expression = expression.replace('7(', '7*(')
    expression = expression.replace('8(', '8*(')
    expression = expression.replace('9(', '9*(')
    expression = expression.replace('x(', 'x*(')
    #Power again
    expression = expression.replace('^', '**')
    numbers = [str(i) for i in range(10)]
    converted_list = []
    has_point = False
    on_number = False
    for i in expression:
        if not i in numbers:
            if on_number:
                if i == '.':
                    has_point = True
                else:
                    if not has_point:
                        converted_list.append('.0')
                    on_number = False
                    has_point = False
        else:
            on_number = True
        converted_list.append(i)
    if on_number and not has_point:
        converted_list.append('.0')
    return ''.join(converted_list)

if __name__ == "__main__":
    import sys
    print convert(sys.argv[1])
