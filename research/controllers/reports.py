from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from datetime import datetime
import os
from services.structured_data import Output
from controllers.sendemails import Emails
from templates.reports.capables.get_report.capacitados2021 import Style_cap
from services.config_logging import Log
    
class Organizer:
    """
            Class that organizes files and directories.
    """
    def __init__(self, name):
        self.path = ''
        self.name_id = ''
        self.name = name
        self.logger = Log().logger(__name__)
    
    def locate(self, name_rootdirectory):
        """
            Function to check the computer's current directory, and create a folder for each
            type of file, if it doesn't exist.
        """
        try:
            self.path = f'{name_rootdirectory}/'
    
            # Check if the path already exists.
            if os.path.exists(self.path):
                pass
    
            else:
                os.makedirs(self.path)
                # Create folder
    
            self.logger.info('Path verified successfully.')
            return Output().return_funtion(200, self.path)
    
        except Exception as error:
            self.logger.error(f'Error organizing file. {error}')
            return Output().return_funtion(500, error)
    
    def generate_name_id(self, time):
        """
            Function to automatically generate a name_id name.
        """
        try:
            time = time.replace(' ', '')
            time = time.replace('-', '')
            time = time.replace(':', '')
            time = time.replace('.', '')
            self.name_id = time + "_" + self.name
    
            self.logger.info('name_id generated successfully')
            return Output().return_funtion(200, self.name_id)
    
        except Exception as error:
            self.logger.error(f'Error generating name_id. {error}')
            return Output().return_funtion(500, error)
    
    
class Send_report:
    """
        Class to send the file made and deleted after.
    """
    def __init__(self, location, filename, to_email, title):
        self.filename = filename
        self.local = location
        self.subject = title
        self.to_email = to_email
        self.text_body = f'Segue em anexo o {title}.'
        self.logger = Log().logger(__name__)
    
    def del_arquive(self):
        """
            Function to delete the uploaded file.
        """
        try:
            # Delete thefile
            os.unlink(f'{self.local}/{self.filename}')
            self.logger.info('Deleted file.')
            return Output().return_funtion(200, None)
    
        except Exception as error:
            self.logger.error(f'Error deleting file. {error}')
            return Output().return_funtion(500, error)
    
    def sending(self):
        """
            Function to send the file by email from the user.
        """
        try:
            self.logger.info('Sending...')
            
            shipping = Emails(self.subject, self.text_body, self.to_email).send_anex(self.local, self.filename)
            
            # To try 3 times if it fails.
            if shipping['status'] != 200:
                x = 1
                while x <= 3 and shipping['status'] != 200:
                    shipping = Emails(self.subject, self.text_body, self.to_email).send_anex(self.local, self.filename)
                    x += 1
    
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if shipping['status'] != 200:
                self.logger.error('Error sending email.')
                return Output().return_funtion(400, shipping['results'])
            else:
                test = self.del_arquive()
                # Tests whether the function was successful, otherwise the execution is stopped with the error.
                if test['status'] != 200:
                    self.logger.error('Error deleting file')
                    return Output().return_funtion(test['status'], test['results'])
    
            return Output().return_funtion(200, None)
        except Exception as error:
            self.logger.error(f'Error trying to send the file. {error}')
            return Output().return_funtion(500, error)
    
    
