##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp import http
from openerp.http import request

class lia2_site(http.Controller):

	def check_token(self, token, request):
		token_from_db = request.env["portal.token"].sudo().search([("token", "=", token)])

		return len(token_from_db) > 0

	@http.route("/lia-portal/<string:token>", type="http", auth="public", website=True)
	def portal(self, token=False, **post):

		if self.check_token(token, request):
			context = {
				"employees" : request.env["hr.employee"].sudo().search([("publish_in_portal", "=", True)]),
				"projects" : request.env["project.project"].sudo().search([("publish_in_portal", "=", True)]),
				"token" : token
			}
			return request.render("lia2_site.main_template", context)			
		else:
			return request.render("lia2_site.unauthorized_template", None)


	@http.route("/lia-portal/<string:token>/project/<int:project_id>", type="http", auth="public", website=True)
	def view_project(self, project_id=None, token=None, **post):

		if self.check_token(token, request):
			context = {				
				"project" : request.env["project.project"].sudo().browse(project_id),
				"token" : token	
			}
			return request.render("lia2_site.project_template", context)
		else:
			return request.render("lia2_site.unauthorized_template", None)


	@http.route("/lia-portal/<string:token>/sprint/<int:sprint_id>", type="http", auth="public", website=True)
	def view_sprint(self, sprint_id=None, token=None, **post):
		if self.check_token(token, request):
			sprint = request.env["project.scrum.sprint"].sudo().browse(sprint_id)

			context = {				
				"sprint" : sprint,
				"token" : token	
			}
			return request.render("lia2_site.sprint_template", context)
		else:
			return request.render("lia2_site.unauthorized_template", None)


	@http.route("/lia-portal/<string:token>/employee/<int:employee_id>", type="http", auth="public", website=True)
	def view_employee(self, employee_id=None, token=None, **post):

		if self.check_token(token, request):
			employee = request.env["hr.employee"].sudo().browse(employee_id)

			context = {			
				"meetings" : request.env["project.scrum.meeting"].sudo().search([("user_id_meeting", "=", employee.id)], order="date_meeting"),
				"projects" : request.env["project.project"].sudo().search([("members", "=", employee.name)]),	
				"employee" : employee,
				"token" : token	
			}
			return request.render("lia2_site.employee_template", context)
		else:
			return request.render("lia2_site.unauthorized_template", None)

	@http.route("/lia-portal/<string:token>/employee/<int:employee_id>/meeting/<int:meeting_id>", type="http", auth="public", website=True)
	def view_meetings(self, meeting_id=None, employee_id=None, token=None, **post):

		if self.check_token(token, request):
			meeting = request.env["project.scrum.meeting"].sudo().browse(meeting_id)
			employee = request.env["hr.employee"].sudo().browse(employee_id)

			context = {
				"meetings" : request.env["project.scrum.meeting"].sudo().search([("user_id_meeting", "=", employee.id)], order="date_meeting"),
				"meeting" : meeting,
				"employee" : employee,
				"token" : token
			}
			return request.render("lia2_site.meeting_template", context)
		else:
			return request.render("lia2_site.unauthorized_template", None)