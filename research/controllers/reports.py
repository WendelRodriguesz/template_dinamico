from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from datetime import datetime
import os
from services.structured_data import Output
from controllers.sendemails import Emails
from templates.reports.capables.professionals.profissionais_capacitados_2021 import Style_prof
from templates.reports.capables.students.alunos_capacitados_2021 import Style_stud
 
 
class Organizer:
   """
       Class that organizes files and directories.
   """
   def __init__(self, name):
       self.path = ''
       self.name_id = ''
       self.name = name
 
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
 
           print('Path verified successfully.')
           return Output().return_funtion(200, self.path)
 
       except Exception as error:
           print('Error organizing file.', error)
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
 
           print('name_id generated successfully')
           return Output().return_funtion(200, self.name_id)
 
       except Exception as error:
           print('Error generating name_id.', error)
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
 
   def del_arquive(self):
       """
           Function to delete the uploaded file.
       """
       try:
           # Delete thefile
           os.unlink(f'{self.local}/{self.filename}')
           print('Deleted file.')
           return Output().return_funtion(200, None)
 
       except Exception as error:
           print('Error deleting file.', error)
           return Output().return_funtion(500, error)
 
   def sending(self):
       """
           Function to send the file by email from the user.
       """
       try:
           print('Sending...')
           shipping = Emails(self.subject, self.text_body, self.to_email).send_anex(self.local, self.filename)
 
           # To try 3 times if it fails.
           if shipping['status'] != 200:
               x = 1
               while x <= 3 and shipping['status'] != 200:
                   shipping = Emails(self.subject, self.text_body, self.to_email).send_anex(self.local, self.filename)
                   x += 1
 
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if shipping['status'] != 200:
               print('Error sending email.')
               return Output().return_funtion(400, shipping['results'])
           else:
               test = self.del_arquive()
               # Tests whether the function was successful, otherwise the execution is stopped with the error.
               if test['status'] != 200:
                   print('Error deleting file')
                   return Output().return_funtion(test['status'], test['results'])
 
           return Output().return_funtion(200, None)
       except Exception as error:
           print('Error trying to send the file.', error)
           return Output().return_funtion(500, error)
 
 
