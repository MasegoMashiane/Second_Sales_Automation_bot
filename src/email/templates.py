class EmailTemplates:
    #Template library 
    INITIAL = '''
             <html>
             <body>
             <p>Hi {name}, </p>
             <p>I noticed {company} is doing great work in {industry}.
             I wanted to reach out because we help companies like yours {value_prop}.
             </p>
             <p> Would you be open to a quick 15-minute call this week?</p>
             <p>Best regards, <br>{sender_name}></p>
             </body>
             </html> 
'''
    FOLLOWUP_1='''
    <html>
    <body>
    <p>Hi {name}, </p>
    <p>Just following up on my previous email. I understand you're busy, 
    but I thought you might be interested in how we've helped {similar_company}
    achieve {result}.
    </p>
    <p>Would love to chat if you have 10 minutes.</p>
    <p>Best Regards, <br>{sender_name}</p>
    </body>
    </html>
    '''

    FOLLOWUP_2='''
    <html>
    <body>
    <p>Hi {name},</p>
    <p>Last follow-up! I don't want to be a pest, but wanted to share
    one quick resource that might be helpful: {resource_link}
    </p>
    <p>If now's not the right time, no worries at all.</p>
    <p>Cheers, <br>{sender_name}</p>
    </body>
    </html>
'''

    @classmethod
    def get(cls, template_name, **kwargs):
        #get template with various variables filled
        template = getattr(cls, template_name.upper())
        return template.format(**kwargs)