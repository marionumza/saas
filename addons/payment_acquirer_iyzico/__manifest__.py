{
    "name":  "Iyzico Payment Acquirer",
    "summary":  "Integrating Iyzico with Harpiya. The module allows the customers to make payments for their ecommerce orders using Iyzico Payment Gateway.",
    "category":  "Ecommerce",
    "version":  "13.0.1.0.0",
    "author":  "Boraq-Group",
    "website":  "https://boraq-group.com",
    "description":  """Iyzico Payment Acquirer """,
    "external_dependencies":  {'python': ['iyzipay']},
    "depends":  [
        'payment'
    ],
    "data":  [
        'views/payment_acquirer.xml',
        'views/payment_iyzico_templates.xml',
        'data/iyzico_payment_data.xml',
    ],
    "images":  ['static/description/banner.gif'],
    "application":  True,
    "installable":  True,
    "price":  50.0,
    "currency":  "EUR",
    "pre_init_hook":  "pre_init_check",
    "post_init_hook":  "create_missing_journal_for_acquirers"
}
