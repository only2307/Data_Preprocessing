import sys
import numpy as np
import pandas as pd 
from pandas.api.types import is_string_dtype
import argparse
import math

#we will use infix expression to express operations
def get_expression(s): #make a raw string to a list of operator and operand that we can easy to calculate
    s = s.replace(" ", "")
    operator = ['+', '-', '*', '/', '(', ')']   #List of operator
    expression = []
    expression.append(s[0])
    if(s[0] == '('):
        expression.append('')
    for i in range(1, len(s)):
        if s[i] in operator:
            if(expression[-1] != ''):
                expression.append(s[i])
            else:
                expression[-1] = s[i]
            expression.append('')
        else:
            expression[-1] += s[i]
    if(s[-1] in operator):
        expression.append(s[-1])
    return expression

def calc(a, op, b):         #Calculate: a op(+, -, *, /) b
    if(op == '+'):
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        return a / b
        
def calculate(row, expression):
    operand_stack = []
    operator_stack = []
    operator = {'+' : 0, '-' : 0, '*' : 1, '/' : 1} #List of operator and priority
    for x in expression:
        if(x != '(' and x != ')' and x not in operator): #if x is an operand then push is to operand stack
            if(x.isnumeric()):
                operand_stack.append(float(x))
            else:
                operand_stack.append(row[x])
        if(x == '('): #If x is open bracket then push is to operator stack
            operator_stack.append(x)
        if(x in operator): #If x is and operator
            #If that is an operator that has priority not greater than x
            while(len(operator_stack) > 0 and operator_stack[-1] != '(' and operator[x] <= operator[operator_stack[-1]]):
                #We pop 2 operand and 1 operator to calulate and push it to operand stack
                a = operand_stack.pop()
                b = operand_stack.pop()
                op = operator_stack.pop()
                operand_stack.append(calc(a, op, b))
            #Otherwise, just push to operator stack
            operator_stack.append(x)
        if(x == ')'): #If x is close bracket
            #We pop 2 operand and 1 operator to calculate until top of operator stack is open bracket
            while(operator_stack[-1] != '('):
                a = operand_stack.pop()
                b = operand_stack.pop()
                op = operator_stack.pop()
                operand_stack.append(calc(b, op, a))
            operator_stack.pop()
    while(len(operator_stack) > 0): #pop 2 operand and 1 operator to calculate until operator stack is empty
        a = operand_stack.pop()
        b = operand_stack.pop()
        op = operator_stack.pop()
        operand_stack.append(calc(b, op, a))
    return operand_stack.pop()

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input"
    )
    parser.add_argument(
        "-o",
        "--output",
    )
    args = parser.parse_args()
    return args.input, args.output

if __name__ == "__main__":
    input_file, output_file = arg_parser()
    data = pd.read_csv(input_file)
    attributes = list(data)
    exp = input("Enter expression: ") #Expression that we want to calculate
    expression = get_expression(exp) #Raw String to expression for calculate
    alter_name = input("Enter new column name: ") #Name of new column
    if(alter_name == ''):
        attributes.append(' '.join(e for e in expression))
    else:
        attributes.append(alter_name)

    use_attributes = []  #Label of attributes use in expression
    for x in expression:
        if(len(x) > 1 and x.isnumeric() == False):  #Push all operand that may be an attributes list
            use_attributes.append(x)
    for attr in use_attributes:
        if attr not in attributes or is_string_dtype(data[attr]): #Check if it's an attribute or not
            #We also can't calculate of attribute's data type isn't numeric
            print(f"Invalid attributes: {attr}")
            sys.exit()

    f = open(output_file, 'w')
    f.write(','.join(attr for attr in attributes) + '\n') #Write attributes label
    for index, row in data.iterrows():
        next_line = []
        calculatable = True         
        for i in range(len(attributes) - 1):
            attr = attributes[i]
            next_line.append(str(row[attr]))
            if(attr in use_attributes and pd.isna(row[attr])):
                calculatable = False #If there're a missing value in a row, we don't calculate
        if(calculatable):
            next_line.append(str(calculate(row, expression))) #Calculate expression
        else:
            next_line.append('')  #Missing value if we don't calculate
        f.write(','.join(cell for cell in next_line) + '\n')  #Write line to output file
    f.close()