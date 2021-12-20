from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, landscape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime
import os
from research.controllers.sendemails import Emails


class Organizador:
    def __init__(self, nome):
        self.caminho = ''
        self.nUnico = ''
        self.nome = nome

    def localize(self, nomediretorioraiz):
        try:
            self.caminho = f'{nomediretorioraiz}/{self.nome}'

            if os.path.exists(self.caminho):
                # print('Caminho já existe.')
                pass

            else:
                os.makedirs(self.caminho)
                # print('Caminho não existe.')

            return self.caminho

        except Exception as error:
            print('Erro ao organizar o arquivo.', error)
            return 404

    def gerar_nomeU(self, time):
        try:
            time = time.replace(' ', '')
            time = time.replace('-', '')
            time = time.replace(':', '')
            time = time.replace('.', '')
            self.nUnico = time + "_" + self.nome

            return self.nUnico

        except Exception as error:
            print('Erro ao gerar o nome único.', error)
            return 404


def _paragraphText(x, y, tamx, tamy, text, styles, pdf):
    story = [Paragraph(text, styles)]
    frame = Frame(x, y, tamx, tamy, showBoundary=0)
    frame.addFromList(story, pdf)

def del_arquive(filename):
    try:
        os.unlink(filename)

    except Exception as error:
        print('Erro ao apagar o arquivo.', error)
        return 404

