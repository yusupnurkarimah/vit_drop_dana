# -*- coding: utf-8 -*-
from odoo import models, fields, api
import time

SESSION_STATES =[('draft','Draft'),('open','Open'),('confirmed','Confirmed'),
('done','Done')]

class dana(models.Model):
	_name = 'drop.dana'

	name = fields.Char(string="No Form", required=True, default='New', size=100)
	kebutuhan = fields.Selection(
		selection=[
			('Operasional Kantor', 'Operasional Kantor'),
			('Bisnis', 'Bisnis')],
		string="Kebutuhan")
	referensi = fields.Char(string="Referensi Dokumen Penunjang", size=50)
	jawab = fields.Many2one(comodel_name="res.users", 
							string="Penanggung Jawab", 
							required=False,
							default=lambda self: self.env.user.id)
	alasan = fields.Char(string="Alasan Pertimbangan", size=50)
	estimasi = fields.Float(string="Estimasi Kebutuhan Dana")
	bank_asal = fields.Many2one(comodel_name="account.journal", string="Bank Asal")
	bank_tujuan = fields.Many2one(comodel_name="account.journal", string="Bank Tujuan")
	waktu = fields.Date(string="Waktu Penggunaan", required=False,
						default=lambda self:time.strftime("%Y-%m-%d"))
	state = fields.Selection(selection=SESSION_STATES, string="State", required=False,
						readonly=True,
						default=SESSION_STATES[0][0], help="")
	
	#confirm_uid = fields.Many2one(comodel_name="res.users", string="Confirm User")
	#confirm_date = fields.Date(string="Confirm Date", default=lambda self:time.strftime("%Y-%m-%d"))
	#done_uid = fields.Many2one(comodel_name="res.users", string="Done User")
	#done_date = fields.Date(string="Done Date", default=lambda self:time.strftime("%Y-%m-%d"))
	
	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('drop.dana') or 'Error Number!!!'
		return super(dana, self).create(vals)
	
	@api.multi
	def action_draft(self):
		self.state = SESSION_STATES[0][0]
	
	@api.multi
	def action_open(self):
		self.state = SESSION_STATES[1][0]

	@api.multi
	def action_confirm(self):
		self.state = SESSION_STATES[2][0]
		#self.confirm_uid = self.env.user.id
		#self.confirm_date = time.strftime("%Y-%m-%d")
	
	@api.multi
	def action_reject(self):
		self.state = SESSION_STATES[0][0]

	@api.multi
	def action_done(self):
		self.state = SESSION_STATES[3][0]
		self.create_journal_entries()
		#self.done_uid = self.env.user.id
		#self.done_date = time.strftime("%Y-%m-%d")

	@api.multi
	def create_journal_entries(self):
		#object_open = self.env['drop.dana']
		object_account = self.env['account.account']
		
		#records = object_open.search([('state', '=', 'done')])
		#for record in records:
		account_id = object_account.search([('code','=','99999')])
		
		object_account_move = self.env['account.move']
		line_ids = [
			(0, 0, {
				'account_id' : account_id.id,
				'debit' : self.estimasi,
				'credit' : 0,
			}),
			(0, 0, {
				'account_id' : self.bank_asal.default_credit_account_id.id,
				'debit' : 0,
				'credit' : self.estimasi,
			})]
		data = {
			'date' : time.strftime("%Y-%m-%d"),
			'ref' : self.name,
			'journal_id' : self.bank_asal.id,
			'line_ids' : line_ids
		}
		records = object_account_move.create(data)

		line_ids = [
			(0, 0, {
				'account_id' : account_id.id,
				'debit' : 0,
				'credit' : self.estimasi,
			}),
			(0, 0, {
				'account_id' : self.bank_tujuan.default_debit_account_id.id,
				'debit' : self.estimasi,
				'credit' : 0,
			})]
		data = {
			'date' : time.strftime("%Y-%m-%d"),
			'ref' : self.name,
			'journal_id' : self.bank_tujuan.id,
			'line_ids' : line_ids
		}
		records = object_account_move.create(data)