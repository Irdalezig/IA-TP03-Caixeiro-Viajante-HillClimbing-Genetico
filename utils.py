# utils.py
import time
import matplotlib.pyplot as plt
import os

os.makedirs("resultados", exist_ok=True)

def cronometrar(f):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = f(*args, **kwargs)
        fim = time.time()
        tempo = fim - inicio
        print(f"{f.__name__}: {tempo:.4f}s")
        if isinstance(resultado, tuple):
            return resultado + (tempo,)
        else:
            return resultado, tempo
    return wrapper

def salvar_grafico(nome):
    plt.savefig(f"resultados/{nome}.png", dpi=300, bbox_inches='tight')
    plt.close()