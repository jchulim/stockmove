# -*- coding: utf-8 -*-

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AsmtockLocation(models.Model):
    _inherit = 'stock.location'

    valuation_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account')


class ASMStockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account')


class StockMove(models.Model):
    _inherit = 'stock.move'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account')

    def _get_analytic_acc_from_move(self):
        analytic_acc = False
        if self.analytic_account_id:
            analytic_acc = self.analytic_account_id.id
        if not analytic_acc and self.picking_id.analytic_account_id:
            analytic_acc = self.picking_id.analytic_account_id.id
        if not analytic_acc and self.location_dest_id.valuation_in_account_id:
            analytic_acc = (self.location_dest_id
                            .valuation_analytic_account_id.id)
        return analytic_acc

# pylint: disable=R0913
    def _prepare_account_move_line(
            self, qty, cost, credit_account_id, debit_account_id):
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)
        if res and res[0] and res[0][2]:
            analytic_acc = self._get_analytic_acc_from_move()
            res[0][2]['analytic_account_id'] = analytic_acc

        return res
