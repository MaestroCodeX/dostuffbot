def unknown(bot, update):
    """ Default handler when no other handler worked. Just delete the message. """
    update.message.delete()
