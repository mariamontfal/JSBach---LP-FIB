from logging import raiseExceptions
import os
from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
import sys

if __name__ is not None and "." in __name__:
    from .jsbachParser import jsbachParser
    from .jsbachVisitor import jsbachVisitor
else:
    from jsbachParser import jsbachParser
    from jsbachVisitor import jsbachVisitor


class Jsbach(jsbachVisitor):

    def __init__(self):
        self.baseConversion = {
                                'A': 0,
                                'B': 1,
                                'C': 2,
                                'D': 3,
                                'E': 4,
                                'F': 5,
                                'G': 6
                                }
        self.played = []
        self.initialMethod = 'Main'
        self.initialParams = []
        self.stack = []
        self.functions = {}

    def setMethod(self, initial_Method, initial_Params):
        self.initialMethod = initial_Method
        self.initialParams = initial_Params

    def visitRoot(self, ctx):
        funcs = list(ctx.getChildren())
        for func in funcs:
            self.visit(func)
        self.stack.append({})
        n = len(self.initialParams)
        if self.initialMethod not in self.functions.keys():
            raise Exception('JSBachException-> Method ' + self.initialMethod + ' not defined')

        if n != len(self.functions[self.initialMethod][0]):
            raise Exception('JSBachException-> In ' + self.initialMethod + ' expected ' +
                            str(len(self.functions[self.initialMethod][0])) +
                            ' parameter(s) but ' + str(n) + ' instantiated')
        try:
            for i in range(n):
                if self.initialParams[i] == "True" or self.initialParams[i] == "true":
                    self.stack[0][self.functions[self.initialMethod][0][i]] = 1
                elif self.initialParams[i] == "False" or self.initialParams[i] == "false":
                    self.stack[0][self.functions[self.initialMethod][0][i]] = 0
                try:
                    self.stack[0][self.functions[self.initialMethod][0][i]] = int(self.initialParams[i])
                except ValueError:
                    try:
                        self.stack[0][self.functions[self.initialMethod][0][i]] = float(self.initialParams[i])
                    except ValueError:
                        self.stack[0][self.functions[self.initialMethod][0][i]] = self.initialParams[i]
        except:
            raise Exception("JSBachException-> Error with the key")
        self.visit(self.functions[self.initialMethod][1])
        self.stack.pop()

    def visitExprFunc(self, ctx):
        l = list(ctx.getChildren())
        fName = l[0].getText()
        if fName in self.functions.keys():
            raise Exception("JSBachException-> Method "+fName+" already defined")
        if l[len(l)-1].getText() != ':|':
            raise Exception("JSBachException-> Unexpected end of block")
        params = []
        i = 1
        while l[i].getText() != '|:' and i < len(l)-1:
            if l[i].getText() in params:
                raise Exception("JSBachException-> Parameter "+l[i].getText()+" already defined")
            params.append(l[i].getText())
            i = i + 1
        i = i + 1
        self.functions[fName] = [params, l[i]]

    def visitExprFuncInvoke(self, ctx):
        l = list(ctx.getChildren())
        fName = l[0].getText()
        if fName not in self.functions.keys():
            raise Exception('JSBachException-> Method ' + fName + ' not defined')
        llistaValors = []
        i = 1
        while i < len(l):
            llistaValors.append(self.visit(l[i]))
            i = i+1
        n = len(llistaValors)
        if n != len(self.functions[fName][0]):
            raise Exception('JSBachException-> In ' + fName + ' expected ' +
                            str(len(self.functions[fName][0])) +
                            ' parameter(s) but ' + str(n) + ' instantiated')
        self.stack.append({})
        nStack = len(self.stack)
        for i in range(n):
            self.stack[nStack-1][self.functions[fName][0][i]] = llistaValors[i]
        self.visit(self.functions[fName][1])
        self.stack.pop()

    def visitInstructions(self, ctx):
        for instruction in list(ctx.getChildren()):
            self.visit(instruction)

    def visitExprParentesis(self, ctx):
        l = list(ctx.getChildren())
        expr = 0
        for i in range(1, len(l)-1):
            expr = self.visit(l[i]) + expr
        return expr

    def visitExprCondParentesis(self, ctx):
        l = list(ctx.getChildren())
        expr = 0
        for i in range(1, len(l)-1):
            expr = self.visit(l[i]) + expr
        return expr

    def visitExprDivMulMod(self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[0]) is None:
            raise Exception("JSBachException-> First parameter is not defined (None)")
        if self.visit(l[2]) is None:
            raise Exception("JSBachException-> Second parameter is not defined (None)")

        if l[1].getSymbol().type == jsbachParser.DIV:
            if self.visit(l[2]) == 0:
                raise Exception("JSBachException-> Dividing by 0 undetermined")
            return self.visit(l[0])/self.visit(l[2])
        elif l[1].getSymbol().type == jsbachParser.MUL:
            return self.visit(l[0])*self.visit(l[2])
        else:
            return self.visit(l[0]) % self.visit(l[2])

    def visitExprSubAdd(self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[0]) is None:
            raise Exception("JSBachException-> First parameter is not defined (None)")
        if self.visit(l[2]) is None:
            raise Exception("JSBachException-> Second parameter is not defined (None)")
        else:
            if l[1].getSymbol().type == jsbachParser.SUB:
                return self.visit(l[0])-self.visit(l[2])
            elif l[1].getSymbol().type == jsbachParser.ADD:
                return self.visit(l[0])+self.visit(l[2])
            else:
                Exception("JSBachException-> Arithmetic operator unexpected")

    def visitExprLessGreater(self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[0]) is None:
            raise Exception("JSBachException-> First parameter is not defined (None)")
        if self.visit(l[2]) is None:
            raise Exception("JSBachException-> Second parameter is not defined (None)")
        if l[1].getSymbol().type == jsbachParser.LT:
            return self.visit(l[0]) < self.visit(l[2])
        elif l[1].getSymbol().type == jsbachParser.GT:
            return self.visit(l[0]) > self.visit(l[2])
        elif l[1].getSymbol().type == jsbachParser.LE:
            return self.visit(l[0]) <= self.visit(l[2])
        elif l[1].getSymbol().type == jsbachParser.GE:
            return self.visit(l[0]) >= self.visit(l[2])
        else:
            raise Exception("JSBachException-> Boolean operator unexpected")

    def visitExprEqDiff(self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[0]) is None:
            raise Exception("JSBachException-> First parameter is not defined (None)")
        if self.visit(l[2]) is None:
            raise Exception("JSBachException-> Second parameter is not defined (None)")
        if l[1].getSymbol().type == jsbachParser.EQ:
            return self.visit(l[0]) == self.visit(l[2])
        elif l[1].getSymbol().type == jsbachParser.DIFF:
            return self.visit(l[0]) != self.visit(l[2])
        else:
            raise Exception("JSBachException-> Boolean operator unexpected")

    def visitExprWrite(self, ctx):
        l = list(ctx.getChildren())
        for i in range(1, len(l)):
            if i != 1:
                print(' ' + str(self.visit(l[i])), end="")
            else:
                print(str(self.visit(l[i])), end="")
        print()

    def visitExprRead(self, ctx):
        l = list(ctx.getChildren())
        i = input()
        n = len(self.stack)-1
        if i == "True" or i == "true":
            self.stack[n][l[1].getText()] = 1
        elif i == "False" or i == "false":
            self.stack[n][l[1].getText()] = 0
        try:
            self.stack[n][l[1].getText()] = int(i)
        except ValueError:
            try:
                self.stack[n][l[1].getText()] = float(i)
            except ValueError:
                self.stack[n][l[1].getText()] = i

    def getPlayed(self):
        return self.played

    def visitExprPlay(self, ctx):
        l = list(ctx.getChildren())
        for nota in l[1:]:
            if isinstance(self.visit(nota), list):
                for notaArr in self.visit(nota):
                    self.played.append(notaArr)
            else:
                self.played.append(self.visit(nota))

    def assigList(self, llista, valor):
        n = len(self.stack)-1
        if llista.getText() in self.stack[n]:
            while len(self.stack[n][llista.getText()]) > 0:
                self.stack[n][llista.getText()].pop()
            for i in self.visit(valor):
                self.stack[n][llista.getText()].append(i)
        else:
            self.stack[n][llista.getText()] = self.visit(valor)

    def visitExprAssig(self, ctx):
        l = list(ctx.getChildren())
        n = len(self.stack)-1
        if isinstance(self.visit(l[2]), list):
            self.assigList(l[0], l[2])
        else:
            i = self.visit(l[2])
            if i == "True" or i == "true":
                self.stack[n][l[0].getText()] = 1
            elif i == "False" or i == "false":
                self.stack[n][l[0].getText()] = 0
            try:
                self.stack[n][l[0].getText()] = int(i)
            except ValueError:
                try:
                    self.stack[n][l[0].getText()] = float(i)
                except ValueError:
                    self.stack[n][l[0].getText()] = i
                self.stack[n][l[0].getText()] = self.visit(l[2])

    def visitExprLenList(self, ctx):
        l = list(ctx.getChildren())
        n = len(self.stack)-1
        if isinstance(self.stack[n][l[1].getText()], list):
            return len(self.stack[n][l[1].getText()])
        else:
            raise Exception("JSBachException-> Not possible to apply lenght into a " +
                            str(self.stack[n][l[1].getText()]))

    def visitExprPush(self, ctx):
        l = list(ctx.getChildren())
        n = len(self.stack)-1
        self.stack[n][l[0].getText()].append(self.visit(l[2]))

    def visitExprPop(self, ctx):
        l = list(ctx.getChildren())
        n = len(self.stack)-1
        self.stack[n][l[1].getText()].pop(self.visit(l[3])-1)

    def visitExprIndex(self, ctx):
        l = list(ctx.getChildren())
        n = len(self.stack)-1
        try:
            return self.stack[n][l[0].getText()][self.visit(l[2])-1]
        except:
            raise Exception("JSBachException-> Index out of bounds")

    def visitExprVar(self, ctx):
        l = list(ctx.getChildren())
        n = len(self.stack)-1
        return self.stack[n][l[0].getText()]

    def visitExprList(self, ctx):
        l = list(ctx.getChildren())
        lVar = []
        for i in l[1:len(l)-1]:
            lVar.append(self.visit(i))
        return lVar

    def visitExprNum(self, ctx):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    def visitExprString(self, ctx):
        l = list(ctx.getChildren())
        return l[0].getText()[1:len(l[0].getText())-1]

    def visitExprFlo(self, ctx):
        l = list(ctx.getChildren())
        return float(l[0].getText())

    def visitExprBoolVar(self, ctx):
        l = list(ctx.getChildren())
        if l[0].getText() == "true":
            return True
        else:
            return False

    def visitExprNota(self, ctx):
        l = list(ctx.getChildren())
        b = self.baseConversion[l[0].getText()[0]]
        if len(l[0].getText()) > 1:
            escalar = int(l[0].getText()[1])
            if l[0].getText()[0] == 'A' or l[0].getText()[0] == 'B':
                return b + 7*escalar
            else:
                return b + 7*(escalar-1)
        else:
            if l[0].getText() == 'A' or l[0].getText()[0] == 'B':
                return b + 7*5
            else:
                return b + 7*4

    def intToNota(self, notaInt):
        b = notaInt % 7
        escalar = int(notaInt/7)
        nota = list(self.baseConversion.keys())[list(self.baseConversion.values()).index(b)]
        if nota != 'A' and nota != 'B':
            escalar = escalar + 1
        nota = nota + str(escalar)
        return nota

    def notaToLily(self, nota):
        notaL = nota[0].lower()
        notaI = int(nota[1])
        if notaI > 4:
            mul = notaI - 4
            notaL = notaL + mul*("'")
        else:
            mul = 4 - notaI
            notaL = notaL + mul*(",")
        return notaL

    def visitExprConditBool(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) > 0

    def visitExprBool(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[0])

    def visitExprIf(self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[1]):
            for i in range(3, len(l)-1):
                if l[i].getText() == ':|':
                    break
                self.visit(l[i])
            return True
        else:
            return False

    def visitExprIfElse(self, ctx):
        l = list(ctx.getChildren())
        if self.visitExprIf(ctx):
            return None
        else:
            i = 0
            while l[i].getText() != 'else':
                i = i + 1
            for el in l[i+1:len(l)-1]:
                self.visit(el)

    def visitExprWhile(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[0])

    def visitExprLoop(self, ctx):
        l = list(ctx.getChildren())

        while self.visit(l[1]):
            for i in range(3, len(l)):
                if l[i].getText() == ':|':
                    break
                self.visit(l[i])


