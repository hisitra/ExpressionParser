import math
import cmath

class CustomSyntaxError(Exception):
    pass

class Expression:

    __signs = {"^" : lambda a, b : a ** b, "/" : lambda a, b : a / b, "*" : lambda a, b : a * b, "-" : lambda a, b : a - b, "+" : lambda a, b : a + b}
    __functions = ("si", "co", "ta", "as", "ac", "at", "lo", "ln")
    __numbers = (".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    __constants = {"e" : math.e, "i" : 1j}
    __allowedCharacters = {"s", "i", "n", "c", "o", "t", "a", "h", "l", "g", "x", "i", "e", "(", ")"}.union(set(__numbers)).union(set(__signs))
    __functionsDict = {"sin" : cmath.sin, "asin" : cmath.asin, "sinh" : cmath.sinh, "asinh" : cmath.asinh,
                       "cos" : cmath.cos, "acos" : cmath.acos, "cosh" : cmath.cosh, "acosh" : cmath.acosh,
                       "tan" : cmath.tan, "atan" : cmath.atan, "tanh" : cmath.tanh, "atanh" : cmath.atanh,
                       "log" : cmath.log10, "ln" : cmath.log}


    def __init__(self, exp):

        try :
            self.__exp = self.__correctSyntax(["("] + list(exp.lower()) + [")"])
            self.__valueAtIndex = [None] * len(self.__exp)
            self.__endPointOf = [None] * len(self.__exp)
            self.__assignConstants()

        except CustomSyntaxError:
            print("Check syntax")
            


    def toString(self):
        return ''.join(self.__exp)


    def __correctSyntax(self, exp):
        for i in range(len(exp)):
            if exp[i] not in Expression.__allowedCharacters:
                raise CustomSyntaxError("Check expression syntax")
            if exp[i] == "(" and exp[i + 1] == "-":
                exp.insert(i + 1, "0")
        return exp


    def __assignConstants(self):

        abb = self.__exp
        i = 0
        while i < len(abb):
            if abb[i] in Expression.__constants.keys():
                self.__valueAtIndex[i] = Expression.__constants[abb[i]]
                self.__endPointOf[i] = i
                
            if abb[i] in Expression.__numbers:
                number = ""
                startingOfNumber = i
                while abb[i] in Expression.__numbers:
                    number += abb[i]
                    i += 1
                i -= 1
                endingOfNumber = i
                self.__valueAtIndex[startingOfNumber] = float(number)
                self.__valueAtIndex[endingOfNumber] = float(number)
                self.__endPointOf[startingOfNumber] = endingOfNumber
                self.__endPointOf[endingOfNumber] = startingOfNumber

            i += 1

        

    def valueAtPoint(self, point):

        abb = self.__exp
        for i in range(len(abb)):
            if abb[i] == "x":
                self.__valueAtIndex[i] = point
                self.__endPointOf[i] = i

        openBracketIndices = []
        for i in range(len(abb)):
            if abb[i] == "(":
                openBracketIndices.append(i)

            elif abb[i] == ")":
                self.__valueAtIndex[openBracketIndices[-1]] = self.__expressionParser(openBracketIndices[-1] + 1, i, point)
                if (self.__valueAtIndex[openBracketIndices[-1]]) == None:
                    return None
                self.__valueAtIndex[i] = self.__valueAtIndex[openBracketIndices[-1]]
                self.__endPointOf[openBracketIndices[-1]] = i
                self.__endPointOf[i] = openBracketIndices[-1]
                del openBracketIndices[-1]

        return self.__valueAtIndex[0]


    def __expressionParser(self, start, end, point):

        abb = self.__exp
        i = start
        while i < end:
            if abb[i] == "(":
                i = self.__endPointOf[i]
                continue

            if abb[i] + abb[i + 1] in Expression.__functions:
                for x in range(i, end):
                    if abb[x] == "(":
                        try :
                            self.__valueAtIndex[i] = Expression.__functionsDict[''.join(abb)[i : x]](self.__valueAtIndex[x])
                        except ValueError:
                            return None
                        except OverflowError:
                            return None
                        except ZeroDivisionError:
                            return None
                    
                        self.__valueAtIndex[self.__endPointOf[x]] = self.__valueAtIndex[i]
                        self.__endPointOf[i] = self.__endPointOf[x]
                        self.__endPointOf[self.__endPointOf[x]] = i
                        i = x
                        break

            i += 1

        for sign in Expression.__signs:
            i = start
            while i < end:
                if abb[i] == "(":
                    i = self.__endPointOf[i]
                    continue

                if abb[i] == sign:
                    try :
                        self.__valueAtIndex[self.__endPointOf[i - 1]] = self.__signs[abb[i]](self.__valueAtIndex[i - 1], self.__valueAtIndex[i + 1])
                    except ZeroDivisionError:
                        return None
                    except OverflowError:
                        return None
                    except ValueError:
                            return None
                        
                    self.__valueAtIndex[self.__endPointOf[i + 1]] = self.__valueAtIndex[self.__endPointOf[i - 1]]
                    self.__endPointOf[self.__endPointOf[i - 1]] = self.__endPointOf[i + 1]
                    if self.__endPointOf[i - 1] == self.__endPointOf[i + 1]:
                        self.__endPointOf[self.__endPointOf[i + 1]] = i - 1
                    else:
                        self.__endPointOf[self.__endPointOf[i + 1]] = self.__endPointOf[i - 1]

##                        print("val[",self.__endPointOf[i + 1],"] = ", self.__valueAtIndex[self.__endPointOf[i + 1]])
##                        print("val[",self.__endPointOf[self.__endPointOf[i + 1]],"] = ", self.__valueAtIndex[self.__endPointOf[self.__endPointOf[i + 1]]])
##                        print("endPointOf[",self.__endPointOf[i - 1],"] = ", self.__endPointOf[self.__endPointOf[i - 1]])
##                        print("endPointOf[",self.__endPointOf[i + 1],"] = ", self.__endPointOf[self.__endPointOf[i + 1]])
                i += 1

        return self.__valueAtIndex[start]
                        
                
exp = input("Enter:")
expression = Expression(exp)
print(expression.valueAtPoint(2))
