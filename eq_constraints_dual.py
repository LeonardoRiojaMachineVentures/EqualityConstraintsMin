from numpy import *
import math

debug = False

class SimplexDual:
    def __init__(self, obj):
        self.obj = array(obj, dtype=float);
        self.rows = []
        self.cons = []
        self.z = 0
        self.orig = []
        self.Borig =[]
 
    def add(self, con, val, symbol):
        self.orig.append(con)
        self.Borig.append(val)
        c = array([con], dtype=float)
        if symbol == '=<':
            self.rows.append(c)
            self.cons.append([val])

        if symbol == '=>':
            self.rows.append(c*-1)
            self.cons.append([val*-1])

        if symbol == '=':
            self.rows.append(c)
            self.rows.append(c*-1)
            self.cons.append([val])
            self.cons.append([val*-1])

    def gen(self):

        self.A = zeros((1,len(self.rows[0][0])))
        for r in self.rows:
            self.A=concatenate((self.A, r), axis=0)
        self.A=delete(self.A,0,0)

        l = len(self.A)
        I = identity(l, dtype=float)
        self.A = concatenate((self.A,I), axis=1)
        self.cons= array(self.cons, dtype=float)

        self.obj.resize(1,len(self.A[1]))

    
    def solve(self):
        if debug:
            print("****************************\nInicial: ")
            print("Matriz A inicial:")
            for r in self.orig:
                print(r)
            print("B Original:", str(self.Borig))
            print("Z: ", str(self.obj))
            self.output()
        rindx = 0
        cindx = 0
        while True:
            # Buscamos en la columna b el valor más negativo
            tmp = 0
            i = 0
            negs = []
            for r in self.cons:
                if tmp > r[0]:
                    tmp = r[-1]
                    minval = tmp
                i = i + 1

            # Si no existen valores negativos en la columna 
            # no tiene solución el sistema
            n = 0
            if debug:
                print(negs)
            for r in self.cons:
                if r != minval:
                    n = n + 1
                    continue
                if debug:
                    print(n, minval)
                rindx = n 
                tmp = -float('Inf')
                if self.A[rindx].min() >= 0:
                    if debug:
                        print(self.A[rindx])
                    n = n + 1
                    continue 

                if debug:
                    print("Sale:", str(self.A[rindx]))

                # Buscamos el valor mínimo en esa columna
                coefs = self.obj / self.A[rindx]
                
                if debug:
                    print("Coefs:", str(coefs[0]))
                i = 0
                for c in coefs[0]:
                    if c>tmp and c= 0:
                if debug:
                    print(self.A[rindx])
                print("Problema no acotado")
                return 0 
            if debug:
                print(self.A[rindx])
             
            m = self.A[rindx][cindx]
            if debug:
                print("Mínimo: " + str(m) + " [" + str(rindx) + ",", str(cindx)+ "]")

            # Convertimos a 1 el elemento pibote 
            self.A[rindx]=self.A[rindx]*float(float(1)/float(m))
            f = float(float(1)/float(m))
            con = float(self.cons[rindx][0])
            self.cons[rindx][0]=f * con

            # Convertimos a 0 los demás elementos en la columna
            for n in range(len(self.A)):
                if n != rindx:
                    thisp = self.A[n][cindx]
                    self.A[n]=self.A[n]-(self.A[rindx]*thisp)
                    self.cons[n][0]=self.cons[n][0]-(self.cons[rindx][0]*thisp)
            thisp2 = self.obj[0][cindx]
            self.obj[0]=self.obj-(self.A[rindx]*thisp2)
            self.z = self.z - (self.cons[rindx][0] * thisp2)

            if debug:
                print("****************************\n")
                self.output()
                input()
            
            #Comprobamos si es una solución óptima
            if self.cons.min() >= 0:
                print("No hay valores negativos en b")
                if debug:
                    print(self.obj)
                if self.obj.min() >= 0:
                    i=0
                    for o in self.cons:
                        i=i+1
                    print("Con Z " + str(self.z))
                    break
                else:                    
                    print("Con Z " + str(-1*self.z))
                    return 0

    def simplex(self):
        pass

    def output(self):
        print(self.A)
        print(self.cons)
        print(self.obj)

if __name__ == "__main__":

    t = SimplexDual(\
            [2, 4,  3,  2,  2,  4,  1,  5, 6])
    #      x12|x14|x24|x32|x34|x45|x47|x56|x76
    t.add([ 1 , 1,  0,  0,  0,  0,  0,  0,  0], 1, '=')
    t.add([-1 , 0,  1, -1,  0,  0,  0,  0,  0], 0, '=')
    t.add([ 0 ,-1, -1,  0, -1,  1,  1,  0,  0], 0, '=')
    t.add([ 0 , 0,  0,  1,  1,  0,  0,  0,  0], 0, '=')
    t.add([ 0 , 0,  0,  0,  0, -1,  0,  1,  0], 0, '=')
    t.add([ 0 , 0,  0,  0,  0,  0, -1,  0,  1], 0, '=')
    t.add([ 0 , 0,  0,  0,  0,  0,  0, -1, -1],-1, '=')
    t.gen()
    t.solve()
