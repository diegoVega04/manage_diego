from odoo import models, fields, api
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
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    is_paused = fields.Boolean()

    sprint_id = fields.Many2one("manage_diego.sprint", string="Sprint", ondelete="cascade")
    history = fields.Many2one("manage_diego.history", ondelete="set null", help="Historia relacionada")
    technologys_id = fields.Many2many(comodel_name="manage_diego.technology", 
                                        relation = "technologys_tasks", 
                                        column1 = "tasks_ids", 
                                        column2 = "technologys_ids")

    def _get_code(self):
        for task in self:
                task.code = "TSK_"+str(task.id)


class Sprint(models.Model):
    _name = 'manage_diego.sprint'
    _description = 'manage_diego.sprint'

    name = fields.Char()
    description = fields.Char()
    duration = fields.Integer()
    start_date = fields.Datetime()
    end_date = fields.Datetime()

    tasks_id = fields.One2many(string="Tasks", comodel_name="manage_diego.task", inverse_name="sprint_id")
    project = fields.Many2one("manage_diego.project")

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for sprint in self:            
                if isinstance(sprint.start_date, datetime.datetime) and sprint.duration > 0:
                    sprint.end_date = sprint.start_date + datetime.timedelta(days=sprint.duration)
                else:
                    sprint.end_date = sprint.start_date