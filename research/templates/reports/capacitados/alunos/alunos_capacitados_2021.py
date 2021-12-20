from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os
from research.services.structured_data import Output


class Style_alun:
    def __init__(self, pdf):
        self.pdf = pdf

    def _paragraphText(self, x, y, tamx, tamy, text, styles):
        try:
            story = [Paragraph(text, styles)]
            frame = Frame(x, y, tamx, tamy, showBoundary=0)
            frame.addFromList(story, self.pdf)

            return Output().return_funtion(200, None)

        except Exception as error:
            print('Erro ao colocar texto no template.', error)
            return Output().return_funtion(500, error)

    def _get_informations(self, period, program, iniciativa, entrega, execucao_perid, period_red):
        try:
            informations = [
                period,
                program,
                iniciativa,
                entrega,
                execucao_perid,
                period_red
            ]

            return Output().return_funtion(200, informations)

        except Exception as error:
            print('Erro ao colocar texto no template.', error)
            return Output().return_funtion(500, error)

    def _get_alunCapacit(self, period, program, iniciativa, entrega, execucao_perid, period_red):
        try:
            diretorio = f'{os.getcwd()}/templates/reports/capacitados/'
            # Wallpaper
            wallpaper = f'{diretorio}images/pag1.jpg'
            self.pdf.drawImage(wallpaper, 0, 0, width=850, height=595)

            # Get basic information
            information = self._get_informations(period, program, iniciativa, entrega, execucao_perid, period_red)

            # text
            styles = ParagraphStyle(alignment=TA_LEFT,
                                    name='LEFT',
                                    fontSize=12,
                                    wordWrap=None,
                                    textColor=colors.black)

            period = information['results'][0]
            self._paragraphText(245, 375, 570, 30, period, styles)

            program = information['results'][1]
            self._paragraphText(142, 295, 675, 30, program, styles)

            iniciativa = information['results'][2]
            self._paragraphText(142, 265, 674, 40, iniciativa, styles)

            entrega = information['results'][3]
            self._paragraphText(142, 240, 675, 30, entrega, styles)

            execucao_perid = information['results'][4]
            self._paragraphText(142, 125, 675, 100, execucao_perid, styles)

            self.pdf.showPage()

            # Página 2
            wallpaper = f'{diretorio}images/pag2.jpg'
            self.pdf.drawImage(wallpaper, 0, 0, width=850, height=595)

            self.pdf.showPage()

            # Página 3
            # Wallpaper
            wallpaper = f'{diretorio}images/pag3.jpg'
            self.pdf.drawImage(wallpaper, 0, 0, width=850, height=595)

            # text
            self._paragraphText(143, 387, 675, 30, entrega, styles)

            styles = ParagraphStyle(alignment=TA_CENTER,
                                    name='LEFT',
                                    fontSize=12,
                                    wordWrap=None,
                                    textColor=colors.white)

            period_red = information['results'][5]
            self._paragraphText(265, 320, 153, 30, period_red, styles)
            self._paragraphText(665, 320, 153, 30, period_red, styles)

            # região1
            subscribers_by_region = {
                '01. CARIRI': 451,
                '02. CENTRO SUL': 127,
                '03. GRANDE FORTALEZA': 662,
                '04. LITORAL LESTE': 35,
                '05. LITORAL NORTE': 161,
                '06. LITORAL OESTE/VALE DO CURU': 156,
                '07. MACIÇO DO BATURITÉ': 20,
                '08. SERRA DA IBIAPABA': 35,
                '09. SERTÃO CENTRAL': 107,
                '10. SERTÃO DE CANINDÉ': 43,
                '11. SERTÃO DE SOBRAL': 73,
                '12. SERTÃO DOS CRATEÚS': 66,
                '13. SERTÃO DOS INHAMUNS': 7,
                '14. VALE DO JAGUARIBE': 30,
                '15. ESTADO DO CEARÁ': 4
            }
            column = 293
            row = [30, 265, 420, 665]
            width = [235, 153]
            height = 30
            i = 0
            total = 0

            for region in subscribers_by_region:
                subscribers = str(subscribers_by_region[region])
                total += subscribers_by_region[region]
                if column == 77:
                    column = 293
                    i = 2

                # Region
                styles = ParagraphStyle(alignment=TA_LEFT,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.white)
                self._paragraphText(row[i], column, width[0], height, region, styles)

                # Subscribers
                styles = ParagraphStyle(alignment=TA_CENTER,
                                        name='LEFT',
                                        fontSize=12,
                                        wordWrap=None,
                                        textColor=colors.black)
                self._paragraphText(row[i + 1], column, width[1], height, subscribers, styles)
                column -= 27

            # total Subscribers
            self._paragraphText(row[3], 105, width[1], height, str(total), styles)

            self.pdf.save()
            print('Relatório gerado!')
            return Output().return_funtion(200, None)

        except Exception as error:
            print('Erro ao gerar o relatórios de alunos!!', error)
            return Output().return_funtion(500, error)