class Reports:
   """
       Class to generate reports according to the type and data provided.
   """
   def __init__(self, initiative, category, start_period, end_period, workload, to_email, type):
       self.initiative = initiative
       self.category = category
       self.start_period = start_period
       self.end_period = end_period
       self.workload = workload
       self.to_email = to_email
       self.type = type
 
   def manage_reports(self):
       """
           Function to identify the type of report and redirect generation.
       """
       try:
           if self.type == 'PROFISSIONAL-CAPACITADO':
               print('File type completed successfully!')
               self._get_professional_capable()
 
               return Output().return_funtion(200, None)
 
           elif self.type == 'ALUNO-CAPACITADO':
               print('File type completed successfully!')
               self._get_student_capable()
               return Output().return_funtion(200, None)
 
           else:
               print('Error finding file type!!')
               return Output().return_funtion(404, None)
 
       except Exception as error:
           print('Error to file type!!', error)
           return Output().return_funtion(404, error)
 
   def transform_date(self):
       """
           Function to convert the dates provided from the API, into the report date.
       """
       try:
           start_period = f'{self.start_period[6:10]}-{self.start_period[3:5]}-{self.start_period[:2]}'
           end_period = f'{self.end_period[6:10]}-{self.end_period[3:5]}-{self.end_period[:2]}'
           dates = [start_period, end_period]
 
           return Output().return_funtion(200, dates)
 
       except Exception as error:
           print('Error converting dates', error)
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
           print('Error finding period', error)
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
               print('Error generating path and folder')
               return Output().return_funtion(path['status'], path['results'])
 
           name_id = Organizer(name).generate_name_id(time)
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if name_id['status'] != 200:
               print('Error generating name_id name')
               return Output().return_funtion(name_id['status'], name_id['results'])
 
           # Identify the creation, location and file type.
           # pdf = canvas.Canvas(f'{path["results"]}test.pdf', pagesize=landscape(A4))
           pdf = canvas.Canvas(f'{path["results"]}{name_id["results"]}.pdf', pagesize=landscape(A4))
 
           # Get the periods in a tuple.
           periods = self._get_date()
 
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if periods['status'] != 200:
               print('Error getting period', periods['status'], periods['results'])
               return Output().return_funtion(periods['status'], periods['results'])
 
           # Setting the parameters
           period = periods['results'][0]
 
           period_reduced = periods['results'][1]
 
           program = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'
 
           initiative = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com as realidades
            regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''
 
           delivery = self.type.replace('-', ' ')
 
           execution_perid = """Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade
            presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho,
            bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles:
            professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de janeiro a junho foram
            qualificados 1.977 (mil, novecentos e setenta e sete) profissionais da educação. Dentre as principais
            formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas,
            Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """
 
           # Takes file generation.
           test = Style_prof(pdf)._get_profCapacit(period, program, initiative, delivery, execution_perid, period_reduced)
 
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if test['status'] != 200:
               print('Error generating report')
               return Output().return_funtion(test['status'], test['results'])
           print('Report generated')
 
           # Calls uploading and deleting the file.
           title = f'Relatório de {delivery} - {period}'
           # test = Send_report(path["results"], 'test.pdf', self.to_email, title).sending()
           test = Send_report(path["results"], f'{name_id["results"]}.pdf', self.to_email, title).sending()
 
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if test['status'] != 200:
               print('Error generating send and delete report')
               return Output().return_funtion(test['status'], test['results'])
 
           return Output().return_funtion(200, None)
 
       except Exception as error:
           print('Error generating professional report!!', error)
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
               print('Error generating path and folder')
               return Output().return_funtion(path['status'], path['results'])
 
           name_id = Organizer(name).generate_name_id(time)
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if name_id['status'] != 200:
               print('Error generating name_id name')
               return Output().return_funtion(name_id['status'], name_id['results'])
 
           # Identify the creation, location and file type.
           # pdf = canvas.Canvas(f'{path["results"]}test.pdf', pagesize=landscape(A4))
           pdf = canvas.Canvas(f'{path["results"]}{name_id["results"]}.pdf', pagesize=landscape(A4))
 
           # Get the periods in a tuple.
           periods = self._get_date()
 
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if periods['status'] != 200:
               print('Error getting period', periods['status'], periods['results'])
               return Output().return_funtion(periods['status'], periods['results'])
 
           # Setting the parameters
           period = periods['results'][0]
 
           period_reduced = periods['results'][1]
 
           program = '433 - DESENVOLVIMENTO DO ENSINO MÉDIO'
 
           initiative = '''433.1.01 - Qualificação curricular do Ensino Médio contextualizado com as realidades
            regionais e internacionais, e ao dinamismo socioeconômico e ambiental. '''
 
           delivery = self.type.replace('-', ' ')
 
           execution_perid = """Essa iniciativa engloba profissionais da educação que recebem formação, na modalidade
            presencial, semipresencial e educação a distância (EaD), com o objetivo qualificar seu desempenho,
            bem como contribuir para a melhoria do ensino regular na Rede Pública Estadual, sendo eles:
            professores, diretores, coordenadores pedagógicos e técnicos. Nos meses de janeiro a junho foram
            qualificados 1.977 (mil, novecentos e setenta e sete) profissionais da educação. Dentre as principais
            formações podemos citar: Compartilhando Saberes e Conhecimentos entre Pares, Jornadas Pedagógicas,
            Oficinas de Gravação de Vídeo Aulas, Curso Diálogos Socioemocionais, Conexão SEDUC. """
 
           # Takes file generation.
           test = Style_stud(pdf)._get_studCapacit(period, program, initiative, delivery, execution_perid, period_reduced)
 
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if test['status'] != 200:
               print('Error generating report')
               return Output().return_funtion(test['status'], test['results'])
           print('Report generated')
 
           # Calls uploading and deleting the file.
           title = f'Relatório de {delivery} - {period}'
           # test = Send_report(path["results"], 'test.pdf', self.to_email, title).sending()
           test = Send_report(path["results"], f'{name_id["results"]}.pdf', self.to_email, title).sending()
 
           # Tests whether the function was successful, otherwise the execution is stopped with the error.
           if test['status'] != 200:
               print('Error generating send and delete report')
               return Output().return_funtion(test['status'], test['results'])
 
           return Output().return_funtion(200, None)
 
       except Exception as error:
           print('Error generating student report!!', error)
           return Output().return_funtion(500, error)