class Certificates:
    def __init__(self, type, nomes):
        self.type = type
        self.nomes = nomes
        self.subject = 'Hello'
        self.to_email = 'wendel.viana1@aluno.ce.gov.br', 'erick.silva41@aluno.ce.gov.br'
        self.text_body = 'Hello Wooorlld!!'

    def manage_certificates(self):
        try:
            if self.type == 'planner':
                self._get_planner()

            if self.type == 'profcapacit':
                self._get_profCapacit()

            if self.type == 'aluncapacit':
                self._get_alunCapacit()

        except Exception as error:
            print('Error!!', error)
            return 404

    def _get_planner(self):
        try:
            for nome in self.nomes:
                time = datetime.now()
                time = str(time)

                diretorio = f'{os.getcwd()}/results/Planner'

                caminho = Organizador(nome).localize(diretorio)
                nUnico = Organizador(nome).gerar_nomeU(time)

                pdf = canvas.Canvas(f'{caminho}/{nUnico}.pdf', pagesize=portrait(A4))
                # Wallpaper
                wallpaper = 'assets/planner.jpg'
                pdf.drawImage(wallpaper, 0, 0, width=595, height=850)
                # text
                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=88,
                                        wordWrap=None,
                                        textColor=colors.black)

                text = 'Planner'
                _paragraphText(0, 600, 593, 95, text, styles, pdf)

                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=54,
                                        wordWrap=None,
                                        textColor=colors.black)
                text = '2021'
                _paragraphText(0, 540, 593, 30, text, styles, pdf)

                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=34,
                                        wordWrap=None,
                                        textColor=colors.black)
                text = 'Certificado'
                _paragraphText(0, 250, 593, 30, text, styles, pdf)

                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=24,
                                        wordWrap=None,
                                        textColor=colors.black)
                text = nome
                _paragraphText(0, 150, 593, 30, text, styles, pdf)

                pdf.save()
                Emails(self.subject, self.text_body, self.to_email).send_anex(f'{caminho}/{nUnico}.pdf')

            # del_arquive(f'{caminho}/{nUnico}.pdf')
        except Exception as error:
            print('Error!!', error)
            return 404

    def _get_profCapacit(self):
        try:
            for nome in self.nomes:
                time = datetime.now()
                time = str(time)

                diretorio = f'{os.getcwd()}/results/Professores Capacitados'

                caminho = Organizador(nome).localize(diretorio)
                nUnico = Organizador(nome).gerar_nomeU(time)

                pdf = canvas.Canvas(f'{caminho}/{nUnico}.pdf', pagesize=landscape(A4))
                # Wallpaper
                wallpaper = 'assets/images/pag1.jpg'
                pdf.drawImage(wallpaper, 0, 0, width=850, height=595)
                # text
                styles = ParagraphStyle(alignment=TA_LEFT,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.black)

                text = 'Janeiro a junho de 2021'
                _paragraphText(245, 375, 675, 30, text, styles, pdf)

                text = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'
                _paragraphText(142, 295, 675, 30, text, styles, pdf)

                text = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com ' as realidades 
                    regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''
                _paragraphText(142, 255, 674, 50, text, styles, pdf)

                text = 'PROFISSIONAL CAPACITADO'
                _paragraphText(142, 240, 675, 30, text, styles, pdf)

                text = """Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade 
                presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho, 
                bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles: 
                professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de janeiro a junho foram 
                qualificados 1.977 (mil, novecentos e setenta e sete) profissionais da educação. Dentre as principais 
                formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas, 
                Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """
                _paragraphText(142, 125, 675, 100, text, styles, pdf)

                pdf.showPage()

                # Página 2
                wallpaper = 'assets/images/pag2.jpg'
                pdf.drawImage(wallpaper, 0, 0, width=850, height=595)

                pdf.showPage()

                # Página 3
                # Wallpaper
                wallpaper = 'assets/images/pag3.jpg'
                pdf.drawImage(wallpaper, 0, 0, width=850, height=595)

                # text
                text = "PROFISSIONAL CAPACITADO"
                _paragraphText(143, 387, 675, 30, text, styles, pdf)

                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.white)

                text = 'META REALIZADA'
                _paragraphText(265, 340, 163, 30, text, styles, pdf)

                text = '(JAN-JUN)'
                _paragraphText(265, 330, 163, 30, text, styles, pdf)

                text = 'META REALIZADA'
                _paragraphText(665, 340, 150, 30, text, styles, pdf)

                text = '(JAN-JUN)'
                _paragraphText(665, 330, 150, 30, text, styles, pdf)

                styles = ParagraphStyle(alignment=TA_LEFT,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.white)

                # região1
                text = '01. CARIRI'
                _paragraphText(30, 310, 235, 30, text, styles, pdf)

                text = '02. CENTRO SUL'
                _paragraphText(30, 280, 235, 30, text, styles, pdf)

                text = '03. GRANDE FORTALEZA'
                _paragraphText(30, 255, 235, 30, text, styles, pdf)

                text = '04. LITORAL LESTE'
                _paragraphText(30, 228, 235, 30, text, styles, pdf)

                text = '05. LITORAL NORTE'
                _paragraphText(30, 202, 235, 30, text, styles, pdf)

                text = '06. LITORAL OESTE/VALE DO CURU'
                _paragraphText(30, 175, 235, 30, text, styles, pdf)

                text = '07. MACIÇO DO BATURITÉ'
                _paragraphText(30, 147, 235, 30, text, styles, pdf)

                text = '08. SERRA DA IBIAPABA'
                _paragraphText(30, 120, 235, 30, text, styles, pdf)

                # região 2
                text = '09. SERTÃO CENTRAL'
                _paragraphText(425, 310, 235, 30, text, styles, pdf)

                text = '10. SERTÃO DE CANINDÉ'
                _paragraphText(425, 280, 235, 30, text, styles, pdf)

                text = '11. SERTÃO DE SOBRAL'
                _paragraphText(425, 255, 235, 30, text, styles, pdf)

                text = '12. SERTÃO DOS CRATEÚS'
                _paragraphText(425, 228, 235, 30, text, styles, pdf)

                text = '13. SERTÃO DOS INHAMUNS'
                _paragraphText(425, 202, 235, 30, text, styles, pdf)

                text = '14. VALE DO JAGUARIBE'
                _paragraphText(425, 175, 235, 30, text, styles, pdf)

                text = '15. ESTADO DO CEARÁ'
                _paragraphText(425, 147, 235, 30, text, styles, pdf)

                # META 1
                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.black)
                text = '451'
                _paragraphText(265, 305, 163, 30, text, styles, pdf)

                text = '127'
                _paragraphText(265, 277, 163, 30, text, styles, pdf)

                text = '662'
                _paragraphText(265, 252, 163, 30, text, styles, pdf)

                text = '35'
                _paragraphText(265, 225, 163, 30, text, styles, pdf)

                text = '161'
                _paragraphText(265, 200, 163, 30, text, styles, pdf)

                text = '156'
                _paragraphText(265, 171, 163, 30, text, styles, pdf)

                text = '20'
                _paragraphText(265, 145, 163, 30, text, styles, pdf)

                text = '35'
                _paragraphText(265, 118, 163, 30, text, styles, pdf)

                # META 2
                text = '107'
                _paragraphText(665, 305, 163, 30, text, styles, pdf)

                text = '43'
                _paragraphText(665, 277, 163, 30, text, styles, pdf)

                text = '73'
                _paragraphText(665, 252, 163, 30, text, styles, pdf)

                text = '66'
                _paragraphText(665, 225, 163, 30, text, styles, pdf)

                text = '7'
                _paragraphText(665, 200, 163, 30, text, styles, pdf)

                text = '30'
                _paragraphText(665, 171, 163, 30, text, styles, pdf)

                text = '4'
                _paragraphText(665, 145, 163, 30, text, styles, pdf)

                text = '1.977'
                _paragraphText(665, 118, 163, 30, text, styles, pdf)

                pdf.save()
                Emails(self.subject, self.text_body, self.to_email).send_anex(f'{caminho}/{nUnico}.pdf')

                del_arquive(f'{caminho}/{nUnico}.pdf')
                print('Arquivo apagado!')
        except Exception as error:
            print('Error!!', error)
            return 404

    def _get_alunCapacit(self):
        try:
            for nome in self.nomes:
                time = datetime.now()
                time = str(time)

                diretorio = f'{os.getcwd()}/results/Alunos Capacitados'

                caminho = Organizador(nome).localize(diretorio)
                nUnico = Organizador(nome).gerar_nomeU(time)

                pdf = canvas.Canvas(f'{caminho}/{nUnico}.pdf', pagesize=landscape(A4))
                # Wallpaper
                wallpaper = 'assets/images/pag1.jpg'
                pdf.drawImage(wallpaper, 0, 0, width=850, height=595)
                # text
                styles = ParagraphStyle(alignment=TA_LEFT,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.black)

                text = 'Janeiro a junho de 2021'
                _paragraphText(245, 375, 675, 30, text, styles, pdf)

                text = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'
                _paragraphText(142, 295, 675, 30, text, styles, pdf)

                text = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com ' as realidades 
                    regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''
                _paragraphText(142, 255, 674, 50, text, styles, pdf)

                text = 'ALUNO CAPACITADO'
                _paragraphText(142, 240, 675, 30, text, styles, pdf)

                text = """Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade 
                presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho, 
                bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles: 
                professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de janeiro a junho foram 
                qualificados 1.977 (mil, novecentos e setenta e sete) profissionais da educação. Dentre as principais 
                formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas, 
                Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """
                _paragraphText(142, 125, 675, 100, text, styles, pdf)

                pdf.showPage()

                # Página 2
                wallpaper = 'assets/images/pag2.jpg'
                pdf.drawImage(wallpaper, 0, 0, width=850, height=595)

                pdf.showPage()

                # Página 3
                # Wallpaper
                wallpaper = 'assets/images/pag3.jpg'
                pdf.drawImage(wallpaper, 0, 0, width=850, height=595)

                # text
                text = "ALUNO CAPACITADO"
                _paragraphText(143, 387, 675, 30, text, styles, pdf)

                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.white)

                text = 'META REALIZADA'
                _paragraphText(265, 340, 163, 30, text, styles, pdf)

                text = '(JAN-JUN)'
                _paragraphText(265, 330, 163, 30, text, styles, pdf)

                text = 'META REALIZADA'
                _paragraphText(665, 340, 150, 30, text, styles, pdf)

                text = '(JAN-JUN)'
                _paragraphText(665, 330, 150, 30, text, styles, pdf)

                styles = ParagraphStyle(alignment=TA_LEFT,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.white)

                # região1
                text = '01. CARIRI'
                _paragraphText(30, 310, 235, 30, text, styles, pdf)

                text = '02. CENTRO SUL'
                _paragraphText(30, 280, 235, 30, text, styles, pdf)

                text = '03. GRANDE FORTALEZA'
                _paragraphText(30, 255, 235, 30, text, styles, pdf)

                text = '04. LITORAL LESTE'
                _paragraphText(30, 228, 235, 30, text, styles, pdf)

                text = '05. LITORAL NORTE'
                _paragraphText(30, 202, 235, 30, text, styles, pdf)

                text = '06. LITORAL OESTE/VALE DO CURU'
                _paragraphText(30, 175, 235, 30, text, styles, pdf)

                text = '07. MACIÇO DO BATURITÉ'
                _paragraphText(30, 147, 235, 30, text, styles, pdf)

                text = '08. SERRA DA IBIAPABA'
                _paragraphText(30, 120, 235, 30, text, styles, pdf)

                # região 2
                text = '09. SERTÃO CENTRAL'
                _paragraphText(425, 310, 235, 30, text, styles, pdf)

                text = '10. SERTÃO DE CANINDÉ'
                _paragraphText(425, 280, 235, 30, text, styles, pdf)

                text = '11. SERTÃO DE SOBRAL'
                _paragraphText(425, 255, 235, 30, text, styles, pdf)

                text = '12. SERTÃO DOS CRATEÚS'
                _paragraphText(425, 228, 235, 30, text, styles, pdf)

                text = '13. SERTÃO DOS INHAMUNS'
                _paragraphText(425, 202, 235, 30, text, styles, pdf)

                text = '14. VALE DO JAGUARIBE'
                _paragraphText(425, 175, 235, 30, text, styles, pdf)

                text = '15. ESTADO DO CEARÁ'
                _paragraphText(425, 147, 235, 30, text, styles, pdf)

                # META 1
                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.black)
                text = '451'
                _paragraphText(265, 305, 163, 30, text, styles, pdf)

                text = '127'
                _paragraphText(265, 277, 163, 30, text, styles, pdf)

                text = '662'
                _paragraphText(265, 252, 163, 30, text, styles, pdf)

                text = '35'
                _paragraphText(265, 225, 163, 30, text, styles, pdf)

                text = '161'
                _paragraphText(265, 200, 163, 30, text, styles, pdf)

                text = '156'
                _paragraphText(265, 171, 163, 30, text, styles, pdf)

                text = '20'
                _paragraphText(265, 145, 163, 30, text, styles, pdf)

                text = '35'
                _paragraphText(265, 118, 163, 30, text, styles, pdf)

                # META 2
                text = '107'
                _paragraphText(665, 305, 163, 30, text, styles, pdf)

                text = '43'
                _paragraphText(665, 277, 163, 30, text, styles, pdf)

                text = '73'
                _paragraphText(665, 252, 163, 30, text, styles, pdf)

                text = '66'
                _paragraphText(665, 225, 163, 30, text, styles, pdf)

                text = '7'
                _paragraphText(665, 200, 163, 30, text, styles, pdf)

                text = '30'
                _paragraphText(665, 171, 163, 30, text, styles, pdf)

                text = '4'
                _paragraphText(665, 145, 163, 30, text, styles, pdf)

                text = '1.977'
                _paragraphText(665, 118, 163, 30, text, styles, pdf)

                pdf.save()
                Emails(self.subject, self.text_body, self.to_email).send_anex(f'{caminho}/{nUnico}.pdf')

        except Exception as error:
            print('Error!!', error)
            return 404
