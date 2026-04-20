#!/usr/bin/env python3
"""
DevOps Cert Trainer - Treinamento para certificações via Ollama
Otimizado para Termux (Android)
"""

import json
import random
import requests
import sys
import os
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"  # Troque pelo modelo que você tiver instalado

CERTS = {
    "1": "Terraform Associate",
    "2": "GCP Professional DevOps Engineer",
    "3": "AWS DevOps Engineer Professional",
    "4": "CKA - Certified Kubernetes Administrator",
}

CORES = {
    "reset":  "\033[0m",
    "verde":  "\033[92m",
    "vermelho": "\033[91m",
    "amarelo": "\033[93m",
    "azul":   "\033[94m",
    "ciano":  "\033[96m",
    "negrito": "\033[1m",
}

def c(texto, cor):
    return f"{CORES[cor]}{texto}{CORES['reset']}"

# ─── OLLAMA ────────────────────────────────────────────────────────────────────
def gerar_questao(cert, historico_temas=[]):
    temas_vistos = ", ".join(historico_temas[-5:]) if historico_temas else "nenhum"

    prompt = f"""Você é um examinador da certificação {cert}.

Gere UMA questão de múltipla escolha no estilo real do exame.
Evite repetir esses temas recentes: {temas_vistos}

Responda APENAS com JSON válido, sem texto extra, neste formato exato:
{{
  "tema": "nome curto do tema",
  "questao": "texto da pergunta",
  "opcoes": {{
    "A": "texto da opção A",
    "B": "texto da opção B",
    "C": "texto da opção C",
    "D": "texto da opção D"
  }},
  "resposta": "A",
  "explicacao": "explicação detalhada de por que esta é a resposta correta e por que as outras estão erradas"
}}"""

    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }, timeout=60)
        resp.raise_for_status()
        texto = resp.json()["response"].strip()

        # Limpar possível markdown
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        elif "```" in texto:
            texto = texto.split("```")[1].split("```")[0].strip()

        return json.loads(texto)
    except requests.exceptions.ConnectionError:
        print(c("\n❌ Ollama não está rodando. Execute: ollama serve &", "vermelho"))
        sys.exit(1)
    except Exception as e:
        print(c(f"\n⚠️  Erro ao gerar questão: {e}", "amarelo"))
        return None

# ─── UI ────────────────────────────────────────────────────────────────────────
def limpar():
    os.system("clear")

def cabecalho(cert, pontos, total):
    print(c("─" * 45, "azul"))
    print(c(f"  📚 {cert}", "negrito"))
    if total > 0:
        pct = int((pontos / total) * 100)
        cor = "verde" if pct >= 70 else "amarelo" if pct >= 50 else "vermelho"
        print(c(f"  ✅ {pontos}/{total} corretas ({pct}%)", cor))
    print(c("─" * 45, "azul"))
    print()

def exibir_questao(dados, numero):
    print(c(f"Questão {numero}", "ciano") + c(f"  [{dados['tema']}]", "amarelo"))
    print()
    print(dados["questao"])
    print()
    for letra, texto in dados["opcoes"].items():
        print(f"  {c(letra, 'negrito')}) {texto}")
    print()

def pedir_resposta():
    while True:
        resp = input(c("Sua resposta (A/B/C/D) ou 'p' para pular: ", "ciano")).strip().upper()
        if resp in ["A", "B", "C", "D", "P"]:
            return resp
        print(c("  Digite A, B, C, D ou P", "vermelho"))

def mostrar_resultado(dados, resposta_usuario):
    correta = dados["resposta"].upper()
    acertou = resposta_usuario == correta

    print()
    if acertou:
        print(c("✅ CORRETO!", "verde"))
    else:
        print(c(f"❌ ERRADO! A resposta era: {correta}", "vermelho"))

    print()
    print(c("Explicação:", "amarelo"))
    # Quebrar explicação em linhas de ~45 chars para tela pequena
    explicacao = dados["explicacao"]
    palavras = explicacao.split()
    linha = ""
    for palavra in palavras:
        if len(linha) + len(palavra) + 1 > 45:
            print("  " + linha)
            linha = palavra
        else:
            linha = f"{linha} {palavra}".strip()
    if linha:
        print("  " + linha)
    print()

def menu_cert():
    limpar()
    print(c("─" * 45, "azul"))
    print(c("  🎯 DevOps Cert Trainer", "negrito"))
    print(c("─" * 45, "azul"))
    print()
    print("Escolha a certificação:\n")
    for num, nome in CERTS.items():
        print(f"  {c(num, 'ciano')}) {nome}")
    print()
    while True:
        escolha = input(c("Opção: ", "ciano")).strip()
        if escolha in CERTS:
            return CERTS[escolha]
        print(c("  Opção inválida", "vermelho"))

def menu_pos_sessao(pontos, total):
    pct = int((pontos / total) * 100) if total > 0 else 0
    print(c("─" * 45, "azul"))
    print(c("  📊 Resultado da Sessão", "negrito"))
    print(c("─" * 45, "azul"))
    print()
    print(f"  Acertos: {c(str(pontos), 'verde')}/{total}")
    print(f"  Taxa:    {c(str(pct) + '%', 'verde' if pct >= 70 else 'amarelo' if pct >= 50 else 'vermelho')}")
    print()
    if pct >= 70:
        print(c("  🎉 Boa! Acima da média de aprovação.", "verde"))
    elif pct >= 50:
        print(c("  📈 Quase lá. Continue treinando!", "amarelo"))
    else:
        print(c("  💪 Precisa revisar mais. Não desiste!", "vermelho"))
    print()
    print(f"  {c('1', 'ciano')}) Nova sessão")
    print(f"  {c('2', 'ciano')}) Trocar certificação")
    print(f"  {c('3', 'ciano')}) Sair")
    print()

# ─── SESSÃO ────────────────────────────────────────────────────────────────────
def sessao(cert, num_questoes=10):
    pontos = 0
    historico_temas = []

    for i in range(1, num_questoes + 1):
        limpar()
        cabecalho(cert, pontos, i - 1)
        print(c("⏳ Gerando questão...", "amarelo"))

        dados = gerar_questao(cert, historico_temas)
        if not dados:
            print(c("Pulando questão com erro...", "amarelo"))
            continue

        historico_temas.append(dados.get("tema", ""))
        limpar()
        cabecalho(cert, pontos, i - 1)
        exibir_questao(dados, i)

        resposta = pedir_resposta()

        if resposta == "P":
            print(c("\n⏭️  Questão pulada", "amarelo"))
            input(c("\nEnter para continuar...", "ciano"))
            continue

        if resposta == dados["resposta"].upper():
            pontos += 1

        mostrar_resultado(dados, resposta)
        input(c("Enter para continuar...", "ciano"))

    return pontos, num_questoes

# ─── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    cert = menu_cert()

    while True:
        limpar()
        print(c(f"\n  Quantas questões? (padrão: 10)\n", "ciano"))
        qtd_input = input(c("  Quantidade: ", "ciano")).strip()
        try:
            qtd = int(qtd_input) if qtd_input else 10
            qtd = max(1, min(qtd, 30))
            break
        except ValueError:
            pass

    while True:
        pontos, total = sessao(cert, qtd)
        limpar()
        menu_pos_sessao(pontos, total)

        opcao = input(c("Opção: ", "ciano")).strip()
        if opcao == "1":
            continue
        elif opcao == "2":
            cert = menu_cert()
        else:
            limpar()
            print(c("\n  Bons estudos! 🚀\n", "verde"))
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c("\n\n  Até mais! 👋\n", "ciano"))
        sys.exit(0)
