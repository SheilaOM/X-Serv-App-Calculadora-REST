#!/usr/bin/python3
"""
CALCULADORA SIMPLE VERSIÓN REST
Versión en que el usuario en primer lugar tiene que enviar un POST/create, en el
que se devolverá un número identificador del navegador. A continuación, el
usuario podrá hacer un PUT añadiendo como recurso el identificador dado y como
cuerpo la operación que quiere realizar (con formato operando1,operando2,operador)
Si el usuario quiere ver el resultado de la operación, deberá enviar un GET
con el recurso de su identificador. Si se envia un DELETE, se eliminará la
operación guardada del identificador que se haya pasado como recurso.
"""

import webapp
import random

class calc (webapp.webApp):

    nav = {}

    def parse(self, request):
        metodo = request.split(' ')[0]
        recurso = request.split(' ')[1][1:]
        cuerpo = request.split('\n')[-1]
        return (metodo, recurso, cuerpo)

    def process(self, parsed):
        metodo = parsed[0]
        recurso = parsed[1]
        cuerpo = parsed[2]
        print("met: " + metodo + ", recu: " + recurso)

        if metodo == "POST":
            if recurso == "create":
                id = str(random.randint(0,1000000000))
                self.nav[id] = [None, None, None]
                httpCode = "HTTP/1.1 200 OK"
                htmlBody = "<html><body>El código de tu navegador es: " +\
                           id + "</html></body>"
            else:
                httpCode = "HTTP/1.1 404 Not Found"
                htmlBody = "<html><body>Recurso no encontrado" +\
                           "</html></body>"

        elif metodo == "PUT":
            if recurso in self.nav:
                op1 = cuerpo.split(',')[0]
                op2 = cuerpo.split(',')[1]
                op = cuerpo.split(',')[-1]

                self.nav[recurso] = [op1, op2, op]
                httpCode = "HTTP/1.1 200 OK"
                htmlBody = "<html><body>Me has pedido: " + op1 + op + op2+\
                            "</html></body>"
            else:
                httpCode = "HTTP/1.1 404 Not Found"
                htmlBody = "<html><body>Recurso no encontrado" +\
                           "</html></body>"

        elif metodo == "GET":
            if recurso in self.nav:
                op1 = self.nav[recurso][0]
                op2 = self.nav[recurso][1]
                op = self.nav[recurso][2]
                if op == '+':
                    res = int(op1) + int(op2)
                elif op == '-':
                    res = int(op1)-int(op2)
                elif op == "*":
                    res = int(op1)*int(op2)
                elif op == "/":
                    try:
                        res = int(op1)/int(op2)
                    except ZeroDivisionError:
                        httpCode = "HTTP/1.1 200 OK"
                        htmlBody = "<html><body>Error: división entre 0" +\
                                   "</html></body>"
                        return (httpCode, htmlBody)

                httpCode = "HTTP/1.1 200 OK"
                htmlBody = "<html><body>" + op1 + op + op2 + "=" + str(res) +\
                           "</html></body>"


            else:
                httpCode = "HTTP/1.1 404 Not Found"
                htmlBody = "<html><body>Recurso no encontrado" +\
                           "</html></body>"

        elif metodo == "DELETE":
            del self.nav[recurso]
            httpCode = "HTTP/1.1 200 OK"
            htmlBody = "<html><body>Operación eliminada</html></body>"

        else:
            httpCode = "HTTP/1.1 403 Access Denied"
            htmlBody = "<html><body>Access Denied" +\
                        "</body></html>"


        return (httpCode, htmlBody)

if __name__ == "__main__":
    testWebApp = calc("localhost", 1234)
