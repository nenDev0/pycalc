from enum import IntEnum
from src.log import log

class Calc_Type(IntEnum):
    ADDITION = 0
    POWER = 1
    MULTIPLICATION = 2
    DIVISON = 3
    ROOT = 4
    MODULUS = 5


def calculate(a: float, b: float, calc_type: Calc_Type):
    log.debug(f'a, b: {a} :: {b} ::: type: {calc_type}')
    match calc_type:
        case Calc_Type.ADDITION:
            return addition(a,b)    
        case Calc_Type.MULTIPLICATION:
            return multiplication(a,b) 
        case Calc_Type.DIVISON:
            return division(a,b) 
        case Calc_Type.POWER:
            return power(a,b) 
        case Calc_Type.POWER:
            return power(a,1/b) 
        case Calc_Type.MODULUS:
            return modulus(a,b) 

def addition(a: float, b: float) -> float:
    if a==None:
        return b
    return a+b


def multiplication(a: float, b: float) -> float:
    if a==None:
        return b
    return a*b


def division(a: float, b: float) -> float:
    if a==None:
        return b
    if b==0:
        return None
    return a/b


def power(a: float, b: float) -> float:
    if a==None:
        return b
    return a**b


def modulus(a: float, b: float) -> float:
    if a==None:
        return b
    return a % b



def read_term(term: str):
    term = separate_brackets(term)
    log.debug(f'term, separate_brackets: {term}')
    term = check_calculation_types(term, Calc_Type.ADDITION)
    if type(term) == complex:
        return None
    if type(term) == str:
        term = term.replace('--', '', -1)
    return term

def separate_brackets(term: str):
    if term == None or term == '':
        return None
    
    if term.find("(") != -1 or term.find(")") != -1:
        if term.count("(") != term.count(")"):
            return term
        log.debug(f'sub_term, before: {term}')
        bracket_left = term.index("(")
        bracket_right = None
        term_sub = term.replace("(", "", 1)
        count = 2
        while bracket_right == None:
            # log.debug(f'{term_sub.index("(")}, {term_sub.index(")")}')
            if term_sub.find("(") != -1 and term_sub.index("(") < term_sub.index(")"):
                    term_sub = term_sub.replace("(", "", 1)
                    term_sub = term_sub.replace(")", "", 1)
                    count+=2
                    continue
            bracket_right = term_sub.index(")")+count
            term_sub = term_sub.replace(")", "", 1)

        log.debug(f'sub_term, after: {term_sub}')

        bracket = term[bracket_left: bracket_right]
        log.debug(f'bracket, 1: {bracket}')
        del bracket_right, bracket_left
        log.debug(f'term, split: {term.split(bracket,1)}')
        a, c = term.split(bracket,1)
        bracket = bracket[1:-1]
        log.debug(f'bracket, 2: {bracket}')
        bracket = read_term(bracket)
        if a != '':
            a_c = a[-1]
            log.debug(f'bracket, a: {a[0:-1]}')
            if a[0:-1] != '':
                a = str(read_term(a[0:-1]))
            a = a + a_c
        if c != '':
            c_c = c[0]
            log.debug(f'bracket, c: {c[1:]}')
            if c[1:] != '':
                c = str(read_term(c[1:]))
            c = c_c + c
        term = a + str(bracket) + c
        log.debug(f'term: {term}')
        if type(term) == str:
            term = term.replace('--', '', -1)
    return term

def check_calculation_types(term: str, calc_type: Calc_Type) -> float:

    result = None

    match calc_type:
        case Calc_Type.ADDITION:
            str_type = "+"
        case Calc_Type.POWER:
            str_type = "**"
        case Calc_Type.MULTIPLICATION:
            str_type = "*"
        case Calc_Type.DIVISON:
            str_type = "/"
        case Calc_Type.ROOT:
            str_type = "//"
        case Calc_Type.MODULUS:
            str_type = "%"
    log.debug(f'CCT called, str_type: {str_type}, term: {term}')
    if term.find(str_type)== -1:
        if calc_type!=5:
            term = check_calculation_types(term, calc_type+1)
            if term == None or type(term) == complex:
                return None
        if type(term) == str:
            term = term.replace('--', '', -1)
        return term
    if calc_type != 5:
        slices = term.split(str_type)
        for i in range(len(slices)):
            slices[i] = check_calculation_types(slices[i],calc_type+1)
        result = None
        for i in slices:
            if i == None or type(i) == complex:
                return None
            if type(i) == str:
                i = i.replace('--', '', -1)
            result = calculate(result, float(i), calc_type)
        return result
