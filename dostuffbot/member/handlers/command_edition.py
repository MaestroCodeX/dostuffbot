# @middleware
# def command_edit_caller(update, context):
#     ''' Callback function to handle edit command button. '''
#     query = update.callback_query
#
#     command_id = get_command_id_from_call(query.data)
#     query.edit_message_text(
#         text='Send me a new command.',
#         reply_markup=keyboards.back_command_menu_markup(command_id),
#         parse_mode='MARKDOWN',
#     )


# @middleware
# def command_edit_caller_sent(update, context):
#     ''' Callback function to handle editing commmand state when caller text was sent. '''
#     caller = update.message.text
#     db_bot = context.bot.db_bot
#
#     if Command.objects.filter(bot=db_bot, caller=caller).exists():
#         update.message.reply_text(f'The command {caller} already exists.')
#
#     command = Command.objects.filter(bot=db_bot, status=CommandStatus.EDIT_CALLER).first()
#     command.caller = caller
#     command.save()
#     update.message.reply_text(
#         texts.command_menu(command),
#         reply_markup=keyboards.command_menu_markup(command),
#         parse_mode='MARKDOWN',
#     )
