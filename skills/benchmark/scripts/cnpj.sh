#!/usr/bin/env bash
# Uso: cnpj.sh 29200424000181 [outro_cnpj ...]
# Consulta a Receita via BrasilAPI (grátis, sem chave): razão social, abertura, capital,
# porte, CNAEs, Simples (opção/exclusão) e QSA com data de entrada e faixa etária.
# Dica: rode também nos outros CNPJs de cada sócio — empresa irmã costuma ser o achado.
for c in "$@"; do
  c="${c//[^0-9]/}"
  echo "===== $c"
  curl -s -m 20 "https://brasilapi.com.br/api/cnpj/v1/$c" | python3 -c '
import sys, json
d = json.load(sys.stdin)
if "razao_social" not in d: print(d); sys.exit()
for k in ["razao_social","nome_fantasia","data_inicio_atividade","capital_social","porte",
          "natureza_juridica","descricao_situacao_cadastral","cnae_fiscal_descricao",
          "municipio","uf","logradouro","numero","bairro","opcao_pelo_simples",
          "data_opcao_pelo_simples","data_exclusao_do_simples"]:
    print(f"{k}: {d.get(k)}")
print("CNAEs secundários:", [x["descricao"] for x in d.get("cnaes_secundarios", [])])
for s in d.get("qsa", []):
    print("SÓCIO:", s.get("nome_socio"), "|", s.get("qualificacao_socio"), "|",
          s.get("data_entrada_sociedade"), "|", s.get("faixa_etaria"))
'
done
