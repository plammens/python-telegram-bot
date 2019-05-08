"""
This module implements some useful shortcut decorators for handlers.
"""


import telegram.ext as tge


def cmdhandler(dispatcher, command=None, **handler_kwargs):
    """
    Decorator factory for command handlers; acts as as shortcut to add
    command handlers to a ``telegram.ext.Dispatcher``. The returned decorator adds
    the decorated function as a command handler for the command ``command``
    to ``dispatcher``. If ``command`` is not specified it defaults to
    the decorated function's name.

    Example:
    ```
    @cmdhandler(dispatcher, allow_edited=True)
    def start():
        pass
    ```

    is equivalent to
    ````
    def start():
        pass

    handler = CommandHandler('start', start, allow_edited=True)
    dispatcher.add_command_handler(handler)
    ````

    :param dispatcher: ``telegram.ext.Dispatcher`` object to which to add
                        the command handler
    :param command: name of bot command to add a handler for
    :param handler_kwargs: additional keyword arguments for the
                           creation of the command handler (these will be passed
                           to ``telegram.ext.dispatcher.add_handler``)
    :return: the decorated function, unchanged
    """

    # Actual decorator
    def decorator(callback):
        if dispatcher.use_context:
            def decorated(update, context, *args, **kwargs):
                return callback(update, context, *args, **kwargs)
        else:
            def decorated(bot, update, *args, **kwargs):
                return callback(bot, update, *args, **kwargs)

        handler = tge.CommandHandler(command or callback.__name__, decorated, **handler_kwargs)
        dispatcher.add_handler(handler)
        return callback

    return decorator
