from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from datetime import datetime
import os
from research.services.structured_data import Output
from research.controllers.sendemails import Emails
from research.templates.reports.capacitados.profissionais.profissionais_capacitados_2021 import Style_prof
from research.templates.reports.capacitados.alunos.alunos_capacitados_2021 import Style_alun


class Organizador:
    """
        Classe que organiza os arquivos e diretoríos.
    """
    def __init__(self, nome):
        self.caminho = ''
        self.nUnico = ''
        self.nome = nome

    def localize(self, nomediretorioraiz):
        """
            Função para verificar o diretorio atual do computador, e criar uma pasta para cada
            tipo de arquivo, caso não exista.
        """
        try:
            self.caminho = f'{nomediretorioraiz}/'

            # Verificar se o caminho já existe.
            if os.path.exists(self.caminho):
                pass

            else:
                os.makedirs(self.caminho)
                # Criar pasta

            print('Caminho verificado com sucesso.')
            return Output().return_funtion(200, self.caminho)

        except Exception as error:
            print('Erro ao organizar o arquivo.', error)
            return Output().return_funtion(500,  error)

    def gerar_nomeU(self, time):
        """
            Função para gerar automaticamente um nome único.
        """
        try:
            time = time.replace(' ', '')
            time = time.replace('-', '')
            time = time.replace(':', '')
            time = time.replace('.', '')
            self.nUnico = time + "_" + self.nome

            print('Nome único gerado com sucesso')
            return Output().return_funtion(200, self.nUnico)

        except Exception as error:
            print('Erro ao gerar o nome único.', error)
            return Output().return_funtion(500,  error)


class Send_report:
    """
        Classe para enviar o arquivo feito e deletado após.
    """
    def __init__(self, local, filename, to_email, title):
        self.filename = filename
        self.local = local
        self.subject = title
        self.to_email = to_email
        self.text_body = f'Segue em anexo o {title}.'

    def del_arquive(self):
        """
            Função para deletar o arquivo enviado.
        """
        try:
            # Apagar o arquivo
            os.unlink(f'{self.local}/{self.filename}')
            print('Arquivo deletado.')
            return Output().return_funtion(200, None)

        except Exception as error:
            print('Erro ao apagar o arquivo.', error)
            return Output().return_funtion(500,  error)

    def sending(self):
        """
            Função para enviar o arquivo por e-mail do usuario.
        """
        try:
            print('Enviando...')
            envio = Emails(self.subject, self.text_body, self.to_email).send_anex(self.local, self.filename)

            # Para tentar 3 vezes caso dê erro.
            if envio['status'] != 200:
                x = 1
                while x <= 3 and envio['status'] != 200:
                    envio = Emails(self.subject, self.text_body, self.to_email).send_anex(self.local, self.filename)
                    x += 1

            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if envio['status'] != 200:
                print('Erro ao enviar o e-mail.')
                return Output().return_funtion(400, envio['results'])
            else:
                test = self.del_arquive()
                # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
                if test['status'] != 200:
                    print('Erro ao apagar arquivo')
                    return Output().return_funtion(test['status'], test['results'])

            return Output().return_funtion(200, None)
        except Exception as error:
            print('Erro ao tentar enviar o arquivo.', error)
            return Output().return_funtion(500,  error)