def createMusic(evaluated):
    notesPlayed = evaluated.getPlayed()
    lilyNotes = ""
    for note in notesPlayed:
        lilyNotes = lilyNotes + str(evaluated.notaToLily(evaluated.intToNota(note))) + " "
    lilyNotes = lilyNotes + "\n"

    if len(notesPlayed) == 0:
        print("\nProgram without music played")
        return

    try:
        os.system('rm bac.*')
    except:
        ('The system cannot erase the files bac.*')

    head = '\\version "2.22.1" \n \\score {\n \\absolute {\n \\tempo 4 = 120'
    tail = '} \n \\layout { } \n \\midi { } \n}'
    bac = head + lilyNotes + tail
    with open("bac.lily", 'w') as f:
        f.write(bac)
        print(bac)

    os.system("lilypond bac.lily")
    os.system("timidity -Ow -o bac.wav bac.midi")
    os.system("ffmpeg -i bac.wav -codec:a libmp3lame -qscale:a 2 bac.mp3")
    os.system("afplay bac.mp3")
    try:
        os.system('rm bac.lily')
    except:
        ('The system cannot erase the file bac.lily')


input_stream = FileStream(sys.argv[1], encoding='utf-8')
lexer = jsbachLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = jsbachParser(token_stream)
tree = parser.root()

evaluated = Jsbach()
if len(sys.argv) > 2:
    evaluated.setMethod(sys.argv[2], sys.argv[3:])
evaluated.visit(tree)

print("\nComputation finished, please, press any key to generate music files", end="")
input()
createMusic(evaluated)
