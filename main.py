from typing import Callable
from string import ascii_uppercase
from inspect import signature

def get_used_parameters(expression: str) -> set[str]:
    # Iteriert über 'ascii_uppercase' um chars zwischen A und Z zu finden, welche in 'expression' vorhanden sind, gibt diese dann in einem Set zurück
    # In unserem Fall wird nur {"A"} (für NICHT) oder {"A", "B"} (für andere Funktionen) zurückgegeben werden
    return set(char for char in ascii_uppercase if char in expression)


def generate_function(expression: str) -> Callable[..., int]:
    # Ersetzt alle Kleinbuchstaben durch Großbuchstaben
    expression = expression.upper()
    # Entnimmt aus expression die verwendeten Parameter (A, B, ...)
    used_parameters: set[str] = get_used_parameters(expression)
    # Ersetzt die Operatoren ¬, ∧ und ∨ mit dem von Python bekannten Operatoren not, and und or
    parsed_expression: str = expression.replace("¬", " not ").replace("∧", " and ").replace("∨", " or ")
    # Böses Ausnutzen von eval(...) ☹️
    # Erstellt dynamisch mithilfe des Python-Interpreters ein lambda (Funktion) welche die Parameter aus used_parameters aufnimmt und als Funktionskörper parsed_expression hat
    f: Callable[..., int] = eval(f"lambda {','.join(char for char in used_parameters)}: int({parsed_expression})")
    return f

def generate_parameter_table(f: Callable[..., int]) -> list[tuple[int, ...]]:
    count_of_parameters: int = len(signature(f).parameters) # Bestimmt die Anzahl der Parameter der erstellten Funktion f mithilfe Reflektion
    result: list[tuple[int, ...]] = []
    for i in range(pow(2, count_of_parameters)):                            # Iteriert binär über alle Möglichkeiten der Parameterzusammenstellung
        result.append(tuple(arg for arg in map(int,                             # Macht aus dem String eine Liste von ints und wandelt diese in ein Tupel um und fügt diesen 'result' hinzu
                                                   bin(i)                           # Macht aus 'i' ein String
                                                   .removeprefix('0b')              # Löscht den durch bin(i) entstandenen '0b'-prefix 
                                                   .zfill(count_of_parameters)      # Füllt die leeren Plätze vor dem binären String mit Nullen auf
        )))
    return result
        
def print_one_line(f: Callable[..., int], arguments: tuple[int, ...]):
    # Printed eine Zeile im folgenden Format:
    # A|B|C|...->Z
    print(f"{'|'.join(str(argument) for argument in arguments)}->{f(*arguments)}")

def main() -> None:
    # Nimmt als Input eine logische Aussage mit verschiedenen verwendetet Variablen, Parametern, wie
    # ¬((¬(A∧A))∧(¬(B∧B)))
    # in eine Wahrheitstabelle, wie
    # 0|0->0
    # 0|1->1
    # 1|0->1
    # 1|1->1
    inp: str = input("Logische Aussage >> ")
    f: Callable[..., int] = generate_function(inp)
    for arguments in generate_parameter_table(f):
        print_one_line(f, arguments)


if __name__ == '__main__':
    # technische Details. Sorgt dafür dass, wenn diese Datei in eine andere importiert wird, dann der Code nicht sofort ausgeführt wird
    main()