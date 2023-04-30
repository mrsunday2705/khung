from odoo import fields,api,models
from odoo.exceptions import ValidationError

class ClassManage(models.Model):
    _name = "class.manage"
    _description = "Quản lý lớp học"

    classname = fields.Char(string='Lớp')
    number = fields.Integer(string='Sĩ số',readonly=True)
    number1 = fields.Integer(string='Số HS TB',readonly=True,compute='_hs') 
    number2 = fields.Integer(string='Số HS Khá',readonly=True,compute='_hs')
    number3 = fields.Integer(string='Số HS Giỏi',readonly=True,compute='_hs')
    classman_id = fields.One2many('class.student','classstu_id',string='Lớp học')


    @api.depends('classman_id')
    def _hs(self):
        for diem in self:
            diem.number = len(diem.classman_id)
            diem.number1 = len(diem.classman_id.filtered(lambda r: r.value == 'TB'))
            diem.number2 = len(diem.classman_id.filtered(lambda r: r.value == 'K'))
            diem.number3 = len(diem.classman_id.filtered(lambda r: r.value == 'G'))

class ClassStudent(models.Model):
    _name = "class.student"
    _description = "Quản lý học sinh"

    classstu_id = fields.Many2one('class.manage',string='Lớp',required=True,ondelete='cascade')
    name = fields.Char(string='Họ tên')
    point = fields.Integer(string='Điểm')
    value = fields.Selection([('TB','Trung bình'),
                              ('K','Khá'),
                              ('G','Giỏi')],
                             string='Đánh giá',compute='_danh_gia')
    
    @api.constrains('point')
    def _check_point(self):
        for diem in self:
            if diem.point < 0 or diem.point > 10:
                raise ValidationError('Điểm số phải nằm trong khoảng từ 0 đến 10')
    
    @api.depends('point')
    def _danh_gia(self):
        for diem in self:
            if diem.point <= 6:
                diem.value = 'TB'
            elif  diem.point <= 8:
                diem.value = 'K'
            else:
                diem.value = 'G'
