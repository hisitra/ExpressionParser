import math
import cmath

class Expression:

    __signs = ["^", "/", "*", "-", "+"]
    __functions = ["si", "co", "ta", "as", "ac", "at", "lo", "ln"]
    __numbers = [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    __functionsDict = {"sin" : cmath.sin, "asin" : cmath.asin, "sinh" : cmath.sinh, "asinh" : cmath.asinh,
                       "cos" : cmath.cos, "acos" : cmath.acos, "cosh" : cmath.cosh, "acosh" : cmath.acosh,
                       "tan" : cmath.tan, "atan" : cmath.atan, "tanh" : cmath.tanh, "atanh" : cmath.atanh,
                       "log" : cmath.log10, "ln" : cmath.log}

    def __init__(self, exp):

        exp.insert(0, "(")
        exp.append(")")
        self.__exp = exp
        self.__valueAtIndex = [None] * len(self.__exp)
        self.__endPointOf = [None] * len(self.__exp)
        self.__assignConstants()



    def toString(self):
        return ''.join(self.__exp)



    def __assignConstants(self):

        abb = self.__exp

        i = 0

        while i < len(abb):
            
            if abb[i] == "e":

                self.__valueAtIndex[i] = math.e * (1 + 0j)
                self.__endPointOf[i] = i

            if abb[i] == "i":

                self.__valueAtIndex[i] = 0 + 1j
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
                self.__valueAtIndex[i] = self.__valueAtIndex[openBracketIndices[-1]]
                self.__endPointOf[openBracketIndices[-1]] = i
                self.__endPointOf[i] = openBracketIndices[-1]
                del openBracketIndices[-1]

##        print()
##        print(self.__valueAtIndex)
##        print(self.__endPointOf)


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
                        self.__valueAtIndex[i] = Expression.__functionsDict[''.join(abb)[i : x]](self.__valueAtIndex[x])
                        self.__valueAtIndex[self.__endPointOf[x]] = self.__valueAtIndex[i]
                        self.__endPointOf[i] = self.__endPointOf[x]
                        self.__endPointOf[self.__endPointOf[x]] = i

            i += 1

        for sign in Expression.__signs:
            i = start
            while i < end:

                if abb[i] == "(":
                    i = self.__endPointOf[i]
                    continue

                if abb[i] == sign:
##                    print(sign, self.__valueAtIndex[i - 1], self.__valueAtIndex[i + 1])
                    state = True
                    if sign == "^":
                        self.__valueAtIndex[self.__endPointOf[i - 1]] = self.__valueAtIndex[i - 1] ** self.__valueAtIndex[i + 1]

                    elif sign == "/":
                        self.__valueAtIndex[self.__endPointOf[i - 1]] = self.__va
                        lueAtIndex[i - 1] / self.__valueAtIndex[i + 1]

                    elif sign == "*":
                        self.__valueAtIndex[self.__endPointOf[i - 1]] = self.__valueAtIndex[i - 1] * self.__valueAtIndex[i + 1]

                    elif sign == "-":
                        if abb[i - 1] == "(":
                            self.__valueAtIndex[i] = self.__valueAtIndex[i + 1] * -1
                            self.__valueAtIndex[self.__endPointOf[i + 1]] = self.__valueAtIndex[i]
                            self.__endPointOf[i] = self.__endPointOf[i + 1]
                            self.__endPointOf[self.__endPointOf[i + 1]] = i
                            state = False
                        else:
                            self.__valueAtIndex[self.__endPointOf[i - 1]] = self.__valueAtIndex[i - 1] - self.__valueAtIndex[i + 1]

                    elif sign == "+":
                        self.__valueAtIndex[self.__endPointOf[i - 1]] = self.__valueAtIndex[i - 1] + self.__valueAtIndex[i + 1]

                    if state:
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

##        print("retured")

        return self.__valueAtIndex[start]
                        
                

while True:                
    expression = Expression(list(input("Expression: ")))
    print(expression.valueAtPoint(1))
