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

from openerp import models, api, _, fields
import random

class project_project(models.Model):
	_inherit = "project.project"

	publish_in_portal = fields.Boolean(string="Publish In Portal")
	
class user_portal(models.Model):
	_inherit = "hr.employee"

	publish_in_portal = fields.Boolean(string="Publish In Portal")
	website_description = fields.Html(string="HTML Description", sanitize=False)


class project_token(models.Model):
	_name = "portal.token"
	_inherit = ['mail.thread', 'ir.needaction_mixin']



	def generate_token(self):
		token = ""
		alphabet = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
		for letter in range(10):
			token += alphabet[random.randrange(len(alphabet))]		
		return token	

	def generate_link(self):
		base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
		return base_url+"/lia-portal/"+self.token

	partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
	token = fields.Char(string="Token", default=generate_token)

class res_partner(models.Model):
	_inherit = "res.partner"

	token_id = fields.Many2one(comodel_name="portal.token", string="Token")

	@api.multi
	def send_invite_link(self):

		assert len(self) == 1, 'This option should only be used for a single id at a time.'

		self.token_id = self.env["portal.token"].create({})

		template = self.env.ref('lia2_site.email_template_id', False)
		compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)

		ctx = {
			"default_model" : "res.partner",
			"default_res_id" : self.id,
			"default_use_template" : bool(template),
			"default_template_id" : template.id,
			"default_composition_mode" : "comment"
		}
		self.state = "sent"
		return {
			"name" : _("Compose Email"),
			"type" : "ir.actions.act_window",
			"view_type" : "form",
			"view_mode" : "form",
			"res_model" : "mail.compose.message",
			"views" : [(compose_form.id, "form")],
			"view_id" : compose_form.id,
			"target" : "new",
			"context" : ctx
		}

	
