from __future__ import unicode_literals

from django.db import models
from django.db.models import signals

from applications.companies import models as companies_models
from applications.customers import models as customers_models
from applications.inventories import models as inventories_models
from applications.invoices import listeners as invoices_listeners
from applications.taxes import models as taxes_models

from libs import models as libs_models


class Invoice(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores invoices and their info.
    """
    company = models.ForeignKey(companies_models.Company, related_name='invoices')
    customer = models.ForeignKey(customers_models.Customer, related_name='invoices', help_text='Customer whom invoice is for.')
    seq_number = models.PositiveIntegerField(help_text='Invoice number.')
    date = models.DateField(help_text='Date of invoice generation.')
    is_paid = models.BooleanField(default=False, help_text='Represents whether this invoice has been paid.')
    pdf = models.FileField(blank=True, null=True, help_text='Rendered PDF version of invoice.')

    def __unicode__(self):
        return '{} - {}- {}'.format(self.company, self.customer, self.seq_number) if self.active else 'INACTIVE'

    @classmethod
    def _get_next_seq_number(cls):
        """
        Returns next available sequence number to use for invoice.
        """
        return (cls.all_objects.aggregate(models.Max('seq_number'))['seq_number__max'] or 0) + 1


class InvoiceItem(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores items in invoices and their info.
    """
    invoice = models.ForeignKey(Invoice, related_name='items')
    item = models.ForeignKey(inventories_models.Item, related_name='invoices')
    quantity = models.PositiveIntegerField(help_text='Quantity of item.')
    discount = models.DecimalField(decimal_places=2, max_digits=16, help_text='Amount of discount given on this item.')
    amount = models.DecimalField(decimal_places=2, max_digits=16, help_text='Actual amount of this item.')
    tax_applied = models.DecimalField(decimal_places=2, max_digits=16, help_text='Tax applied on this item.')
    total_amount = models.DecimalField(decimal_places=2, max_digits=16, help_text='Total amount taken for this item.')

    class Meta:
        unique_together = ('invoice', 'item')

    def __unicode__(self):
        return '{} - ({} - ({}))'.format(self.invoice, self.item, self.total_amount) if self.active else 'INACTIVE'


class InvoiceItemTax(libs_models.BaseSoftDeleteDatesModel):
    """
    Stores taxes on items in invoices and their info.
    """
    invoice_item = models.ForeignKey(InvoiceItem, related_name='taxes')
    tax = models.ForeignKey(taxes_models.Tax, related_name='invoiced_items')
    percentage = models.DecimalField(decimal_places=2, max_digits=16, help_text='Percentage of tax applied on the item.')
    amount = models.DecimalField(decimal_places=2, max_digits=16, help_text='Actual amount of tax applied on the item.')

    class Meta:
        unique_together = ('invoice_item', 'tax')

    def __unicode__(self):
        return '{} -> {}% -> {}'.format(self.invoice_item, self.percentage, self.amount) if self.active else 'INACTIVE'


signals.post_save.connect(invoices_listeners.update_invoice_pdf_from_invoice, sender=Invoice)
signals.post_save.connect(invoices_listeners.update_invoice_pdf_from_invoice_item, sender=InvoiceItem)
signals.post_save.connect(invoices_listeners.update_invoice_pdf_from_invoice_item_tax, sender=InvoiceItemTax)
