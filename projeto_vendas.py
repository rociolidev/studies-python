import pandas as pd

# Um dicionário: cada chave vira uma coluna, cada lista são os valores dela
dados = {
    "data": ["2026-10-01", "2026-10-02", "2026-10-02", "2026-10-03", "2026-10-04",
             "2026-10-05", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08"],
    "produto": ["Mouse", "Teclado", "Monitor", "mouse", "Notebook",
                "Teclado", "Monitor", "Mouse", "Notebook", "Teclado"],
    "categoria": ["Acessórios", "Acessórios", "Telas", "Acessórios", "Computadores",
                  "Acessórios", "Telas", "Acessórios", "Computadores", "Acessórios"],
    "quantidade": [3, 2, 1, 4, 1, None, 2, 5, 1, 3],
    "preco_unitario": [50.0, 120.0, 900.0, 50.0, 3500.0,
                       120.0, 900.0, 50.0, 3500.0, 120.0],
}

# Transforma o dicionário em uma tabela (DataFrame)
vendas = pd.DataFrame(dados)

print(vendas)
print()
print("Linhas e colunas:", vendas.shape)
print()
vendas.info()
print("\n--- Verificando valores ausentes por coluna ---")
print(vendas.isna().sum())

print("\n--- Produtos únicos antes da correção ---")
print(vendas["produto"].unique())

# Padroniza: remove espaços extras e deixa a primeira letra maiúscula
vendas["produto"] = vendas["produto"].str.strip().str.capitalize()

print("\n--- Produtos únicos depois da correção ---")
print(vendas["produto"].unique())
print("\n--- Linha(s) com quantidade ausente ---")
ausentes = vendas[vendas["quantidade"].isna()]
print(ausentes)

print("\n--- Outras vendas de Teclado, para comparar ---")
teclados = vendas[vendas["produto"] == "Teclado"]
print(teclados)
# Cria a coluna de receita (NaN x preço continua NaN)
vendas["receita"] = vendas["quantidade"] * vendas["preco_unitario"]

# Sinaliza as linhas com quantidade não informada
vendas["quantidade_informada"] = vendas["quantidade"].notna()

print("\n--- Tabela com receita e sinalização ---")
print(vendas)

# sum() do Pandas ignora NaN por padrão
receita_total = vendas["receita"].sum()
print("\nReceita total (ignorando a linha sem quantidade):", receita_total)

# Cenários para a venda desconhecida: 2 e 3 unidades de Teclado
preco_teclado = 120.0
print("Se a venda ausente fosse de 2 unidades:", receita_total + 2 * preco_teclado)
print("Se a venda ausente fosse de 3 unidades:", receita_total + 3 * preco_teclado)
print("\n--- Receita por produto ---")
receita_produto = vendas.groupby("produto")["receita"].sum().sort_values(ascending=False)
print(receita_produto)

print("\n--- Receita por categoria ---")
receita_categoria = vendas.groupby("categoria")["receita"].sum().sort_values(ascending=False)
print(receita_categoria)

print("\n--- Quantidade vendida por produto ---")
print(vendas.groupby("produto")["quantidade"].sum())

print("\n--- Ticket médio por venda (linhas com receita conhecida) ---")
print(vendas["receita"].mean())
import matplotlib.pyplot as plt

# Gráfico 1: receita por produto (barras)
plt.figure(figsize=(8, 5))
receita_produto.plot(kind="bar", color="steelblue")
plt.title("Receita por produto (outubro/2026)")
plt.xlabel("Produto")
plt.ylabel("Receita (R$)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_receita_produto.png")
plt.close()

# Gráfico 2: receita por categoria (barras)
plt.figure(figsize=(8, 5))
receita_categoria.plot(kind="bar", color="seagreen")
plt.title("Receita por categoria (outubro/2026)")
plt.xlabel("Categoria")
plt.ylabel("Receita (R$)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_receita_categoria.png")
plt.close()

print("\nGráficos salvos na pasta do projeto.")
conclusoes = f"""CONCLUSÕES - Vendas de outubro/2026

Receita total (linhas com quantidade conhecida): R$ {receita_total:.2f}
Produto com maior receita: {receita_produto.index[0]} (R$ {receita_produto.iloc[0]:.2f})
Categoria com maior receita: {receita_categoria.index[0]}
Ticket médio por venda: R$ {vendas["receita"].mean():.2f}

Observações:
- O Mouse lidera em unidades vendidas, mas não em receita.
- Uma venda de Teclado (05/10) está sem quantidade e ficou fora dos totais.
- O impacto estimado dessa venda é de 240 a 360 reais (cerca de 2% do total).
"""

with open("conclusoes.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(conclusoes)

print("\nConclusões salvas em conclusoes.txt")