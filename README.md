# 🎯 DevOps Cert Trainer

> LLM local rodando no Android via Termux. Gera questões no estilo real dos exames de certificação — sem internet, sem custo por token.

![Python](https://img.shields.io/badge/Python-3.10+-4d9fff?style=flat-square&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-0.21+-00ff88?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Android%20%2F%20Termux-ffb800?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-white?style=flat-square)

---

## 📋 Sobre

Script Python CLI que usa o **Ollama** para gerar questões de múltipla escolha no estilo real dos exames de certificação DevOps. Funciona 100% offline no Android via Termux.

**Certificações suportadas:**
- Terraform Associate (HashiCorp)
- GCP Professional DevOps Engineer
- AWS DevOps Engineer Professional
- CKA — Certified Kubernetes Administrator

---

## ⚙️ Requisitos

| Item | Mínimo |
|------|--------|
| Android | 10+ |
| Termux | F-Droid (não Play Store) |
| RAM | 4GB (8GB+ recomendado) |
| Espaço livre | ~3GB |
| Python | 3.10+ |

---

## 🚀 Instalação

### 1. Instalar o Termux

Baixe pela **F-Droid** (a versão da Play Store está desatualizada):
👉 https://f-droid.org → buscar "Termux"

```bash
pkg update && pkg upgrade -y
pkg install python python-pip curl git -y
```

### 2. Instalar o Ollama

```bash
pkg install ollama -y

# Verificar
ollama --version
```

### 3. Baixar um modelo LLM

| Modelo | Tamanho | RAM | Indicado para |
|--------|---------|-----|---------------|
| `llama3.2:3b` | ~2GB | 4GB+ | Dispositivos com pouca RAM |
| `qwen2.5:7b` | ~4.5GB | 8GB+ | Melhor qualidade geral |
| `deepseek-r1:7b` | ~4.5GB | 8GB+ | Raciocínio lógico |

```bash
# Recomendado para 8GB+ RAM
ollama pull llama3.2:3b
```

### 4. Instalar o script

```bash
mkdir ~/estudos && cd ~/estudos

# Baixar
curl -O https://github.com/yagothadeu25/cert-trainer
# Instalar dependência
pip install requests

# Ajustar modelo (se necessário)
sed -i 's/qwen2.5:7b/llama3.2:3b/' cert_trainer.py
```

### 5. Rodar

Abra **duas sessões** no Termux (deslize da esquerda para criar nova aba):

```bash
# Sessão 1 — iniciar Ollama
ollama serve

# Sessão 2 — rodar o trainer
cd ~/estudos && python cert_trainer.py
```

---

## 🖥️ Como usar

```
─────────────────────────────────────────────
  🎯 DevOps Cert Trainer
─────────────────────────────────────────────

  1) Terraform Associate
  2) GCP Professional DevOps Engineer
  3) AWS DevOps Engineer Professional
  4) CKA - Certified Kubernetes Administrator

Opção: _
```

1. Escolha a certificação
2. Defina o número de questões (padrão: 10)
3. Responda A / B / C / D — ou `p` para pular
4. Veja a explicação detalhada de cada resposta
5. Acompanhe seu score no topo da tela

---

## 🛠️ Configuração

Edite as variáveis no topo do `cert_trainer.py`:

```python
MODEL = "llama3.2:3b"        # modelo instalado no Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"  # padrão
```

---

## 🔧 Troubleshooting

**Ollama não está rodando**
```bash
ollama serve &
sleep 3 && curl http://localhost:11434
```

**Modelo não encontrado**
```bash
ollama list          # ver modelos instalados
ollama pull llama3.2:3b
```

**Erro de conexão no script**
```bash
# Testar API manualmente
curl http://localhost:11434/api/generate \
  -d '{"model":"llama3.2:3b","prompt":"oi","stream":false}'
```

---

## 📁 Estrutura

```
estudos/
├── cert_trainer.py   # script principal
└── README.md         # este arquivo
```

---

## 📄 Licença

MIT — use, modifique e distribua à vontade.

---

<p align="center">
  feito por <strong>mtsdevops</strong> •
  <a href="https://linkedin.com/in/mtsdevops">LinkedIn</a> •
  <a href="https://hackerone.com/mtsdevops">HackerOne</a>
</p>
