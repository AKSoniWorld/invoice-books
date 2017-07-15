def update_invoice_pdf_from_invoice(instance, **kwargs):
    """
    Listener to update pdf of the invoice on change/creation.
    """
    # Update pdf.


def update_invoice_pdf_from_invoice_item(instance, **kwargs):
    """
    Listener to update pdf of the invoice on change/creation.
    """
    update_invoice_pdf_from_invoice(instance.invoice, **kwargs)


def update_invoice_pdf_from_invoice_item_tax(instance, **kwargs):
    """
    Listener to update pdf of the invoice on change/creation.
    """
    update_invoice_pdf_from_invoice(instance.invoice_item.invoice, **kwargs)
