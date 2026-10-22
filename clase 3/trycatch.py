def division(a:float, b:float):
    resultado:float
    try:
        resultado = a/b
    except ZeroDivisionError:
        print('No se puede dividir por cero')
    except Exception as e:
        print(f'Error ineseperado: {e}')
    else: 
        print(resultado)
    finally:
        print('Esto se ejecuta siempre')

division(5, 'hola')