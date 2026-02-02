# Aerocell: Simulador de Propagação de Aerossóis

## Acesse a aplicação

Use o deploy para testar a aplicação diretamente no navegador:
https://aerocell-wnetohr.streamlit.app/

## Visão Geral

Aerocell é um simulador desenvolvido para modelar a propagação de aerossóis em ambientes fechados utilizando conceitos de autômatos celulares. Fornece simulações realistas de como doenças respiratórias se propagam em espaços confinados, ajudando pesquisadores e profissionais a compreender a dinâmica de transmissão e avaliar estratégias de mitigação.

## Descrição do Projeto

Este projeto simula a transmissão de aerossóis em ambientes fechados aproveitando a teoria dos autômatos celulares. Modela a dinâmica espacial e temporal da transmissão de doenças em ambientes internos, permitindo análise dos fatores que influenciam a propagação de doenças respiratórias.

## Características Principais

- **Simulação baseada em Autômatos Celulares** - Modela a propagação de aerossóis usando regras discretas baseadas em grade
- **Modelagem de ambientes fechados** - Simula cenários realistas em ambientes internos
- **Análise de transmissão de doenças** - Rastreia como as doenças respiratórias se propagam através de partículas de aerossol
- **Parâmetros personalizáveis** - Ajuste as condições ambientais e fatores de transmissão

## Como Começar

Siga os passos abaixo para configurar o ambiente e executar o AeroCell em sua máquina local.

#### **Pré-requisitos**
* Python 3.8 ou superior instalado.
* Gerenciador de pacotes `pip`.

#### **Passo a Passo**

1.  **Clone o repositório ou baixe os arquivos:**
    Certifique-se de que os arquivos `main.py`, `engine.py` e `requirements.txt` estejam na mesma pasta.

2.  **Instale as dependências:**
    Abra o terminal na pasta do projeto e execute:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    No terminal, utilize o comando do Streamlit:
    ```bash
    streamlit run main.py
    ```

4.  **Acesse no Navegador:**
    A aplicação abrirá automaticamente em seu navegador padrão no endereço `http://localhost:8501`.
    
## 🧠 Como funciona a Lógica de Difusão?

A propagação de partículas no **AeroCell** não utiliza loops complexos para cada célula, mas sim um modelo matemático de **Autômatos Celulares** baseado na física de fluidos. A ideia central é que o ar tende ao equilíbrio: áreas com alta concentração "doam" partículas para áreas vizinhas com menor concentração.

### A Regra de Transição

A cada passo da simulação (frame), o novo valor de uma célula é calculado pela seguinte fórmula:

$$\phi_{novo} = (\phi_{atual} \cdot (1 - \alpha)) + (\bar{\phi}_{vizinhos} \cdot \alpha)$$

Onde:
* **$\phi_{atual}$**: A quantidade de aerossol que a célula contém no momento.
* **$\alpha$ (Taxa de Difusão)**: Um coeficiente entre 0 e 1 que define a velocidade do espalhamento.
* **$\bar{\phi}_{vizinhos}$**: A média da concentração das células vizinhas (Vizinhança de Von Neumann).

### Na prática, isso significa que:

1.  **Inércia:** Se definirmos a difusão em $0.2$, a célula preserva $80\%$ ($1 - 0.2$) do seu conteúdo atual. Isso representa a resistência da massa de ar ao movimento instantâneo.
2.  **Interação:** A célula absorve $20\%$ da média da concentração ao seu redor. Se os vizinhos estiverem saturados, a célula tende a equalizar sua concentração com eles.
3.  **Realismo Visual:** Este cálculo resulta em uma dissipação radial suave, simulando o comportamento real de gases e vapores em ambientes fechados.

### Otimização com NumPy

Para garantir que a simulação rode em tempo real no **Streamlit**, o AeroCell utiliza **vetorização matricial**. Em vez de iterar sobre cada célula individualmente (o que seria computacionalmente caro em Python), deslocamos a matriz de dados inteira em quatro direções usando a função `np.roll()`. 

Isso permite que o processador execute as operações matemáticas em blocos, garantindo alta performance mesmo em grades de alta resolução.

## 📉 Mecanismo de Decaimento (Decay)

Em uma simulação realista, as partículas de aerossol não permanecem em suspensão eternamente. O **AeroCell** implementa um fator de decaimento para simular fenômenos físicos como a sedimentação (partículas que caem no chão) e a dissipação natural da carga viral no ambiente.

### A Equação de Decaimento

Após o cálculo da difusão, aplicamos uma redução linear na concentração de cada célula através da seguinte fórmula:

$$\phi_{final} = \phi_{novo} \cdot (1 - \delta)$$

Onde:
* **$\phi_{final}$**: O valor final da concentração após todas as perdas do frame.
* **$\phi_{novo}$**: O valor resultante do cálculo de difusão.
* **$\delta$ (Taxa de Decaimento)**: Um coeficiente (geralmente muito pequeno, ex: 0.005) que define o percentual de perda por ciclo.

### Por que o Decaimento é importante?

1.  **Sedimentação:** Partículas de aerossol são influenciadas pela gravidade e, eventualmente, depositam-se em superfícies.
2.  **Inativação Viral:** No contexto de patógenos como o SARS-CoV-2 ou Influenza, o vírus perde sua capacidade infecciosa ao longo do tempo devido a fatores ambientais (umidade, temperatura, radiação UV).
3.  **Estabilidade da Simulação:** Matematicamente, o decaimento evita que a concentração de partículas se acumule infinitamente no sistema, garantindo que o ambiente eventualmente retorne ao estado de "ar limpo" se a fonte de emissão for interrompida.

### Implementação Vetorizada

No código, essa operação é realizada em uma única linha para toda a grade:

```python
self.grid *= (1 - self.decay)

## 🧱 Sistema de Obstáculos e Colisões

Para simular ambientes reais (salas, consultórios ou escritórios), o **AeroCell** utiliza um sistema de máscaras booleanas para definir barreiras físicas. Obstáculos são tratados como regiões de "capacidade zero", onde a concentração de aerossol é nula e a passagem de partículas é bloqueada.

### Lógica de Máscara Matricial

Diferente de sistemas de colisão tradicionais baseados em vetores, o AeroCell utiliza álgebra matricial para aplicar restrições físicas em tempo real:

$$\phi_{final} = \phi_{calculado} \odot (1 - M_{obstáculos})$$

Onde:
* **$M_{obstáculos}$**: Uma matriz binária de mesma dimensão da grade, onde $1$ representa um obstáculo e $0$ representa espaço livre.
* **$\odot$**: Representa o produto de Hadamard (multiplicação elemento a elemento).

### Por que usar máscaras?

1. **Performance:** Permite que o simulador calcule colisões para milhões de células simultaneamente, sem a necessidade de checar cada partícula individualmente.
2. **Complexidade de Cenários:** Com essa abordagem, é possível desenhar qualquer layout de ambiente (paredes, mesas, divisórias) simplesmente alterando os valores da matriz de obstáculos.
3. **Realismo:** As barreiras forçam a "nuvem" de aerossol a contornar objetos, simulando fielmente como o ar se comporta em cantos e corredores estreitos.