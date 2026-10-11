from services import sys, Path

def obter_pasta_dados():

    # Quando executado como .exe compilado
    if getattr(sys, "frozen", False):

        pasta = Path.home() / "PDV"

    # Durante o desenvolvimento
    else:

        pasta = Path(__file__).resolve().parents[2]

    pasta.mkdir(

        parents=True,

        exist_ok=True

    )

    return pasta


def obter_caminho_config():

    return (

        obter_pasta_dados()

        / "config.json"

    )