class Reports:
    """
        Class to generate reports according to the type and data provided.
    """
    def __init__(self, initiative, category, start_period, end_period, workload, to_email, type_template):
        self.initiative = initiative
        self.category = category
        self.start_period = start_period
        self.end_period = end_period
        self.workload = workload
        self.to_email = to_email
        self.type_template = type_template
        self.logger = Log().logger(__name__)
    
    def manage_reports(self):
        """
            Function to identify the type of report and redirect generation.
        """
        try:
            if self.type_template == 'PROFISSIONAL-CAPACITADO':
                self.logger.info('File type completed successfully!')
                self._get_professional_capable()
    
                return Output().return_funtion(200, None)
    
            elif self.type_template == 'ALUNO-CAPACITADO':
                self.logger.info('File type completed successfully!')
                self._get_student_capable()
                return Output().return_funtion(200, None)
    
            else:
                self.logger.error('Error finding file type!!')
                return Output().return_funtion(404, None)
    
        except Exception as error:
            self.logger.error(f'Error to file type!! {error}')
            # print('Error to file type!! ',  error)
            return Output().return_funtion(404, error)
    
    def transform_date(self):
        """
            Function to convert the dates provided from the API, into the report date.
        """
        try:
            start_period = f'{self.start_period[6:10]}-{self.start_period[3:5]}-{self.start_period[:2]}T00:00:00-03:00'
            end_period = f'{self.end_period[6:10]}-{self.end_period[3:5]}-{self.end_period[:2]}T23:59:59-03:00'
            dates = [start_period, end_period]
    
            return Output().return_funtion(200, dates)
    
        except Exception as error:
            self.logger.error(f'Error converting dates {error}')
            return Output().return_funtion(500, error)
    
    def _get_date(self):
        """
            Function to get the month in full.
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
            period = self.transform_date( )
            mes_start = period['results'][0][5:7]
            mes_end = period['results'][1][5:7]
            year = period['results'][1][:4]
    
            period = f'{date_infull[mes_start][0:]} à {date_infull[mes_end].lower()} de {year}'
            period_reduced= f'({date_infull[mes_start][:3]}-{date_infull[mes_end][:3]})'.upper()
            results = [period, period_reduced]
    
            return Output().return_funtion(200, results)
    
        except Exception as error:
            self.logger.error(f'Error finding period {error}')
            return Output().return_funtion(404, error)
    
    def _get_professional_capable(self):
        """
            Function to generate the report of capables professionals.
        """
        try:
            name = 'report_professional'
            time = datetime.now()
            time = str(time)
    
            # get the current report along with the Skilled Professionals folder.
            directory = f'{os.getcwd()}/research/results/Profissionais capacitados'
    
            path = Organizer(name).locate(directory)
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if path['status'] != 200:
                self.logger.error('Error generating path and folder')
                return Output().return_funtion(path['status'], path['results'])
    
            name_id = Organizer(name).generate_name_id(time)
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if name_id['status'] != 200:
                self.logger.error('Error generating name_id name')
                return Output().return_funtion(name_id['status'], name_id['results'])
            
            # Identify the creation, location and file type.
            # pdf = canvas.Canvas(f'{path["results"]}test.pdf', pagesize=landscape(A4))
            pdf = canvas.Canvas(f'{path["results"]}{name_id["results"]}.pdf', pagesize=landscape(A4))
            
            # Get the periods in a tuple.
            periods = self._get_date()
            
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if periods['status'] != 200:
                self.logger.error('Error getting period ' + periods['status'] + ' ' + periods['results'])
                return Output().return_funtion(periods['status'], periods['results'])
            
            # Setting the parameters
            period = periods['results'][0]
    
            period_reduced = periods['results'][1]
    
            program = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'
    
            initiative = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com as realidades
                regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''
    
            delivery = self.type_template.replace('-', ' ')
            
    
            total = 1  # Change heee-------------------------------------------------------------

            execution_perid = f"""Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade
                            presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho,
                            bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles:
                            professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de {period.lower()} foram
                            qualificados {str(total)} alunos da rede estadual. Dentre as principais
                            formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas,
                            Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """

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

            # Takes file generation.
            test = Style_cap(pdf)._get_Capacit(period, program, initiative, delivery, execution_perid, period_reduced, subscribers_by_region)
            # print("test")
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if test['status'] != 200:
                self.logger.error('Error generating report')
                return Output().return_funtion(test['status'], test['results'])
            self.logger.info('Report generated')
    
            # Calls uploading and deleting the file.
            title = f'Relatório de {delivery} - {period}'
            # test = Send_report(path["results"], 'test.pdf', self.to_email, title).sending()
            test = Send_report(path["results"], f'{name_id["results"]}.pdf', self.to_email, title).sending()
    
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if test['status'] != 200:
                self.logger.error('Error generating send and delete report')
                return Output().return_funtion(test['status'], test['results'])
    
            return Output().return_funtion(200, None)
    
        except Exception as error:
            self.logger.error(f'Error generating professional report!! {error}')
            return Output().return_funtion(500, error)
    
    def _get_student_capable(self):
        """
            Function to generate the report of capables students.
        """
        try:
            name = 'student_report'
            time = datetime.now()
            time = str(time)
    
            directory = f'{os.getcwd()}/research/results/Alunos capacitados'
    
            path = Organizer(name).locate(directory)
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if path['status'] != 200:
                self.logger.error('Error generating path and folder')
                return Output().return_funtion(path['status'], path['results'])
    
            name_id = Organizer(name).generate_name_id(time)
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if name_id['status'] != 200:
                self.logger.error('Error generating name_id name')
                return Output().return_funtion(name_id['status'], name_id['results'])
    
            # Identify the creation, location and file type.
            # pdf = canvas.Canvas(f'{path["results"]}test.pdf', pagesize=landscape(A4))
            pdf = canvas.Canvas(f'{path["results"]}{name_id["results"]}.pdf', pagesize=landscape(A4))
    
            # Get the periods in a tuple.
            periods = self._get_date()
    
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if periods['status'] != 200:
                self.logger.error('Error getting period ' + periods['status'] + ' ' + periods['results'])
                return Output().return_funtion(periods['status'], periods['results'])
    
            # Setting the parameters
            period = periods['results'][0]
    
            period_reduced = periods['results'][1]
    
            program = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'
    
            initiative = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com as realidades
                regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''
    
            delivery = self.type_template.replace('-', ' ')
    
            total = 1  # Change heee-------------------------------------------------------------

            execution_perid = f"""Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade
                            presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho,
                            bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles:
                            professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de {period.lower()} foram
                            qualificados {str(total)} alunos da rede estadual. Dentre as principais
                            formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas,
                            Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """

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

            # Takes file generation.
            test = Style_cap(pdf)._get_Capacit(period, program, initiative, delivery, execution_perid, period_reduced, subscribers_by_region)
    
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if test['status'] != 200:
                self.logger.error('Error generating report')
                return Output().return_funtion(test['status'], test['results'])
            self.logger.info('Report generated')
    
            # Calls uploading and deleting the file.
            title = f'Relatório de {delivery} - {period}'
            # test = Send_report(path["results"], 'test.pdf', self.to_email, title).sending()
            test = Send_report(path["results"], f'{name_id["results"]}.pdf', self.to_email, title).sending()
    
            # Tests whether the function was successful, otherwise the execution is stopped with the error.
            if test['status'] != 200:
                self.logger.error('Error generating send and delete report')
                return Output().return_funtion(test['status'], test['results'])
    
            return Output().return_funtion(200, None)
    
        except Exception as error:
            self.logger.error(f'Error generating student report!! {error}')
            return Output().return_funtion(500, error)

