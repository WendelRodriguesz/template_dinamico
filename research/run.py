from controllers.reports import Reports


# Name the parameters
iniciativa = ["iniciativa 1", "iniciativa 2"]
categoria = ["categoria 1", "categoria 2"]
periodo_inicio = "01-01-2021"
periodo_fim = "31-12-2021"
carga_horaria = ["64", "32"]
email = "wendel2010@alu.ufc.br"
template = "ALUNO-CAPACITADO"    

# Cod funcional
Reports(iniciativa, categoria, periodo_inicio, periodo_fim, carga_horaria, email, template).manage_reports()

