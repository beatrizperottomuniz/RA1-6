'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1 6
'''
from decimal import Decimal, ROUND_HALF_EVEN
import math

def exibirResultados(resultados: list) -> None:
    print("\n------ Resultados esperados ------")
    for i, valor in enumerate(resultados):
        print(f"Linha {i + 1}: {formatar(valor)}")
    print("-----------------------------------")

# para IEEE754 -> roundTiesToEven
def formatar(valor):
    if math.isclose(valor, round(valor)):
        return str(int(round(valor)))
    
    return str(
        Decimal(str(valor)).quantize(
            Decimal("1.0"),
            rounding=ROUND_HALF_EVEN
        )
    )