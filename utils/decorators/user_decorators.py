from django.shortcuts import render, redirect


def company_required(function):
    def the_wrapper_around_the_original_function(request, auction_id):
        if not request.user.company:
            return redirect('/no_company_error')
        return function(request, auction_id)
    return the_wrapper_around_the_original_function