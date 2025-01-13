from odoo import models, fields, api # type: ignore
import datetime

class Project(models.Model):
    _name = 'manage_diego.project'
    _description = 'manage_diego.project'

    name = fields.Char()
    description = fields.Char()
    histories = fields.One2many(comodel_name="manage_diego.history", inverse_name="project")
    sprints = fields.One2many(comodel_name="manage_diego.sprint", inverse_name="project")


class History(models.Model):
    _name = 'manage_diego.history'
    _description = 'manage_diego.history'

    name = fields.Char()
    description = fields.Char()
    project = fields.Many2one("manage_diego.project", ondelete="set null")
    tasks = fields.One2many(string="Tareas", comodel_name="manage_diego.task", inverse_name="history")
    used_technologies = fields.Many2many("manage_diego.technology", compute="_get_used_technologies")

    def _get_used_technologies(self):
        for history in self:
            technologies = None
            for task in history.tasks:
                if not technologies:
                    technologies = task.technologys_id
                else:
                    technologies = technologies + task.technologys_id
            history.used_technologies = technologies


class Technology(models.Model):
    _name = 'manage_diego.technology'
    _description = 'manage_diego.technology'

    name = fields.Char()
    description = fields.Char()
    photo = fields.Image()
    tasks_id = fields.Many2many(comodel_name="manage_diego.task",
                                relation="technologys_tasks",
                                column1 = "technologys_ids",
                                column2 = "tasks_ids")


class Task(models.Model):
    _name = 'manage_diego.task'
    _description = 'manage_diego.task'

    code = fields.Char(compute="_get_code")
    name = fields.Char()
    description = fields.Char()
    start_date = fields.Datetime(default=lambda p: datetime.datetime.now()) #las tareas por defecto empiezan el dia que las creas pero se puede cambiar
    end_date = fields.Datetime()
    is_paused = fields.Boolean()
    sprint_id = fields.Many2one("manage_diego.sprint", string="Sprint", ondelete="cascade", compute="_get_sprint", store=True)
    history = fields.Many2one("manage_diego.history", ondelete="set null", help="Historia relacionada")
    technologys_id = fields.Many2many(comodel_name="manage_diego.technology", 
                                        relation = "technologys_tasks", 
                                        column1 = "tasks_ids", 
                                        column2 = "technologys_ids")
    project = fields.Many2one("manage_diego.project", related="history.project", readonly=True)
    #campo prioridad como parte de las ampliaciones mia
    prioridad = fields.Selection([
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ], default='medio')

    #codigo ajustado a los nuevos campos y con algunos cambios para evitar errores que me daban
    @api.depends('project')
    def _get_sprint(self):
        for task in self:
            if task.history and task.project:
                sprints = self.env['manage_diego.sprint'].search([
                    ('project', '=', task.project.id),
                    ('end_date', '>', fields.Datetime.now())
                ], order='end_date asc', limit=1)
                task.sprint_id = sprints.id if sprints else False
            else:
                task.sprint_id = False

    @api.depends()
    def _get_code(self):    
        for task in self:
                task.code = "TSK_"+str(task.id)


class Sprint(models.Model):
    _name = 'manage_diego.sprint'
    _description = 'manage_diego.sprint'

    name = fields.Char()
    description = fields.Char()
    duration = fields.Integer(default=5)
    start_date = fields.Datetime()
    end_date = fields.Datetime(compute="_get_end_date")

    tasks_id = fields.One2many(string="Tasks", comodel_name="manage_diego.task", inverse_name="sprint_id")
    project = fields.Many2one("manage_diego.project")

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for sprint in self:            
                if sprint.start_date and sprint.duration > 0:
                    sprint.end_date = sprint.start_date + datetime.timedelta(days=sprint.duration)
                else:
                    sprint.end_date = sprint.start_date