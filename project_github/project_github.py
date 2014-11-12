# -*- coding: utf-8 -*-
##############################################################################
#
#    Project Github
#    Copyright (C) 2014 Hans Henrik Gabelgaard
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from github import Github
from slugify import slugify


class project_github_ghaccount(models.Model):
    _name = 'project_github.ghaccount'
    _description = 'GitHub Account'

    name = fields.Char(string='GitHub Account')
    ghtoken = fields.Char(string='GitHub Access Token')
    is_org = fields.Boolean(string='Is GitHub Organization')
    ghrepo_ids = fields.One2many(
        'project_github.ghrepo',
        'ghaccount_id',
        string='GitHub repos')

    @api.multi
    def button_fetch_repos(self):

        g = Github(self.ghtoken)
        if self.is_org:
            repos = g.get_organization().get_repos(type='owner')
        else:
            repos = g.get_user().get_repos(type='owner')
        for repo in repos:
            new_repo = True
            for ghrepo in self.ghrepo_ids:
                if ghrepo.ghrepoid == repo.id:
                    new_repo = False
            if new_repo:
                self.env['project_github.ghrepo'].create(
                    {'name': repo.name,
                     'ghrepoid': repo.id,
                     'ghaccount_id': self.id})


class project_github_ghrepo(models.Model):
    _name = 'project_github.ghrepo'
    _description = 'GitHub Repo'

    name = fields.Char(string='GitHub Repo')
    ghrepoid = fields.Integer(string='GH ID')
    ghaccount_id = fields.Many2one('project_github.ghaccount')


# class project_github_ghbranch(models.Model):
#     _name = 'project_github.ghbranh'
#     _description = 'GitHub Branch'
#
#     name = fields.Char(string='GitHub Branch')
#     ghbranchid = fields.Integer(string='GH ID')
#     ghurl      = fields.Char(string='GitHub Branch')
#     ghrepo_id = fields.Many2one('project_github.ghrepo')


class res_users(models.Model):
    _inherit = 'res.users'

    ghtoken = fields.Char(string='GitHub Access Token')


class project_project(models.Model):
    _inherit = 'project.project'

    ghrepo_id = fields.Many2one('project_github.ghrepo', string="GitHub Repo")


class project_task(models.Model):
    _inherit = 'project.task'

    ghissue = fields.Integer(string='GitHub Issue')
    ghbranch = fields.Char(string='GitHub Branch')

    @api.multi
    def button_create_open_issue(self):

        if self.ghissue:
            g = Github(self.env.user.ghtoken)
            if self.project_id.ghrepo_id.ghaccount_id.is_org:
                repo = g.get_organization().get_repo(
                    self.project_id.ghrepo_id.name)
            else:
                repo = g.get_user().get_repo(self.project_id.ghrepo_id.name)
            issue = repo.get_issue(self.ghissue)
            return {'type': 'ir.actions.act_url', 'url': issue.html_url,
                    'nodestroy': True, 'target': 'new'}
        else:
            g = Github(self.env.user.ghtoken)
            if self.project_id.ghrepo_id.ghaccount_id.is_org:
                repo = g.get_organization().get_repo(
                    self.project_id.ghrepo_id.name)
            else:
                repo = g.get_user().get_repo(self.project_id.ghrepo_id.name)

            link = '%s/?db=%s#id=%s&amp;view_type=form&amp;model=project.task' \
                % (self.env['ir.config_parameter'].search(
                    [('key', '=', 'web.base.url')])[0].value,
                   self.env.cr.dbname, self.id)
            issue = repo.create_issue(self.name, body=link)
            self.ghissue = issue.number
            return True

    @api.multi
    def button_create_open_branch(self):

        if self.ghbranch:
            g = Github(self.env.user.ghtoken)
            if self.project_id.ghrepo_id.ghaccount_id.is_org:
                repo = g.get_organization().get_repo(
                    self.project_id.ghrepo_id.name)
            else:
                repo = g.get_user().get_repo(self.project_id.ghrepo_id.name)
            link = "https://github.com/%s/%s/tree/%s" % (
                self.project_id.ghrepo_id.ghaccount_id.name,
                self.project_id.ghrepo_id.name, self.ghbranch)
            return {'type': 'ir.actions.act_url', 'url': link,
                    'nodestroy': True, 'target': 'new'}
        else:
            g = Github(self.env.user.ghtoken)
            if self.project_id.ghrepo_id.ghaccount_id.is_org:
                repo = g.get_organization().get_repo(
                    self.project_id.ghrepo_id.name)
            else:
                repo = g.get_user().get_repo(self.project_id.ghrepo_id.name)
            ref = repo.get_git_ref('heads/master')
            branch = slugify('%d %s' % (self.ghissue, self.name))
            repo.create_git_ref('refs/heads/' + branch, ref.object.sha)

            self.ghbranch = branch
            return True
