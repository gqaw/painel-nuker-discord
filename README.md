# painel-nuker-discord
Bot de nuker em painel, discord.

# requesitos pra rodar o código 


Este código foi desenvolvido para rodar um bot do Discord, realizando ações de "nuking" no servidor. Para executar o código, você precisa dos seguintes requisitos:
1. Python

O código foi desenvolvido utilizando o Python 3.8 ou superior. Você pode verificar a versão do Python instalada no seu sistema com o seguinte comando:

python --version

Caso não tenha o Python instalado, você pode baixá-lo no site oficial: Python.org.
2. Bibliotecas Python

Este código usa algumas bibliotecas externas. Para instalar as dependências necessárias, você deve criar um ambiente virtual (recomendado) e instalar as bibliotecas com o pip.
Passo a passo para instalação das dependências:

    Crie um ambiente virtual (opcional, mas recomendado):

python -m venv venv

Ative o ambiente virtual:

    Windows:

.\venv\Scripts\activate

Linux/macOS:

    source venv/bin/activate

Instale as dependências usando o pip:

pip install -r requirements.txt

Ou se você não tem o requirements.txt, pode instalar manualmente com o seguinte comando:

    pip install discord.py colorama

Bibliotecas necessárias:

    discord.py: Para interação com a API do Discord.

    colorama: Para colorir o texto no terminal.

3. Token do Bot

Para que o bot funcione, você precisa de um token de bot válido do Discord. Para obter o token, siga estas etapas:

    Acesse o Portal de Desenvolvedores do Discord.

    Crie uma nova aplicação ou use uma aplicação existente.

    Vá até a seção Bot e gere um token.

    Insira o token gerado no código ou forneça-o ao rodar o script quando solicitado.

4. Permissões do Bot

Certifique-se de que o bot tenha as permissões necessárias para realizar as ações de "nuking" no servidor. Isso inclui permissões para deletar canais, banir membros, criar canais e editar o nome do servidor, entre outras.
