"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from functools import wraps
from typing import Any, Callable

from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo


class CommonInjectionUtils:
    """ Utilities to inject custom functionality into other functions. """
    @staticmethod
    def inject_into(target_object: Any, target_function_name: str) -> Callable:
        """
            Obsolete: Please use inject_safely_into instead.
        """
        return CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), target_object, target_function_name)

    @staticmethod
    def inject_safely_into(mod_identity: CommonModIdentity, target_object: Any, target_function_name: str) -> Callable:
        """
            A decorator used to inject code into another function.
            It will catch and log exceptions and run the original function should any problems occur.

            Example 'cls' Usage:
            @CommonInjectionUtils.inject_safely_into(SimSpawner, SimSpawner.spawn_sim._name__)
            def do_custom_spawn_sim(original, cls, *args, **kwargs):
                return original(*args, **kwargs)

            Example 'self' Usage:
            @CommonInjectionUtils.inject_safely_into(SimInfo, SimInfo.load_sim_info.__name__)
            def do_custom_load_sim_info(original, self, *args, **kwargs):
                return original(self, *args, **kwargs)

            Note:
             Injection WILL work on:
               - Functions decorated with 'classmethod'
               - Functions with 'cls' or 'self' as the first argument.
             Injection WILL NOT work on:
               - Functions decorated with 'staticmethod'
               - Global functions, i.e. Functions not contained within a class.
        :param mod_identity: The identity of the mod injecting into a function.
        :param target_object: The class that contains the target function.
        :param target_function_name: The name of the function being injected to.
        :return: A wrapped function.
        """

        def _function_wrapper(original_function, new_function):

            @wraps(original_function)
            def _wrapped_function(*args, **kwargs):
                try:
                    return new_function(original_function, *args, **kwargs)
                except Exception as ex:
                    # noinspection PyBroadException
                    try:
                        from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                        CommonExceptionHandler.log_exception(mod_identity.name, 'Error occurred while injecting into function \'{}\' of class'.format(new_function.__name__, target_object.__name__), exception=ex)
                    except Exception:
                        pass
                    return original_function(*args, **kwargs)
            if inspect.ismethod(original_function):
                return classmethod(_wrapped_function)
            return _wrapped_function

        def _injected(wrap_function):
            original_function = getattr(target_object, target_function_name)
            setattr(target_object, target_function_name, _function_wrapper(original_function, wrap_function))
            return wrap_function
        return _injected
