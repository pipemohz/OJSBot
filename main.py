from os import name
from bots import AuditBot
from mail_service import send_mail

# COMPLETED 1: Make a class for audit bot
# COMPLETED 2: Extract URL list from sitemap
# COMPLETED 3: Create a function for checking sidebar blocks (custom and PKP)
# COMPLETED 4: Create a funtion for checking navigation bar items and URLs
# COMPLETED 5: Create a function for URL validation
# COMPLETED 6: Create a function for filling reports to send by email
# COMPLETED 7: Create a mail service for sending reports
# IN PROCESS 10: Create a function to get current issue for audit components


bot = AuditBot()

# print(bot.inspect_journal_home('https://revistas.uexternado.edu.co/index.php/contad/'))



# send_mail()
