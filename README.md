# pivo-embarcado

Este repositório contém o serviço de visão computacional do pivô PIPE.

* Algoritmo de visão computacional baseado no artigo disponível em:

```https://automaticaddison.com/the-ultimate-guide-to-real-time-lane-detection-using-opencv/```

# Passos para rodar

1. Ter python 3.9 e pip instalados 
2. Navegar para a pasta src
3. rodar o comando `pip install -r requirements.txt`
4. rodar o comando `python subscriber.py`

# Funcionamento

Após seguir os passos acima, o serviço estará esperando eventos mqtt, no momento no broker eqmx. O arquivo publisher.py pode ser usado para testar o serviço, na ausência dos outros sistemas do subsistema de software do PIPE.

O serviço publica continuamente as mensagens `L1` para indicar que o pivô deve virar levemente para a esquerda `R1` para indicar que deve virar levemente para a direita e `L0` para indicar que deve permancecer andando reto.

# Funcionamento do publisher.py

Após rodar o publisher, digitar 1 e enter para iniciar a navegação autônoma e 2 e enter para pará-la.