class Reports:
    """
        Classe para gerar relatórios de acordo com o tipo e dados fornecidos.
    """
    def __init__(self, iniciativa, categoria, periodo_inicio, periodo_fim, carga_horaria, to_email, type):
        self.iniciativa = iniciativa
        self.categoria = categoria
        self.periodo_inicio = periodo_inicio
        self.periodo_fim = periodo_fim
        self.carga_horaria = carga_horaria
        self.to_email = to_email
        self.type = type

    def manage_reports(self):
        """
            Função para identificar o tipo de relatório e redirecionar a geração.
        """
        try:
            if self.type == 'PROFISSIONAL-CAPACITADO':
                print('Tipo de arquivo concluído com sucesso!')
                self._get_profissional_capacitado()

                return Output().return_funtion(200, None)

            elif self.type == 'ALUNO-CAPACITADO':
                print('Tipo de arquivo concluído com sucesso!')
                self._get_aluno_capacitado()
                return Output().return_funtion(200, None)

            else:
                print('Error ao encontrar tipo de arquivo!!')
                return Output().return_funtion(404, None)

        except Exception as error:
            print('Error ao tipo de arquivo!!', error)
            return Output().return_funtion(404, error)

    def transforme_date(self):
        """
            Função para converter as datas fornecidas da API, em data do relatório.
        """
        try:
            periodo_inicio = f'{self.periodo_inicio[6:10]}-{self.periodo_inicio[3:5]}-{self.periodo_inicio[:2]}'
            periodo_fim = f'{self.periodo_fim[6:10]}-{self.periodo_fim[3:5]}-{self.periodo_fim[:2]}'
            dates = [periodo_inicio, periodo_fim]

            return Output().return_funtion(200, dates)

        except Exception as error:
            print('Erro ao converter as datas', error)
            return Output().return_funtion(500, error)

    def _get_date(self):
        """
            Função para obter o mês por extenso.
        """
        try:
            date_infull = {
                '01': 'Janeiro',
                '02': 'Fevereiro',
                '03': 'Março',
                '04': 'Abril',
                '05': 'Maio',
                '06': 'Junho',
                '07': 'Julho',
                '08': 'Agosto',
                '09': 'Setembro',
                '10': 'Outubro',
                '11': 'Novembro',
                '12': 'Dezembro'
            }
            period = self.transforme_date()
            mes_inicio = period['results'][0][5:7]
            mes_fim = period['results'][1][5:7]
            ano = period['results'][1][:4]

            period = f'{date_infull[mes_inicio][0:]} a {date_infull[mes_fim].lower()} de {ano}'
            period_red = f'({date_infull[mes_inicio][:3]}-{date_infull[mes_fim][:3]})'.upper()
            results = [period, period_red]

            return Output().return_funtion(200, results)

        except Exception as error:
            print('Erro ao encontrar o período', error)
            return Output().return_funtion(404, error)

    def _get_profissional_capacitado(self):
        """
            Função para gerar o relatório de profissionais capacitados.
        """
        try:
            nome = 'report_profissional'
            time = datetime.now()
            time = str(time)

            # obtêm o relatório atual junto com a pasta de Profissionais capacitados.
            diretorio = f'{os.getcwd()}/results/Profissionais Capacitados'

            caminho = Organizador(nome).localize(diretorio)
            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if caminho['status'] != 200:
                print('Erro ao gerar caminho e pasta')
                return Output().return_funtion(caminho['status'], caminho['results'])

            nUnico = Organizador(nome).gerar_nomeU(time)
            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if nUnico['status'] != 200:
                print('Erro ao gerar nome único')
                return Output().return_funtion(nUnico['status'], nUnico['results'])

            # Identificar a criação, local e tipo de arquivo.
            # pdf = canvas.Canvas(f'{caminho["results"]}test.pdf', pagesize=landscape(A4))
            pdf = canvas.Canvas(f'{caminho["results"]}{nUnico["results"]}.pdf', pagesize=landscape(A4))

            # Pegar os periodos em uma tupla.
            periods = self._get_date()

            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if periods['status'] != 200:
                print('Erro ao pegar periodo', periods['status'], periods['results'])
                return Output().return_funtion(periods['status'], periods['results'])

            # Montagem dos parametros
            period = periods['results'][0]

            period_reduzido = periods['results'][1]

            program = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'

            iniciativa = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com as realidades
            regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''

            entrega = self.type.replace('-', ' ')

            execucao_perid = """Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade
            presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho,
            bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles:
            professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de janeiro a junho foram
            qualificados 1.977 (mil, novecentos e setenta e sete) profissionais da educação. Dentre as principais
            formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas,
            Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """

            # Leva a geração do arquivo.
            test = Style_prof(pdf)._get_profCapacit(period, program, iniciativa, entrega, execucao_perid, period_reduzido)

            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if test['status'] != 200:
                print('Erro ao gerar relatorio')
                return Output().return_funtion(test['status'], test['results'])
            print('Gerado o relatório')

            # Chama ao envio e a deletar do arquivo.
            title = f"Relatório de {entrega} - {period}"
            # test = Send_report(caminho["results"], 'test.pdf', self.to_email, title).sending()
            test = Send_report(caminho["results"], f'{nUnico["results"]}.pdf', self.to_email, title).sending()

            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if test['status'] != 200:
                print('Erro ao gerar enviar e deletar report')
                return Output().return_funtion(test['status'], test['results'])

            return Output().return_funtion(200, None)

        except Exception as error:
            print('Erro ao gerar o relatórios de profissionais!!', error)
            return Output().return_funtion(500,  error)

    def _get_aluno_capacitado(self):
        """
            Função para gerar o relatório de profissionais capacitados.
        """
        try:
            nome = 'report_aluno'
            time = datetime.now()
            time = str(time)

            diretorio = f'{os.getcwd()}/results/Alunos Capacitados'

            caminho = Organizador(nome).localize(diretorio)
            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if caminho['status'] != 200:
                print('Erro ao gerar caminho e pasta')
                return Output().return_funtion(caminho['status'], caminho['results'])

            nUnico = Organizador(nome).gerar_nomeU(time)
            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if nUnico['status'] != 200:
                print('Erro ao gerar nome único')
                return Output().return_funtion(nUnico['status'], nUnico['results'])

            # Identificar a criação, local e tipo de arquivo.
            # pdf = canvas.Canvas(f'{caminho["results"]}test.pdf', pagesize=landscape(A4))
            pdf = canvas.Canvas(f'{caminho["results"]}{nUnico["results"]}.pdf', pagesize=landscape(A4))

            # Pegar os periodos em uma tupla.
            periods = self._get_date()

            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if periods['status'] != 200:
                print('Erro ao pegar periodo', periods['status'], periods['results'])
                return Output().return_funtion(periods['status'], periods['results'])

            # Montagem dos parametros
            period = periods['results'][0]

            period_reduzido = periods['results'][1]

            program = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'

            iniciativa = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com as realidades
                        regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''

            entrega = self.type.replace('-', ' ')

            execucao_perid = """Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade
                        presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho,
                        bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles:
                        professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de janeiro a junho foram
                        qualificados 1.977 (mil, novecentos e setenta e sete) profissionais da educação. Dentre as principais
                        formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas,
                        Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """

            # Leva a geração do arquivo.
            test = Style_alun(pdf)._get_alunCapacit(period, program, iniciativa, entrega, execucao_perid,
                                                    period_reduzido)
            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if test['status'] != 200:
                print('Erro ao gerar relatorio')
                return Output().return_funtion(test['status'], test['results'])
            print('Gerado o relatório')

            # Chama ao envio e a deletar do arquivo.
            title = f"Relatório de {entrega} - {period}"
            # test = Send_report(caminho["results"], 'test.pdf', self.to_email, title).sending()
            test = Send_report(caminho["results"], f'{nUnico["results"]}.pdf', self.to_email, title).sending()

            # Testa de a função teve sucesso, caso contrário a execução é parada com o erro.
            if test['status'] != 200:
                print('Erro ao gerar enviar e deletar report')
                return Output().return_funtion(test['status'], test['results'])

            return Output().return_funtion(200, None)

        except Exception as error:
            print('Erro ao gerar o relatórios de alunos!!', error)
            return Output().return_funtion(500, error)